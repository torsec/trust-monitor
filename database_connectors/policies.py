import psycopg2
import os
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

try:
    conn  = psycopg2.connect(
        database="policy", 
        user=config['policies_database']['user'],
        password=config['policies_database']['password'],
        host=config['policies_database']['address'],
        port=config['policies_database']['port']
    )
except Exception as error:
    print("Could not connect to postgres server: %s" % error.__str__())
    os._exit(-1)

def store_policy(policy):
    cur = conn.cursor()
    id = 0

    try:
        cur.execute("""
                INSERT INTO policies (entity_uuid,policy)
                VALUES (%s,%s)
                RETURNING entity_uuid
        """, (
            policy.get("entity_uuid"),
            policy.get("policy")
            )
        )
        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

def retrieve_policy(policy):
    cur = conn.cursor()

    try:
        cur.execute("""
                SELECT * FROM policies WHERE entity_uuid=%s
        """, (
            policy.get("entity_uuid"),
            )
        )
        res = cur.fetchone()
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}

    if res is None:
        return {"error": "policy for entity_uuid " + str(policy["entity_uuid"]) + " not present"}
    
    return { "entity_uuid": res[0], "policy": res[1] }

def purge_policy(policy):
    cur = conn.cursor()
    id = 0

    try:
        cur.execute("""
                DELETE FROM policies WHERE entity_uuid=%s
                RETURNING entity_uuid
        """, (
            policy.get("entity_uuid"),
            )
        )
        id = cur.fetchone()[0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}