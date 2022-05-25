import json
import requests

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

        keylime_tenant_url = "http://" + verifier["metadata"]["tenant_ip"] + "/v2.0/agents/" + entity["external_id"]

        if "metadata" not in entity.keys():
            return {"error" : "metadata not found for entity " + str(entity["entity_uuid"])}
        
        if tech not in entity["metadata"].keys():
            return {"error" : tech + " data not present into metadata field for entity " + str(entity["entity_uuid"])}
        #
        #start building the body for the API request
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

        response = requests.post(keylime_tenant_url, data=json.dump(data))

    def delete(entity):
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}

    def status():
        pass
