import json
import requests
import time
from kafka_connector.kafka_connector import run_kafka_producer

tech = "keylime_v6_4_0"

class KeyLimeAdapter():

    def __init__(self):
        pass

    def register(entity, whitelist, verifier):
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}

        data = {}

        if "tenant_ip" not in verifier["metadata"].keys():
            return {"error" : "tanant_ip not found for technology " + str(verifier["att_tech"])}
        #
        # agent_id = external_id
        #
        keylime_tenant_url = "http://" + verifier["metadata"]["tenant_ip"] + "/v2.0/agents/" + entity["external_id"]

        if "metadata" not in entity.keys():
            return {"error" : "metadata not found for entity " + str(entity["entity_uuid"])}
        
        if tech not in entity["metadata"].keys():
            return {"error" : tech + " data not present into metadata field for entity " + str(entity["entity_uuid"])}
        #
        # start building the body for the API request
        #
        if "agent_ip" not in entity["metadata"][tech].keys():
            return {"error" : "no agent_id field specified in " + str(tech) + " metadata"}

        data["agent_ip"] = entity["metadata"][tech]["agent_id"]
        data["ptype"] = 0
        data["file_data"] = "base64"

        if "tpm_policy" in entity["metadata"][tech].keys():
            data["tpm_policy"] = entity["metadata"][tech]["tpm_policy"]

        data["a_list_data"] = whitelist["whitelist"]

        if "e_list_data" in entity["metadata"][tech].keys():
            data["e_list_data"] = entity["metadata"][tech]["e_list_data"]

        #
        # contact the tenant API
        #
        response = requests.post(keylime_tenant_url, json=data)
        response_body = response.json()

        if response.status_code == 200:
            return {"state" : "entity " + entity["name"] + " succesfully registered in " + tech + " technology"}
        else:
            return {"error" : "Response code: " + str(response.status_code) + ", Status: \"" + response_body['status'] + "\""}

    def attest(entity, verifier):
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}

        #
        # agent_id = external_id
        #
        keylime_tenant_url = "http://" + verifier["metadata"]["tenant_ip"] + "/v2.0/agents/" + entity["external_id"]

        while True:
            response = requests.get(keylime_tenant_url)

            response_body = response.json()

            if response_body['results']['operational_state'] in [3, 4, 5, 6]:  # trusted state
                run_kafka_producer( {
                    "entity_uuid": entity["entity_uuid"],
                    "att_tech": tech,
                    "trust": True
                } )
                time.sleep(1)
            else:
                run_kafka_producer( {
                    "entity_uuid": entity["entity_uuid"],
                    "att_tech": tech,
                    "trust": False
                } )
                break

    def delete(entity):
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}

    def status():
        pass
