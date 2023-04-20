from pymongo import MongoClient
from jsonschema import validate
import os
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config/config.ini')

client = None
try:
    client = MongoClient(
        config['reports_database']['address'], 
        int(config['reports_database']['port']), 
        username=config['reports_database']['user'], 
        password=config['reports_database']['password']
    )
except Exception as e:
    print("Could not connect to mongoDB server: %s" % e.__str__())
    os._exit(-1)

"""
Connenction to the database
"""
db = client['admin']

"""
Connection to the collection
"""
reports = db['reports']


"""
Insert a new document into the reports database
"""
def store_report(report):
    schema = {
        "type" : "object",
        "properties" : {
            "entity_uuid" : {"type" : "number"},
            "trust" : {"type" : "boolean"},
            "time" : {"type" : "string"},
            "state" : {
                "type" : "array",
                "items" : {
                    "type" : "object",
                    "properties" : {
                        "att_tech" : { "type" : "string" },
                        "trust" : { "type" : "boolean" }
                    },
                    "required": ["att_tech", "trust"],
                    "additionalProperties": False
                }
            },
            "metadata" : { "type" : "object" }
        },
        "required": ["entity_uuid", "trust", "time", "state"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the core application
    """
    try:
        validate(report, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

    # fix the date object
    report["time"] = datetime.strptime(report["time"], '%Y-%m-%d %H:%M:%S.%f')

    try:
        _id = reports.insert_one(report).inserted_id
    except Exception as error:
        return {"error": error.__str__()}

    return {"id": str(_id)}

"""
Remove a document from the reports database
"""
def purge_report(report):

    _id = reports.delete_one( {"_id": report["_id"]} )
    
    if _id.deleted_count == 0:
        return {"error": "Object with _id " + str(report["_id"]) + " is not present"}

    return {"id": str(report["_id"])}

"""
Retrieve reports into a date range for a specific entity
"""
def retrieve_reports(request):
    schema = {
        "type" : "object",
        "properties" : {
            "entity_uuid" : {"type" : "number"},
            "last" : {"type" : "boolean"},
            "from" : {"type" : "string"},
            "to" : {"type" : "string"}
        },
        "required": ["entity_uuid"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the core application
    """
    try:
        validate(request, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

    try:
        if "last" in request.keys() and request["last"] is True:
            res = reports.find( {"entity_uuid": request["entity_uuid"]} ).sort([("time",-1)]).limit(1)
        else:
            if "from" in request.keys():
                if "to" in request.keys():
                    res = reports.find( {"entity_uuid": request["entity_uuid"], "time": {
                        "$gt": datetime.strptime(request["from"], "%Y-%m-%dT%H:%M:%S"),     #datetime.strptime(request["from"], "%Y-%m-%dT%H:%M:%S").isoformat(),
                        "$lt": datetime.strptime(request["to"], "%Y-%m-%dT%H:%M:%S")       #datetime.strptime(request["to"], "%Y-%m-%dT%H:%M:%S").isoformat()
                    }} )
                else:
                    res = reports.find( {"entity_uuid": request["entity_uuid"], "time":{
                        "$gt": datetime.strptime(request["from"], "%Y-%m-%dT%H:%M:%S")
                    }} )
            elif "to" in request.keys():
                res = reports.find( {"entity_uuid": request["entity_uuid"], "time": {
                    "$lt": datetime.strptime(request["to"], "%Y-%m-%dT%H:%M:%S")
                }} )
            else:
                res = reports.find( {"entity_uuid": request["entity_uuid"]} )

    except Exception as error:
        return {"error": error.__str__()}

    if res is None:
        return {"error": "report(s) for entity " + str(request["entity_uuid"]) + " not present"}

    return_list = []
    for report in res:
        report['_id'] = str(report['_id']) # convert ObjectID to string for json serialization
        return_list.append(report)

    return {"report_list": return_list}