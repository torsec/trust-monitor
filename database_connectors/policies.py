import psycopg2
import os

try:
    conn  = psycopg2.connect(database="instances", user="postgres", password="prova", host="172.17.0.3", port="5432")
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
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}

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
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": str(id)}