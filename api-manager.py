from quart import Quart, request, send_from_directory
from quart_cors import cors
from core import (
    # delete_policy,
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
    # insert_policy,
    # read_policy,
    # delete_policy,
    attest_entity,
    read_tm_status,
    read_report
)
import configparser
from logger import logger
import requests
import os

config = configparser.ConfigParser()
config.read('config/config.ini')

app = Quart(__name__, static_folder='TM-gui/build',
            static_url_path='/app')
app = cors(app, allow_origin="*")


@app.route('/entity', defaults={'entity_uuid': None})
@app.route('/entity/<entity_uuid>')
async def get_entity(entity_uuid):
    """
    Read data about an object stored into the instances DB. Usage:
        /entity/<entity_uuid>

    If no entity_uuid is provided it responds with the whole list of entities
    """

    #entity_uuid = request.args.get('entity_uuid')
    
    """
    Mandatory values
    """
    #if entity_uuid is None:
    #    return {"error": "entity_uuid field must be present in the URL"}, 422

    ret = read_entity({"entity_uuid" : entity_uuid})

    if isinstance(ret, list):
        return {"entities": ret}

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
        "inf_id: id,
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

    return {"message": "entity " + ret["id"] + " successfully registered"}

@app.route('/entity/<entity_uuid>', methods=['DELETE'])
async def remove_entity(entity_uuid):
    """
    Delete an object from the Trust Monitor

    /entity/<entity_uuid> : entity_uuid -> identifier of the entity to delete from the TM db
    """

    #body = await request.get_json()

    """
    Mandatory values
    """
    #if "entity_uuid" not in body:
    #    return {"error": "entity_uuid field must be present"}, 422

    ret = delete_entity({'entity_uuid': entity_uuid})

    if "error" in ret.keys():
        return {"error": "entity " + str(entity_uuid) + " :" + ret["error"]}, 500

    return {"message": "entity " + ret["id"] + " successfully deleted"}

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

    body = await request.get_json()

    """
    Mandatory values
    """
    if "entity_uuid" not in body:
        return {"error": "entity_uuid field must be present"}, 422

    ret = update_entity(body)

    if "error" in ret.keys():
        return {"error": "entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500

    return {"message": "entity " + ret["id"] + " successfully updated"}

@app.route('/attest_entity', methods=['POST'])
async def ra_entity():
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
        return {"error": "entity_uuid field must be present"}, 422

    ret = start_attestation(body)

    if "error" in ret.keys():
        return {"error" : ret["error"]}, 500

    return {"message": ret["message"]}

@app.route('/attest_entity', methods=['DELETE'])
async def stop_ra_entity():
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
        return {"error": "entity_uuid field must be present"}, 422

    ret = stop_attestation(body)

    if "error" in ret.keys():
        return {"error" : ret["error"]}, 500

    return {"message": ret["message"]}

@app.route('/verifier')
async def get_verifier():
    """
    Read data about a verfier stored into the verfiers DB. Usage:
        /verifier?att_tech=<att_tech_name>&inf_id=<inf_id>

    """

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

        return ret


    ret = retrieve_att_tech({ 'att_tech': att_tech, 'inf_id': inf_id })

    if "error" in ret:
        return {"error": "verifier " + str(att_tech) + " :" + ret["error"]}, 500

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

    return {"message": "verfier " + ret["id"] + " successfully registered"}

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

    return {"message": "verfier " + ret["id"] + " successfully deleted"}

@app.route('/whitelist')
async def get_whitelist():
    """
    Read data about a whitelist stored into the whitelist DB. Usage:
        /whitelist?whitelist_uuid=<whitelist_uuid>

    """
    whitelist_uuid = request.args.get('whitelist_uuid')
    """
    Mandatory values
    """
    if whitelist_uuid is None:
        return {"error": "whitelist_uuid field must be present in the URL"}, 422

    ret = read_whitelist({ "_id": int(whitelist_uuid) })

    if "error" in ret.keys():
        return {"error": "whitelist " + str(whitelist_uuid) + " :" + ret["error"]}, 500

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
                "hash_algo": hash_algo,
                “whitelist_url”: "url" (optional)
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
        return {"error": "_id field must be present"}, 422
    if "metadata" not in body:
        return {"error": "metadata field must be present"}, 422
    if "whitelist" not in body:
        #if "whitelist_url" not in body["metadata"]:
        #    return {"error": "whitelist_url field must be present in metadata, whitelist is not specified"}, 422
        return {"error": "whitelist field must be present"}, 422

    """
    Insert new whitelist in the TM
    """
    ret = insert_whitelist(body)

    if "error_values" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error_values"]}, 422

    if "error" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"message": "whitelist " + ret["id"] + " added successfully"}

