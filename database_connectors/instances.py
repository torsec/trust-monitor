import psycopg2
import os
import configparser

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
        id = cur.fetchone()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

def purge_entity(entity):
    cur  = conn.cursor()
    id = -1

    try:
        cur.execute("""
            DELETE FROM entities WHERE name=%s
            RETURNING entity_uuid
        """,
            (
                entity.get("entity_uuid"),
            )
        )
        id = cur.fetchone()[0][0]
        conn.commit()
    
    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}
