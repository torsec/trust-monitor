import psycopg2
import os
import configparser
from jsonschema import validate

config = configparser.ConfigParser()
config.read('config.ini')

try:
    conn  = psycopg2.connect(
        database='instances', 
        user=config['instances_database']['user'], 
        password=config['instances_database']['password'], 
        host=config['instances_database']['address'], 
        port=config['instances_database']['port']
    )
except Exception as error:
    print("Could not connect to postgres server: %s" % error.__str__())
    os._exit(-1)

def store_entity(entity):
    schema = {
        "type" : "object",
        "properties" : {
            "entity_uuid" : { "type" : "number" },
            "att_tech" : { 
                "type" : "array",
                "items" : { "type" : "string" }
            },
            "name" : { "type" : "string" },
            "external_id" : { "type" : "string" },
            "type" : { "type" : "string" },
            "whitelist_uuid" : { "type" : "number" },
            "child" : { 
                "type" : "array",
                "items": { "type" : "number" }
            },
            "parent" : { "type" : "number" },
            "state" : { "type" : "string" },
            "metadata" : { "type" : "object" }
        },
        "required": ["entity_uuid", "name", "external_id", "type"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the core application
    """
    try:
        validate(entity, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

    cur = conn.cursor()
    id = -1

    try:
        cur.execute("""
                INSERT INTO entities (entity_uuid,att_tech,name,external_id,type,whitelist_uuid,child,parent,state, metadata)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING entity_uuid
        """, (
            entity.get("entity_uuid"),
            entity.get("att_tech"),
            entity.get("name"),
            entity.get("external_id"),
            entity.get("type"),
            entity.get("whitelist_uuid"),
            entity.get("child"),
            entity.get("parent"),
            entity.get("state"),
            str(entity.get("metadata")).replace("\'", "\"")
            )
        )
        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

def retrieve_entity(entity):
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM entities WHERE entity_uuid=%s
        """,
            (
                entity.get("entity_uuid"),
            )
        )
        res = cur.fetchone()
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
        
    obj = {
        "entity_uuid": res[0],
        "att_tech": res[1],
        "name": res[2],
        "external_id": res[3],
        "type": res[4],
        "whitelist_uuid": res[5],
        "child": res[6],
        "parent": res[7],
        "state": res[8],
        "metadata": res[9]
    }
    
    return obj

def purge_entity(entity):
    cur  = conn.cursor()
    id = -1

    try:
        cur.execute("""
            DELETE FROM entities WHERE entity_uuid=%s
            RETURNING entity_uuid
        """,
            (
                entity.get("entity_uuid"),
            )
        )
        id = cur.fetchone()[0]
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}
