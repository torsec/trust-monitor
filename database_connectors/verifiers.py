import psycopg2
import os

try:
    conn  = psycopg2.connect(database="attestation_tech", user="postgres", password="prova", host="172.17.0.3", port="5432")
except Exception as error:
    print("Could not connect to postgres server: %s" % error.__str__())
    os._exit(-1)

def store_verifier(verifier):
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