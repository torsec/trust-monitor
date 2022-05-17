import psycopg2

conn  = psycopg2.connect(database="attestation_tech", user="postgres", password="prova", host="172.17.0.2", port="5432")

def store_verifier(verifier):
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO verifiers (att_tech,metadata)
            VALUES (%s,%s)
    """, (
        verifier.get("att_tech"),
        str(verifier.get("metadata")).replace("\'", "\"")
        )
    )

    conn.commit()
    return