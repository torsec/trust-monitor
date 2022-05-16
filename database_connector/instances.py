import psycopg2

conn  = psycopg2.connect(database="instaces", user="postgres", password="prova", host="172.17.0.2", port="5432")

def insert_entity(entity):
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO entities (name,external_id,type,whitelist_uuid,child,parent,state, metadata)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (entity["name"], entity["external_id"], entity["type"], entity["whitelist_uuid"], entity["child"], entity["parent"], entity["state"], str(entity["metadat""a"]).replace("\'", "\"")))

    conn.commit()
    return