from quart import Quart, request
from core import register_entity
from database_connectors.instances import insert_entity

app = Quart(__name__)

@app.route('/add_entity', methods=['POST'])
async def add_entity():
    """
    Body structure:
    {
        "entity_uuid": uuid,
        "att_tech": att_tech, (optional)
        "name": name,
        "external_id": id,
        "type": type,
        "whitelist_uuid": wl_uuid, (optional)
        "child": [                  (optional)
            uuid_1, uuid_2, ...
        ],
        "parent": id,   (optional)
        "metadata": {
            ...
        }
    }
    """

    body = await request.get_json()
    
    """
    Validation
    """
    if "entity_uuid" not in body:
        return "error"
    if "name" not in body:
        return "error"
    if "external_id" not in body:
        return "error"
    if "type" not in body:
        return "error"
    if "metadata" not in body:
        return "error"

    insert_entity(body)

    register_entity()

    return "success"

@app.route('/remove_entity')
async def remove_entity():
    return

@app.route('/attest_entity')
async def attest_entity():
    return

@app.route('/register_verifier')
async def register_verifier():
    return

@app.route('/upload_whitelist')
async def upload_whitelist():
    return

if __name__ == "__main__":
    app.run()