@app.route('/whitelist', methods=['DELETE'])
async def remove_whitelist():
    """
    Delete a whitelist from the Trust Monitor database

    Body structure:
    {
        "_id": uuid
    }
    """
    body = await request.get_json()

    """
    Mandatory values
    """
    if body is None or "_id" not in body:
        return {"error": "_id field must be present"}, 422

    """
    Delete a whitelist from the TM
    """
    ret = delete_whitelist(body)

    if "error" in ret.keys():
        return {"error": "whitelist " + str(body["_id"]) + " :" + ret["error"]}, 500

    return {"message": "whitelist " + ret["id"] + " successfully deleted"}

# @app.route('/policy')
# async def get_policy():
#     """
#     Read data about a policy for a specific entity stored into the policies DB. Usage:
#         /policy?entity_uuid=<entity_uuid>
# 
#     """
#     entity_uuid = request.args.get('entity_uuid')
#     """
#     Mandatory values
#     """
#     if entity_uuid is None:
#         return {"error": "entity_uuid field must be present in the URL"}, 422
# 
#     ret = read_policy( {"entity_uuid": int(entity_uuid)} )
# 
#     if "error" in ret.keys():
#         return {"error": "policy for entity " + str(entity_uuid) + " :" + ret["error"]}, 500
# 
#     return ret

# @app.route('/policy', methods=['POST'])
# async def upload_policy():
#     """
#     Store a new policy, for a specific object registered into the Trust Monitor
# 
#     Body structure:
#     {
#         "entity_uuid": uuid,
#         "policy": policy
#     }
#     """
# 
#     body = await request.get_json()
# 
#     """
#     Mandatory values
#     """
#     if "entity_uuid" not in body:
#         return {"error": "entity_uuid field must be present"}, 422
#     if "policy" not in body:
#         return {"error": "policy field must be present"}, 422
# 
#     """
#     Insert a policy for an entity in the TM
#     """
#     ret = insert_policy(body)
# 
#     if "error" in ret.keys():
#         return {"error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500
# 
#     return {"message": "policy for entity " + ret["id"] + " added successfully"}

# @app.route('/policy', methods=['DELETE'])
# async def remove_policy():
#     """
#     Delete a policy, for a specific object registered into the Trust Monitor
#     
#     Body structure:
#     {
#         "entity_uuid": uuid
#     }
#     """
#     body = await request.get_json()
# 
#     """
#     Mandatory values
#     """
#     if "entity_uuid" not in body:
#         return {"error": "entity_uuid field must be present"}, 422
# 
#     """
#     Delete a policy for an entity from the TM
#     """
#     ret = delete_policy(body)
# 
#     if "error" in ret.keys():
#         return {"error": "policy for entity " + str(body["entity_uuid"]) + " :" + ret["error"]}, 500
# 
#     return {"message": "policy for entity " + ret["id"] + " successfully deleted"}

@app.route('/status')
async def get_status():

    ret = read_tm_status()

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
    #TODO

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

    return ret

# Serve React App
@app.route('/<path:path>')
async def static_dir(path):
    if path != "" and os.path.exists(app.static_folder.__str__() + '/' + path):
        return await send_from_directory(app.static_folder, path)

@app.route('/app', defaults={'path': ''})
@app.route('/app/<path:path>')  
async def serve(path):     
    if path != "" and os.path.exists(app.static_folder.__str__() + '/' + path):
        return await send_from_directory(app.static_folder, path)
    else:
        return await send_from_directory(app.static_folder, 'index.html')

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
            port=5443,
            ca_certs=config["tls"]["ca_certs"], 
            certfile=config["tls"]["certfile"],  
            keyfile=config["tls"]["keyfile"]
        )
    else:
        app.run(host="0.0.0.0", port=5080)
    