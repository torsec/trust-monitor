import psycopg2
import os
import configparser
from jsonschema import validate

config = configparser.ConfigParser()
config.read('config.ini')

try:
    conn  = psycopg2.connect(
        database='attestation_tech',
        user=config['verifiers_database']['user'],
        password=config['verifiers_database']['password'],
        host=config['verifiers_database']['address'],
        port=config['verifiers_database']['port']
    )
except Exception as error:
    print("Could not connect to postgres server: %s" % error.__str__())
    os._exit(-1)

def store_verifier(verifier):
    schema = {
         "type" : "object",
        "properties" : {
            "att_tech" : { "type" : "string" },
            "inf_id" : { "type" : "number" },
            "metadata" : { "type" : "object" }
        },
        "required": ["att_tech", "inf_id", "metadata"],
        "additionalProperties": False
    }

    """
    Validation of the document received from the core application
    """
    try:
        validate(verifier, schema=schema)
    except Exception as error:
        return {"error_values": error.__str__()}

    cur = conn.cursor()
    id = 0

    try:
        cur.execute("""
                INSERT INTO verifiers (att_tech,inf_id,metadata)
                VALUES (%s,%s,%s)
                RETURNING att_tech
        """, (
            verifier.get("att_tech"),
            verifier.get("inf_id"),
            str(verifier.get("metadata")).replace("\'", "\"")
            )
        )
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": id}

def retrieve_verifier(verifier):
    cur = conn.cursor()

    try:
        cur.execute("""
                SELECT * FROM verifiers WHERE att_tech=%s AND inf_id=%s
        """, (
            verifier.get("att_tech"),
            verifier.get("inf_id")
            )
        )
        res = cur.fetchone()
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}

    if res is None:
        return {"error": "entity_uuid " + str(verifier["att_tech"]) + " not present"}
    
    return { "att_tech": res[0], "inf_id": res[1], "metadata": res[2] }

def purge_verifier(verifier):
    cur = conn.cursor()
    id = 0

    try:
        cur.execute("""
                DELETE FROM verifiers WHERE att_tech=%s AND inf_id=%s
                RETURNING att_tech
        """, (
            verifier.get("att_tech"),
            verifier.get("inf_id")
            )
        )
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": id}