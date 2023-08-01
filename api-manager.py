from quart import Quart, request
from quart_cors import cors
from core import (
    delete_policy,
    insert_att_tech,
    delete_att_tech,
    retrieve_att_tech,
    retrieve_all_att_tech,
    insert_entity,
    start_attestation,
    stop_attestation,
    update_entity,
    read_entity,
    delete_entity,
    insert_whitelist,
    delete_whitelist,
    read_whitelist,
    insert_policy,
    read_policy,
    delete_policy,
    attest_entity,
    read_tm_status,
    read_report
)
import configparser
from logger import logger
import requests

config = configparser.ConfigParser()
config.read('config/config.ini')

app = Quart(__name__)
app = cors(app, allow_origin="*")

def verify_token(token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    #return True, 'Token verified correctly'

    try:
        response = requests.post("https://" + config["spi-idm"]["address"] + ":" + config["spi-idm"]["port"] + "/auth/realms/fishy-realm/protocol/openid-connect/userinfo", data={
            'access_token': token
        }, headers=headers, verify=False)
        response_body = response.json()
    except:
        return False, 'Internal Server Error'
    
    if response.status_code == 500:
        return False, 'Internal Server Error'
    
    if('error' in response_body):
        return False, response_body['error_description']
    else:
        return True, response_body['preferred_username']

@app.route('/entity')
async def get_entity():
    """
    Read data about an object stored into the instances DB. Usage:
        /entity?entity_uuid=<id>&token=<access_token>

    If no entity_uuid is provided it responds with the whole list of entities
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    entity_uuid = request.args.get('entity_uuid')
    
    """
    Mandatory values
    """
    #if entity_uuid is None:
    #    return {"error": "entity_uuid field must be present in the URL"}, 422

    ret = read_entity({"entity_uuid" : entity_uuid})

    if isinstance(ret, list):
        return {"entities": ret, "username": descriprion}

    if "error" in ret.keys():
        return {"error": "entity " + str(entity_uuid) + " :" + ret["error"]}, 500

    return ret

@app.route('/entity', methods=['POST'])
async def add_entity():
    """
    Register a new object into the Trust Monitor

    Body structure:
    {
        "entity_uuid": uuid,
        "inf_id": id,
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

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()
    
    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422
    if "inf_id" not in body:
        return {"error": "inf_id field must be present"}, 422
    if "name" not in body:
        return {"error": "name must field be present"}, 422
    if "external_id" not in body:
        return {"error": "external_id field must be present"}, 422
    if "type" not in body:
        return {"error": "type field must be present"}, 422

    """
    Insert new entity in the TM
    """
    ret = insert_entity(body)

    if "error_values" in ret.keys():
        return {"error": "entity " + str(body["entity_uuid"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "entity " + ret["id"] + " successfully registered", "username": descriprion}

@app.route('/entity', methods=['DELETE'])
async def remove_entity():
    """
    Delete an object from the Trust Monitor

    Body structure:
    {
        "entity_uuid": uuid
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = delete_entity(body)

    if "error" in ret.keys():
        return {"error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "entity " + ret["id"] + " successfully deleted", "username": descriprion}

@app.route('/entity', methods=['PUT'])
async def modify_entity():
    """
    Update an object saved into the Trust Monitor

    Body structure:
    {
        "entity_uuid": uuid,
        "att_tech": [att_tech_1, att_tech_2, ...], (optional)
        "name": name,  (optional)
        "external_id": id,  (optional)
        "type": type,  (optional)
        "whitelist_uuid": wl_uuid, (optional)
        "child": [                  (optional)
            uuid_1, uuid_2, ...
        ],
        "parent": id,   (optional)
        "metadata": {   (optional)
            ...
        }
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = update_entity(body)

    if "error" in ret.keys():
        return {"error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "entity " + ret["id"] + " successfully updated", "username": descriprion}

@app.route('/attest_entity', methods=['POST'])
async def ra_entity():
    """
    Body structure:
    {
        "entity_uuid": uuid
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = start_attestation(body)

    if "error" in ret.keys():
        return {"error" : ret["error"]}, 500

    return {"message": ret["message"], "username": descriprion}

@app.route('/attest_entity', methods=['DELETE'])
async def stop_ra_entity():
    """
    Body structure:
    {
        "entity_uuid": uuid
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = stop_attestation(body)

    if "error" in ret.keys():
        return {"error" : ret["error"]}, 500

    return {"message": ret["message"], "username": descriprion}

@app.route('/verifier')
async def get_verifier():
    """
    Read data about a verfier stored into the verfiers DB. Usage:
        /verifier?token=<token>&att_tech=<att_tech_name>&inf_id=<inf_id>

    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    att_tech = request.args.get('att_tech')
    inf_id = request.args.get('inf_id')
    #body = await request.get_json()

    """
    Mandatory values
    """
    #if "att_tech" not in body:
    #    return {"error": "att_tech field must be present"}, 422
    #if "inf_id" not in body:
    #    return {"error": "inf_id field must be present"}, 422
   
    if att_tech is None or inf_id is None:
        ret = retrieve_all_att_tech()

        if "error" in ret:
            return {"error": "verifier " + str(att_tech) + " :" + ret["error"]}, 500

        return {"verifiers": ret, "username": descriprion}


    ret = retrieve_att_tech({ 'att_tech': att_tech, 'inf_id': inf_id })

    if "error" in ret:
        return {"error": "verifier " + str(att_tech) + " :" + ret["error"]}, 500
    
    ret["username"] = descriprion

    return ret

@app.route('/verifier', methods=['POST'])
async def register_verifier():
    """
    Store information about a new attestation technology, into the Trust Monitor

    Body structure:
    {
        "att_tech": name,
        "inf_id": id,
        "metadata": {
            ...
        }
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "att_tech" not in body:
        return {"error": "att_tech field must be present"}, 422
    if "inf_id" not in body:
        return {"error": "inf_id field must be present"}, 422
    if "metadata" not in body:
        return {"error": "metadata field must be present"}, 422

    """
    Insert new attestation technology in the TM
    """
    ret = insert_att_tech(body)

    if "error_values" in ret.keys():
        return {"error": "verifier " + str(body["att_tech"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"error": "verifier " + str(body["att_tech"]) + " :" + ret["error"]}, 500

    return {"message": "verfier " + ret["id"] + " successfully registered", "username": descriprion}

@app.route('/verifier', methods=['DELETE'])
async def remove_verifier():
    """
    Delete information about a specific attestation technology from the Trust Monitor

    Body structure:
    {
        "att_tech": name,
        "inf_id": id
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "att_tech" not in body:
        return {"error": "att_tech field must be present"}, 422
    if "inf_id" not in body:
        return {"error": "inf_id field must be present"}, 422

    """
    Delete an attestation technology from the TM
    """
    ret = delete_att_tech(body)

    if "error" in ret.keys():
        return {"error": "verifier " + str(body["att_tech"]) + " :" + ret["error"]}, 500

    return {"message": "verfier " + ret["id"] + " successfully deleted", "username": descriprion}

@app.route('/whitelist')
async def get_whitelist():
    """
    Read data about a whitelist stored into the whitelist DB. Usage:
        /whitelist?whitelist_uuid=<whitelist_uuid>

    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    whitelist_uuid = request.args.get('whitelist_uuid')
    """
    Mandatory values
    """
    if whitelist_uuid is None:
        return {"error": "whitelist_uuid field must be present in the URL"}, 422

    ret = read_whitelist({ "_id": int(whitelist_uuid) })

    if "error" in ret.keys():
        return {"error": "whitelist " + str(whitelist_uuid) + " :" + ret["error"]}, 500

    ret["username"] = descriprion

    return ret

@app.route('/whitelist', methods=['POST'])
async def upload_whitelist():
    """
    Upload a new whitelist into the Trust Monitor database

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

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "_id" not in body:
        return {"error": "_id field must be present"}, 422
    if "metadata" not in body:
        return {"error": "metadata field must be present"}, 422
    if "whitelist" not in body:
        return {"error": "whitelist field must be present"}, 422

    """
    Insert new whitelist in the TM
    """
    ret = insert_whitelist(body)

    if "error_values" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"message": "whitelist " + ret["id"] + " added successfully", "username": descriprion}

@app.route('/whitelist', methods=['DELETE'])
async def remove_whitelist():
    """
    Delete a whitelist from the Trust Monitor database

    Body structure:
    {
        "_id": uuid
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification
    
    body = await request.get_json()

    """
    Mandatory values
    """
    if "_id" not in body:
        return {"error": "_id field must be present"}, 422

    """
    Delete a whitelist from the TM
    """
    ret = delete_whitelist(body)

    if "error" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"message": "whitelist " + ret["id"] + " successfully deleted", "username": descriprion}

@app.route('/policy')
async def get_policy():
    """
    Read data about a policy for a specific entity stored into the policies DB. Usage:
        /policy?entity_uuid=<entity_uuid>

    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    entity_uuid = request.args.get('entity_uuid')
    """
    Mandatory values
    """
    if entity_uuid is None:
        return {"error": "entity_uuid field must be present in the URL"}, 422

    ret = read_policy( {"entity_uuid": int(entity_uuid)} )

    if "error" in ret.keys():
        return {"error": "policy for entity " + str(entity_uuid) + " :" + ret["error"]}, 500

    return ret

@app.route('/policy', methods=['POST'])
async def upload_policy():
    """
    Store a new policy, for a specific object registered into the Trust Monitor

    Body structure:
    {
        "entity_uuid": uuid,
        "policy": policy
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422
    if "policy" not in body:
        return {"error": "policy field must be present"}, 422

    """
    Insert a policy for an entity in the TM
    """
    ret = insert_policy(body)

    if "error" in ret.keys():
        return {"error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "policy for entity " + ret["id"] + " added successfully"}

@app.route('/policy', methods=['DELETE'])
async def remove_policy():
    """
    Delete a policy, for a specific object registered into the Trust Monitor
    
    Body structure:
    {
        "entity_uuid": uuid
    }
    """

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    """
    Delete a policy for an entity from the TM
    """
    ret = delete_policy(body)

    if "error" in ret.keys():
        return {"error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "policy for entity " + ret["id"] + " successfully deleted"}

@app.route('/status')
async def get_status():

    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    ret = read_tm_status()

    ret["username"] = descriprion

    return ret

@app.route('/report', methods=['POST'])
async def get_report():
    """
    Get reports for a spacific entity

    Body structure:
    {
        "entity_uuid": uuid,
        "last": true, (optional) boolean
        "from": time_1, (optional) ISOFormat %Y-%m-%dT%H:%M:%S
        "to": time_2 (optional) ISOFormat %Y-%m-%dT%H:%M:%S
    }
    """
    
    #token verification
    token = request.args.get('token')
    success, descriprion = verify_token(token)
    if success is False:
        return {"error": descriprion}, 401
    #END token verification

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = read_report(body)

    if "error_values" in ret.keys():
        return {"error": ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"error": ret["error"]}, 500

    ret["username"] = descriprion

    return ret

if __name__ == "__main__":
    
#
# start the API server
#
    if "tls" in config:
        if "ca_certs" not in config["tls"]:
            raise Exception("No ca_certs specified in tls section of config/config.ini")
        if "certfile" not in config["tls"]:
            raise Exception("No certfile specified in tls section of config/config.ini")
        if "keyfile" not in config["tls"]:
            raise Exception("No keyfile specified in config/config.ini")

        app.run(
            host="0.0.0.0",
            port=config["tls"]["port"],
            ca_certs=config["tls"]["ca_certs"], 
            certfile=config["tls"]["certfile"],  
            keyfile=config["tls"]["keyfile"]
        )
    else:
        app.run(host="0.0.0.0", port=config["api-manager"]["port"])
    