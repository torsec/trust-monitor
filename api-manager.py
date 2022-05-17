from quart import Quart, request
from core import store_att_tech,insert_entity

app = Quart(__name__)

@app.route('/entity', methods=['POST'])
async def add_entity():
    """
    Body structure:
    {
        "entity_uuid": uuid,
        "att_tech": [att_tech_1, att_tech_2, ...], (optional)
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
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"Error": "entity_uuid must be present"}
    if "name" not in body:
        return {"Error": "name must be present"}
    if "external_id" not in body:
        return {"Error": "external_id must be present"}
    if "type" not in body:
        return {"Error": "type must be present"}

    """
    Insert new entity in the TM
    """
    insert_entity(body)

    return {"Message": "entity " + body["entity_uuid"] + " added succesfully"}

@app.route('/entity', methods=['DELETE'])
async def remove_entity():
    return

@app.route('/attest_entity')
async def attest_entity():
    return

@app.route('/register_verifier', methods=['POST'])
async def register_verifier():
    """
    Body structure:
    {
        "att_tech": name,
        "metadata": {
            ...
        }
    }
    """

    body = await request.get_json()

    store_att_tech(body)

    return {"Message": "verfier " + body["att_tech"] + " added succesfully"}

@app.route('/whitelist', methods=['POST'])
async def upload_whitelist():
    return

@app.route('/whitelist', methods=['DELETE'])
async def delete_whitelist():
    return

if __name__ == "__main__":
    app.run()
