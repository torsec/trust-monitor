import requests

version = "keylime_v6_4_0"

class KeyLimeAdapter():

    def __init__(self):
        pass

    def register(entity, whitelist):
        if version not in entity["att_tech"]:
            return {"error" : version + " is not present into the entity's attestation technologies list"}

        data = {}

        if "metadata" not in entity.keys():
            return {"error" : "metadata not found for entity " + str(entity["entity_uuid"])}
        
        if version not in entity["metadata"].keys():
            return {"error" : version + " data not present into metadata field for entity " + str(entity["entity_uuid"])}

        

        

    def delete(entity):
        if version not in entity["att_tech"]:
            return {"error" : version + " is not present into the entity's attestation technologies list"}

    def status():
        pass
