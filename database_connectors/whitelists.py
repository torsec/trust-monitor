from http import client
from pymongo import MongoClient
from jsonschema import validate

try:
    client = MongoClient('172.17.0.2', 27017, username='mongo', password='prova')
except Exception as e:
    print("Could not connect to server: %s" % e.__str__())
    exit(-1)

"""
Connenction to the database
"""
db = client['admin']

"""
Connection to the collection
"""
whitelists = db['whitelist']

"""
Insert a new document into the whitelist database
"""
def store_whitelist(whitelist):

    schema = {
        "type" : "object",
        "properties" : {
            "whitelist_uuid" : {"type" : "number"},
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
        "required": ["whitelist_uuid", "metadata", "whitelist"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the API manager
    """
    try:
        validate(whitelist, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

    try:
        _id = whitelists.insert_one(whitelist).inserted_id
    except Exception as error:
        return {"error": error.__str__()}

    return {"id": str(whitelist["whitelist_uuid"])}

"""
Remove a document from the whitelist database
"""
def purge_whitelist(whitelist):

    _id = whitelists.delete_one( {"whitelist_uuid": whitelist["whitelist_uuid"]} )
    
    if _id.deleted_count == 0:
        return {"error": "Object with whitelist_uuid " + str(whitelist["whitelist_uuid"]) + " is not present"}

    return {"id": str(whitelist["whitelist_uuid"])}