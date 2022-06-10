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
            "metadata" : { "type" : "object" }
        },
        "required": ["att_tech", "metadata"],
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
                INSERT INTO verifiers (att_tech,metadata)
                VALUES (%s,%s)
                RETURNING att_tech
        """, (
            verifier.get("att_tech"),
            str(verifier.get("metadata")).replace("\'", "\"")
            )
        )
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": id}

def retrieve_verifier(att_tech):
    cur = conn.cursor()

    try:
        cur.execute("""
                SELECT * FROM verifiers WHERE att_tech=%s
        """, (
            att_tech,
            )
        )
        res = cur.fetchone()
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}

    if res is None:
        return {"error": "entity_uuid " + str(att_tech) + " not present"}
    
    return { "att_tech": res[0], "metadata": res[1] }

def purge_verifier(verifier):
    cur = conn.cursor()
    id = 0

    try:
        cur.execute("""
                DELETE FROM verifiers WHERE att_tech=%s
                RETURNING att_tech
        """, (
            verifier.get("att_tech"),
            )
        )
        id = cur.fetchall()[0][0]
        conn.commit()

    except Exception as error:
        conn.commit()
        return {"error": error.__str__()}
    
    return {"id": id}