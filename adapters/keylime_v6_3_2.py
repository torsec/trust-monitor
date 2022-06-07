import json
import requests
import time
from kafka_connector.kafka_connector import run_kafka_producer

tech = "keylime_v6_3_2"

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
        """
        metadata structure:
        {
            "keylime_v6_3_2": {
                "agent_ip": ip,
                "tpm_policy": value, (optional) 
                "e_list_data": exclude_list (optional)
            }
        }
        """

        if "agent_ip" not in entity["metadata"][tech].keys():
            return {"error" : "no agent_ip field specified in " + str(tech) + " metadata"}

        data["agent_ip"] = entity["metadata"][tech]["agent_ip"]
        data["ptype"] = 0
        data["file_data"] = ""

        if "tpm_policy" in entity["metadata"][tech].keys():
            data["tpm_policy"] = entity["metadata"][tech]["tpm_policy"]
        
        """
        whitelist object:
        {
            “_id”: uuid,
            "metadata": {
                    "att_tech": att_tech,
                    "hash_algo": hash_algo
            },
            “whitelist”: {
                "a_list_data": [
                    "hash0_sha256 boot_aggregate",
                    "hash1 _sha1 /path/to/file1",
                    "hash2_sha256 /path/to/file1",
                    "hash3_sha1 /path/to/file2",
                    "hash4_sha256 /path/to/file2",
                    ...
                ]
            }
        }
        """
        data["a_list_data"] = whitelist["whitelist"]["a_list_data"]

        if "e_list_data" in entity["metadata"][tech].keys():
            data["e_list_data"] = entity["metadata"][tech]["e_list_data"]

        #
        # contact the tenant API
        #
        """
        {
            "agent_ip": "192.168.0.103",
            "ptype": 0,
            "file_data": "",
            "a_list_data": [
                "000...    boot_aggregate",
                "hash1_256bit   file_path1",
                "hash2_256bit   file_path2",
                "hash3_256bit   file_path3",
                ...
            ],
            "e_list_data":  [
                "/var/log/wtmp",
                "/root/etc/fstab",
                "/boot/grub/grubenv",
                "/sys/fs/.*",
                    ...
            ],
            "pods": {
                "9be621ca-7746-4217-8a28-eab90077ac33": {
                    "a_list_data": [
                        "38ad9774b801c168a15f328a015a1405920ba94148b43ab6143184140252489b /pause",
                        "1edf98db8b375f6fe7e275e3db013777f7c0d5945a49a0f67cf902e90456d6b7 /usr/bin/local-path-provisioner"
                    ]
                },
                "a94e4991-a53f-4952-87ee-6a2b0269e3bf": {
                    "a_list_data": [
                        "38ad9774b801c168a15f328a015a1405920ba94148b43ab6143184140252489b /pause",
                        "d84ccc80082ceb5abbd13377f3d72fb5d02394f3ac087ce36d236e91e42e4dae /metrics-server"
                    ]
                }
            }
        }
        """
        response = requests.post(keylime_tenant_url, json=data)
        response_body = response.json()

        if response.status_code == 200:
            return {"state" : "entity " + entity["name"] + " succesfully registered in " + tech + " technology"}
        else:
            return {"error" : "Response code: " + str(response.status_code) + ", Status: \"" + response_body['status'] + "\""}

    def attest(entity, verifier, topic):
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
                }, topic )
                time.sleep(1)
            else:
                run_kafka_producer( {
                    "entity_uuid": entity["entity_uuid"],
                    "att_tech": tech,
                    "trust": False
                }, topic )
                break

    def delete(entity):
        if tech not in entity["att_tech"]:
            return {"error" : tech + " is not present into the entity's attestation technologies list"}

    def status():
        pass
