from quart import Quart, request
from core import (
    delete_policy,
    insert_att_tech,
    delete_att_tech,
    insert_entity,
    delete_entity,
    insert_whitelist,
    delete_whitelist,
    insert_policy,
    delete_policy
)

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
        return {"Error": "entity_uuid field must be present"}, 422
    if "name" not in body:
        return {"Error": "name must field be present"}, 422
    if "external_id" not in body:
        return {"Error": "external_id field must be present"}, 422
    if "type" not in body:
        return {"Error": "type field must be present"}, 422

    """
    Insert new entity in the TM
    """
    ret = insert_entity(body)

    if "error_values" in ret.keys():
        return {"Error": "entity " + str(body["entity_uuid"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"Error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"Message": "entity " + ret["id"] + " succesfully added"}

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
        return {"Error": "entity_uuid field must be present"}, 422

    ret = delete_entity(body)

    if "error" in ret.keys():
        return {"Error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"Message": "entity " + ret["id"] + " succesfully deleted"}

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
        return {"Error": "att_tech field must be present"}, 422
    if "metadata" not in body:
        return {"Error": "metadata field must be present"}, 422

    """
    Insert new attestation technology in the TM
    """
    ret = insert_att_tech(body)

    if "error" in ret.keys():
        return {"Error": "verifier " + body["att_tech"] + " :" + ret["error"]}, 500

    return {"Message": "verfier " + ret["id"] + " added succesfully"}

@app.route('/register_verifier', methods=['DELETE'])
async def remove_verifier():
    """
    Body structure:
    {
        "att_tech": name
    }
    """

    body = await request.get_json()

    """
    Mandatory values
    """
    if "att_tech" not in body:
        return {"Error": "att_tech field must be present"}, 422

    """
    Delete an attestation technology from the TM
    """
    ret = delete_att_tech(body)

    if "error" in ret.keys():
        return {"Error": "verifier " + body["att_tech"] + " :" + ret["error"]}, 500

    return {"Message": "verfier " + ret["id"] + " deleted succesfully"}


@app.route('/whitelist', methods=['POST'])
async def upload_whitelist():
    """
    Body structure:
    {
        “_id”: uuid,
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
    if "_id" not in body:
        return {"Error": "_id field must be present"}, 422
    if "metadata" not in body:
        return {"Error": "metadata field must be present"}, 422
    if "whitelist" not in body:
        return {"Error": "whitelist field must be present"}, 422

    """
    Insert new whitelist in the TM
    """
    ret = insert_whitelist(body)

    if "error_values" in ret.keys():
        return {"Error": "whitelist " + str(body["_id"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"Error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"Message": "whitelist " + ret["id"] + " added succesfully"}

@app.route('/whitelist', methods=['DELETE'])
async def remove_whitelist():
    """
    Body structure:
    {
        "_id": uuid
    }
    """
    body = await request.get_json()

    """
    Mandatory values
    """
    if "_id" not in body:
        return {"Error": "_id field must be present"}, 422

    """
    Delete a whitelist from the TM
    """
    ret = delete_whitelist(body)

    if "error" in ret.keys():
        return {"Error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"Message": "whitelist " + ret["id"] + " deleted succesfully"}

@app.route('/policy', methods=['POST'])
async def upload_policy():
    """
    Body structure:
    {
        "entity_uuid": uuid,
        "policy": policy
    }
    """

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"Error": "entity_uuid field must be present"}, 422
    if "policy" not in body:
        return {"Error": "policy field must be present"}, 422

    """
    Insert a policy for an entity in the TM
    """
    ret = insert_policy(body)

    if "error" in ret.keys():
        return {"Error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"Message": "policy for entity " + ret["id"] + " added succesfully"}

@app.route('/policy', methods=['DELETE'])
async def remove_policy():
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
        return {"Error": "entity_uuid field must be present"}, 422

    """
    Delete a policy for an entity from the TM
    """
    ret = delete_policy(body)

    if "error" in ret.keys():
        return {"Error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"Message": "policy for entity " + ret["id"] + " deleted succesfully"}

if __name__ == "__main__":
    app.run()
