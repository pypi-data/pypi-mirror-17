from flask_restful import reqparse, Api, Resource
from flask import make_response, request
from functools import wraps
import psycopg2
import psycopg2.extras
from psycopg2 import pool
import sys
import json
import hashlib
import logging
import time
import re
import gevent

from marshmallow import Schema as BaseMarshmallowSchema, post_dump
from marshmallow_jsonapi import Schema, fields

from prometheus_client import Histogram, Gauge, Counter, core
inprogress_requests_gauge = Gauge('inprogress_requests', 'Requests in progress', [])
request_time = Histogram('request_processing_seconds', 'Time spent processing request', ['endpoint'], buckets=(.01, .025, .05, .075, .10, .125, .15, .175, .20, .225, .25, .275,  .30, .325,  .35, .40, .45, .50, .60, .70, 1.0, 2.0, 3.0, 5.0, 10.0, core._INF))
query_time = Histogram('query_processing_seconds', 'Time spent processing DB query', ['query'], buckets=(.02, .04, .06, .08, .10, .125, .15, .175, .20, .250, .30, .4, .5, .6, .8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 8.0, core._INF))
connection_error_gauge = Gauge('connection_errors', 'Number of DB connection errors', [])
timeout_error_gauge = Gauge('timeout_errors', 'Number of DB timeout errors', [])
existing_connections_gauge = Gauge('existing_connections', 'Number of DB connections', [])

# Rollbar key
rollbar_key = os.environ.get('ROLLBAR_KEY')


#
#
# util
#
# utility routines
#
#

parser = reqparse.RequestParser()
parser.add_argument('offset')
parser.add_argument('limit')

dbconfig = {
    "atlas": {
        "dbname" : "atlas",
        "user" : "",
        "password" : "",
        "host" : "localhost",
        "port" : "5432"
    },
    "gustavo": {
        "dbname" : "gustavo",
        "user" : "gustavo",
        "password" : "gustavofrog123",
        "host" : "gustavo-james.cbntcda0y69o.us-east-1.rds.amazonaws.com",
        "port" : "5432"
    }
}


######################################################################
# Intialize gateway and databse
######################################################################
gwconfig = {
    'gateway': 'localhost'
}
def initGateway(gateway):
    if (gateway == 'localhost' or gateway == ''):
        gwconfig['gateway'] = 'localhost'
    else:
        gateway_env = gateway.split(".")[3]
        gwconfig['gateway'] = "http://web.stable.op-api-gateway." + gateway_env + ".lonelyplanet.com"


CONNECT_TIMEOUT=5
connectionPool = None

def initDBPool(host, dbname, user, password, retries, port):
    global connectionPool
    connectionPool = pool.ThreadedConnectionPool(0, 120,host=host, database=dbname, user=user,password=password,port=port,connect_timeout=CONNECT_TIMEOUT)


def initDBParams(name, host, dbname, user, password, retries, port):
    dbconfig[name]["dbname"] = dbname
    dbconfig[name]["user"] = user
    dbconfig[name]["password"] = password
    dbconfig[name]["host"] = host
    dbconfig[name]["retries"] = retries
    dbconfig[name]["port"] = port


DEFAULT_PAGING = 10
START_RETRY_TIMEOUT = 60
SLOW_QUERY_WARN_THRESHOLD_SEC = 1.0
SLOW_QUERY_INFO_THRESHOLD_SEC = 0.3

######################################################################
# Resource
######################################################################

class LoggingCursor(psycopg2.extras.DictCursor):

    @staticmethod
    def compress_whitespace(s):
        return re.sub('\s+', ' ', s)

    @staticmethod
    def truncate(v, length=75):
        s = LoggingCursor.compress_whitespace(v)
        return(s[:length] + '..') if len(s) > length else s

    def execute(self, sql, args=None):
        logger = logging.getLogger()
        try:
            with Timer() as t:
                psycopg2.extras.DictCursor.execute(self, sql, args)
            if t.interval > SLOW_QUERY_WARN_THRESHOLD_SEC:
                logger.warn(LoggingCursor.truncate(self.mogrify(sql, args)), extra={'timing': t.interval})
            elif t.interval > SLOW_QUERY_INFO_THRESHOLD_SEC:
                logger.info(LoggingCursor.truncate(self.mogrify(sql, args)), extra={'timing': t.interval})

        except Exception, exc:
            logger.error("%s %s" % (sql, args))
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

