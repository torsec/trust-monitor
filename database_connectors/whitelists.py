#from pymongo import MongoClient
import psycopg2
from jsonschema import validate
import os
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

client = None
# try:
#     client = MongoClient(
#         config['whitelists_database']['address'], 
#         int(config['whitelists_database']['port']), 
#         username=config['whitelists_database']['user'], 
#         password=config['whitelists_database']['password']
#     )
# except Exception as e:
#     print("Could not connect to mongoDB server: %s" % e.__str__())
#     os._exit(-1)

try:
    conn  = psycopg2.connect(
        database='whitelist', 
        user=config['whitelists_database']['user'], 
        password=config['whitelists_database']['password'], 
        host=config['whitelists_database']['address'], 
        port=config['whitelists_database']['port']
    )
except Exception as error:
    print("Could not connect to postgres server: %s" % error.__str__())
    os._exit(-1)

"""
Connenction to the database
"""
# db = client['admin']

"""
Connection to the collection
"""
# whitelists = db['whitelist']

"""
Insert a new document into the whitelist database
"""
def store_whitelist(whitelist):

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
                "additionalProperties": True
            },
            "whitelist" : {"type" : "object"}
        },
        "required": ["_id", "metadata", "whitelist"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the API manager
    """
    try:
        validate(whitelist, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

#    try:
#        _id = whitelists.insert_one(whitelist).inserted_id
#    except Exception as error:
#        return {"error": error.__str__()}

#    return {"id": str(_id)}

    cur = conn.cursor()
    id = -1

    try:
        cur.execute("""
                INSERT INTO whitelists (whitelist_id,metadata,whitelist)
                VALUES (%s,%s,%s)
                RETURNING whitelist_id
        """, (
            whitelist.get("_id"),
            str(whitelist.get("metadata")).replace("\'", "\""),
            str(whitelist.get("whitelist")).replace("\'", "\"")
            )
        )
        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.rollback()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

"""
Retreive a document from the whitelist database
"""
def retrieve_whitelist(whitelist):
#    try:
#        res = whitelists.find_one( {"_id": whitelist["_id"]} )
#    except Exception as error:
#        return {"error": error.__str__()}
#
#    if res is None:
#        return {"error": "whitelist " + str(whitelist["_id"]) + " not present"}
#
#    return res

    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM whitelists WHERE whitelist_id=%s
        """,
            (
                whitelist.get("_id"),
            )
        )
        res = cur.fetchone()
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}

    if res is None:
        return {"error": "whitelist_id " + str(whitelist["_id"]) + " not present"}

    obj = {
        "whitelist_id": res[0],
        "metadata": res[1],
        "whitelist": res[2],
    }
    
    return obj

"""
Remove a document from the whitelist database
"""
def purge_whitelist(whitelist):
#    try:
#        _id = whitelists.delete_one( {"_id": whitelist["_id"]} )
#    except Exception as error:
#        return {"error": error.__str__()}
#
#    if _id.deleted_count == 0:
#        return {"error": "Object with _id " + str(whitelist["_id"]) + " is not present"}
#
#    return {"id": str(whitelist["_id"])}

    cur  = conn.cursor()
    id = -1

    try:
        cur.execute("""
            DELETE FROM whitelists WHERE whitelist_id=%s
            RETURNING whitelist_id
        """,
            (
                whitelist.get("_id"),
            )
        )
        id = cur.fetchone()[0]
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}