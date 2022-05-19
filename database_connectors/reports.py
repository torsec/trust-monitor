from pymongo import MongoClient
from jsonschema import validate
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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
            "_id" : {"type" : "number"},
            "metadata" : {
                "type" : "object",
                "properties" : {
                    "att_tech" : {"type" : "string"},
                    "hash_algo" : {"type" : "string"}
                },
                "required": ["att_tech", "hash_algo"],
                "additionalProperties": False
            },
            "whitelist" : {"type" : "object"}
        },
        "required": ["_id", "metadata", "whitelist"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the core application
    """
    try:
        validate(report, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

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