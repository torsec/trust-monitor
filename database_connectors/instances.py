import psycopg2

conn  = psycopg2.connect(database="instaces", user="postgres", password="prova", host="172.17.0.2", port="5432")

def store_entity(entity):
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO entities (entity_uuid,att_tech,name,external_id,type,whitelist_uuid,child,parent,state, metadata)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
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

    conn.commit()
    return