from distutils.log import error
import re
from quart import Quart, request
from core import insert_att_tech,insert_entity,delete_entity,insert_whitelist

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
        return {"Error": "entity_uuid field must be present"}
    if "name" not in body:
        return {"Error": "name must field be present"}
    if "external_id" not in body:
        return {"Error": "external_id field must be present"}
    if "type" not in body:
        return {"Error": "type field must be present"}

    """
    Insert new entity in the TM
    """
    ret = insert_entity(body)

    if "error" in ret.keys():
        return {"Error": "entity " + body["entity_uuid"] + " :" + error}

    return {"Message": "entity " + body["entity_uuid"] + "succesfully added"}

@app.route('/entity', methods=['DELETE'])
async def remove_entity():
    """
    Body structure:
    {
        "entity_uuid": uuid
    }
    """

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"Error": "entity_uuid field must be present"}

    ret = delete_entity(body)

    if "error" in ret.keys():
        return {"Error": "entity " + body["entity_uuid"] + " :" + error}

    return {"Message": "entity " + body["entity_uuid"] + " succesfully deleted"}

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

    """
    Mandatory values
    """
    if "att_tech" not in body:
        return {"Error": "att_tech field must be present"}
    if "metadata" not in body:
        return {"Error": "metadata field must be present"}

    """
    Insert new attestation technology in the TM
    """
    ret = insert_att_tech(body)

    return {"Message": "verfier " + body["att_tech"] + " added succesfully"}

@app.route('/whitelist', methods=['POST'])
async def upload_whitelist():
    """
    Body structure:
    {
        “whitelist_uuid”: uuid,
        "metadata": {
                "att_tech": att_tech,
                "hash_algo": hash_algo
        },
        “whitelist”: {
               ...
        }
    }
    """
    body = await request.get_json()

    """
    Mandatory values
    """
    if "whitelist_uuid" not in body:
        return {"Error": "id field must be present"}
    if "whitelist" not in body:
        return {"Error": "whitelist field must be present"}

    """
    Insert new whitelist in the TM
    """
    ret = insert_whitelist(body)

    return {"Message": "whitelist " + str(body["whitelist_uuid"]) + " added succesfully"}

@app.route('/whitelist', methods=['DELETE'])
async def delete_whitelist():
    return

if __name__ == "__main__":
    app.run()