######################################################################
# connectToDB - simple db connection
######################################################################
class ConnectionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def getConnection(obj):
    obj.conn = connectionPool.getconn()
    #obj.conn.set_session(isolation_level=psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)


class DB_Cursor():

    def __init__(self, name):
        self.timer = query_time.labels({"query": name}).time()

    def __enter__(self):
        # Call connection through greenlet - this is so we can timeout on connection
        self.conn = None
        g = gevent.spawn(getConnection, self)
        g.join(timeout=CONNECT_TIMEOUT)

        if not g.successful():
            # Not completely clear this can ever happen - but just in case we got a connection and greenlet was not successful - 
            # put it back on stack (otherwise we leak connections)
            if (self.conn):
                connectionPool.putconn(self.conn)

            # record that error happens in the greenlet - connection could not be established
            connection_error_gauge.inc()
            raise ConnectionError("Connection Pool could not access database")

        # Make sure we got a valid connection - if not - we timed out
        if (self.conn == None):
            timeout_error_gauge.inc()
            raise ConnectionError("Timeout attempting to get connection")

        # return cursor back to user 
        self.timer.__enter__()
        existing_connections_gauge.inc()
        return self.conn.cursor(cursor_factory=LoggingCursor)

    def __exit__(self, type, value, traceback):

        # place connection back on pool
        connectionPool.putconn(self.conn)

        # decrement gauge and stop timer
        existing_connections_gauge.dec()
        self.timer.__exit__(type, value, traceback)



######################################################################
# escape some of the atlas fields so they works in json
# XXX figure out the correct way of doing this!
######################################################################
def escapeField(field):
    #return json.dumps(field)
    return filter(lambda x: ord(x) >= 32 and ord(x)<128, field.replace('"', '\\"').replace('\n', ''))

######################################################################
# standard responses from our endpoints
######################################################################
def stdResponse(obj):
   if (obj != None):

       if ("links" not in obj):
           obj["links"] = {}
       obj["links"]["self"] = request.path + (("?" + request.query_string) if request.query_string else "")
       return obj, 200, {'Etag': hashlib.sha1(json.dumps(obj)).hexdigest()}
   else:
       return errorObject("no object found", 404)

def notFoundResponse():
    logging.error("resource not found")
    return errorObject("resource not found", 404)

def badRequestResponse():
    logging.error("bad request")
    return errorObject("bad request", 400)

def errorResponse(msg):
   return errorObject(msg, 500)

def errorObject(msg, status, title="error"):
    return {"errors": [
              {
                "status": str(status),
                "title":  title,
                "detail": msg
                }
            ]}, status


######################################################################
# Api error handling wrapper class
######################################################################
import traceback
class OpenPlanetApi(Api):
    def __init__(self, *args, **kwargs):
        super(OpenPlanetApi, self).__init__(*args, **kwargs)
        self.representations = {
            'application/vnd.api+json': output_apijson,
        }


    def handle_error(self, e):
        code = getattr(e, 'code', 500)
        #if code == 500:      # for HTTP 500 errors return my custom response
        #return super(OpenPlanetApi, self).handle_error(e) # for all other errors than 500 use flask-restful's default error handling
        #traceback.print_exc()
        etype, value, tb = sys.exc_info()
        logging.error(" ".join(traceback.format_exception_only(etype, value)))
        return self.make_response( {"errors": [
              {
                "status": "error",
                "detail": str(e)
                }
            ]}, code)
        #return errorResponse(str(e))


def output_apijson(data, code, headers=None):
    resp = make_response(json.dumps(data, indent=4, sort_keys=True), code)
    resp.headers.extend(headers or {})
    return resp




######################################################################
# Resource
######################################################################
def convertPathToMetricName(path):
    # This routine will replace the id fields with the constant ID so that we do not have a proliferation
    # of metric name
    # Currently - using a simple algorithm with replacing all sequence of digits with the name ID.  This
    # will break if we use numbers in our endpoints - might want to go to a more sophisticated algorithm at that point
    return re.sub('\d+', 'ID', path)

