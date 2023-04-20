import psycopg2
import os
import configparser
from jsonschema import validate

config = configparser.ConfigParser()
config.read('config/config.ini')

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
            "inf_id" : { "type" : "number" },
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
        "required": ["entity_uuid", "inf_id", "name", "external_id", "type"],
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
                INSERT INTO entities (entity_uuid,inf_id,att_tech,name,external_id,type,whitelist_uuid,child,parent,state,metadata)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING entity_uuid
        """, (
            entity.get("entity_uuid"),
            entity.get("inf_id"),
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
        conn.rollback()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

def edit_entity(entity):
    cur = conn.cursor()
    id = -1

    try:
        if "inf_id" in entity:
            cur.execute("""
                    UPDATE entities SET inf_id=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("inf_id"),
                entity.get("entity_uuid")
                )
            )

        if "att_tech" in entity:
            cur.execute("""
                    UPDATE entities SET att_tech=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("att_tech"),
                entity.get("entity_uuid")
                )
            )

        if "name" in entity:
            cur.execute("""
                    UPDATE entities SET name=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("name"),
                entity.get("entity_uuid")
                )
            )

        if "external_id" in entity:
            cur.execute("""
                    UPDATE entities SET external_id=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("external_id"),
                entity.get("entity_uuid")
                )
            )

        if "type" in entity:
            cur.execute("""
                    UPDATE entities SET type=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("type"),
                entity.get("entity_uuid")
                )
            )

        if "whitelist_uuid" in entity:
            cur.execute("""
                    UPDATE entities SET whitelist_uuid=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("whitelist_uuid"),
                entity.get("entity_uuid")
                )
            )

        if "child" in entity:
            cur.execute("""
                    UPDATE entities SET child=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("child"),
                entity.get("entity_uuid")
                )
            )

        if "parent" in entity:
            cur.execute("""
                    UPDATE entities SET parent=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("parent"),
                entity.get("entity_uuid")
                )
            )

        if "metadata" in entity:
            print(str(entity.get("metadata")).replace("\'", "\""))
            cur.execute("""
                    UPDATE entities SET metadata=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                str(entity.get("metadata")).replace("\'", "\""),
                entity.get("entity_uuid")
                )
            )

        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.rollback()
        return {"error": error.__str__()}

    return {"id": str(id)}

def edit_state_entity(entity):
    cur = conn.cursor()
    id = -1

    try:
        if "state" in entity:
            cur.execute("""
                    UPDATE entities SET state=%s WHERE entity_uuid=%s
                    RETURNING entity_uuid
            """, (
                entity.get("state"),
                entity.get("entity_uuid")
                )
            )

        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.rollback()
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

    if res is None:
        return {"error": "entity_uuid " + str(entity["entity_uuid"]) + " not present"}

    obj = {
        "entity_uuid": res[0],
        "inf_id": res[1],
        "att_tech": res[2],
        "name": res[3],
        "external_id": res[4],
        "type": res[5],
        "whitelist_uuid": res[6],
        "child": res[7],
        "parent": res[8],
        "state": res[9],
        "metadata": res[10]
    }
    
    return obj

def retrieve_all_entities():
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM entities
        """
        )
        res = cur.fetchall()
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}

    if res is None:
        return {"error": "no entity is present in the database"}

    ret_list = []
    for tup in res:
        obj = {
            "entity_uuid": tup[0],
            "inf_id": tup[1],
            "att_tech": tup[2],
            "name": tup[3],
            "external_id": tup[4],
            "type": tup[5],
            "whitelist_uuid": tup[6],
            "child": tup[7],
            "parent": tup[8],
            "state": tup[9],
            "metadata": tup[10]
        }

        ret_list.append(obj)
    
    return ret_list

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