def logRequest(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Timer() as t:
            with inprogress_requests_gauge.track_inprogress():
                with request_time.labels({"endpoint": convertPathToMetricName(request.path)}).time():
                    result = func(*args, **kwargs)
        logging.info("endpoint request", extra={'path': request.path, 'timing': t.interval})
        return result
    return wrapper


class OpResource(Resource):
    method_decorators = [logRequest]


######################################################################
# Utility Schemas
######################################################################

class UrlSchema(BaseMarshmallowSchema):
    href = fields.URL(relative=True)

class GeoJsonCoordinatesSchema(BaseMarshmallowSchema):
    coordinates = fields.List(fields.Float())
    type = fields.Str()


######################################################################
# Mixin classes for schemas
######################################################################
class MoveLinksFromAttributes:
    @post_dump(pass_many=True)
    def moveLinksFromAttributes(self, data, many):
        try:
            # if it is just one object - make it a list so we can use same iteration for next step
            dataSectionList = data["data"] if many else [data["data"]]
            for dataSection in dataSectionList:
                for k,v in dataSection["attributes"]["links"].items():
                    dataSection["links"][k] = v
                del dataSection["attributes"]["links"]
        except:
            pass
            #print "no data->attributes->links section"
            #print data

        return data

class FixRelationshipsEmptyData:
    @post_dump(pass_many=True)
    def fixRelationshipsEmptyData(self, data, many):
        try:
            # if it is just one object - make it a list so we can use same iteration for next step
            dataSectionList = data["data"] if many else [data["data"]]
            for dataSection in dataSectionList:
                for k,v in dataSection["relationships"].items():
                    if (not v):
                        dataSection["relationshpis"][k] = { "data": None }

        except:
            logging.error("Error finding relationship")

        return data

######################################################################
# Filters
######################################################################
def getFilters(request, allowableFilters, resourceType=None):

    filterItems = [item for item in request.args.items() if item[0].lower().startswith("filter")]
    #print "Filter Items: ", filterItems

    filterRegexArray = []
    for allowableFilter, allowableOperators in allowableFilters.items():
        allowableOperatorsStr = "|".join(allowableOperators)
        filterRegexArray.append(r'filter\[({allowableFilter})\]\[({allowableOperators})\]'.format(allowableFilter=allowableFilter, allowableOperators=allowableOperatorsStr))
        if (resourceType):
            filterRegexArray.append(r'filter\[{resourceType}\]\[({allowableFilter})\]\[({allowableOperators})\]'.format(resourceType=resourceType,allowableFilter=allowableFilter, allowableOperators=allowableOperatorsStr))


    filterRegex = "|".join(filterRegexArray)
    #print "regex: ", filterRegex

    filters = {}
    for item,value in filterItems:
        m = re.search(filterRegex, item)
        if (m):
            match_tuple = filter(None, m.groups())
            filters[match_tuple[0]] = {"operator": match_tuple[1], "value": value}
        else:
            logging.error("did not find: %s" % str(item))

    #print "FILTERS"
    #print filters
    #print
    return filters


######################################################################
# Health Check
######################################################################
class ContactInfoSchema(BaseMarshmallowSchema):
    service_owner_slack_id = fields.Str(dump_to="service-owner-slackid")
    slack_channel = fields.Str(dump_to="slack-channel")

class HealthCheckSchema(Schema):
    id = fields.Str()
    lp_service_group_id = fields.Str(dump_to="lp-service-group-id")
    contact_info = fields.Nested(ContactInfoSchema, dump_to="contact-info")
    github_repo_name = fields.Str(dump_to="github-repo-name")
    github_commit = fields.Str(dump_to="github-commit")
    docker_image = fields.Str(dump_to="docker-image")
    dependencies = fields.Relationship(include_resource_linkage=True, many=True, type_="database-dependency-report")
    class Meta:
        type_ = "op-service"
        strict = True
        self_url = "/health-check"


######################################################################
# Timer utility
######################################################################
class Timer:
    def __enter__(self):
        #self.start = time.clock()
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        #self.interval = self.end - self.start
        self.interval = time.time() - self.start


######################################################################
# Query Class - makes a db query
######################################################################
class Query(object):
    def __init__(self, builder):
        self.builder = builder
    def query(self):
        pass


######################################################################
# Builder Class - builds parameters for query class
######################################################################
class Builder(object):
    def __init__(self, QueryObjCls):
        # Create query object
        self.queryObj = QueryObjCls(self)

    def query(self):
        self.queryResults = self.queryObj.query()
        return self.queryResults


