import configparser
import importlib
import sys

config = configparser.ConfigParser()
config.read('config/config.ini')

classes = {}

# Import all adapters (the name of the att_tech attribute of an entity must match the name of one of the adapters' scripts)
# Adapters must be specified in the config/config.ini file:
# [adapters]
# file_name = class_name
def refresh_adapters():
    for module in config["adapters"].keys():
        class_ = config["adapters"][module]
        try:
            classes[module] = getattr(importlib.import_module("."+module, "adapters"), class_) #__import__("adapters."+module, fromlist=[module]), class_
        except:
            print("Adapter " + module + " NOT found!", file=sys.stderr)


def register_entity(entity, whitelist, verifier):

    refresh_adapters()
    
    if verifier["att_tech"] in classes.keys():
        if hasattr(classes[verifier["att_tech"]], 'register') and callable(getattr(classes[verifier["att_tech"]], 'register')):
            classes[verifier["att_tech"]].register(entity, whitelist, verifier)
        else:
            return {"error" : "no register() method found for " + verifier["att_tech"] + " adapter"}  
    else:
        return {"error" : "no adapter found for attestation technology " + verifier["att_tech"] }

def verify_entity(entity, verifier, whitelist, se, topic):

    refresh_adapters()

    if verifier["att_tech"] in classes.keys():
        if hasattr(classes[verifier["att_tech"]], 'register') and callable(getattr(classes[verifier["att_tech"]], 'register')):
            classes[verifier["att_tech"]].attest(entity, verifier, whitelist, se, topic)
        else:
            return {"error" : "no attest() method found for " + verifier["att_tech"] + " adapter"}  
    else:
        return {"error" : "no adapter found for attestation technology " + verifier["att_tech"] }

def delete_entity(entity, verifier):

    refresh_adapters()

    if entity["att_tech"] in classes.keys():
        if hasattr(classes[entity["att_tech"]], 'delete') and callable(getattr(classes[entity["att_tech"]], 'delete')):
            classes[entity["att_tech"]].delete(entity, verifier)
        else:
            return {"error" : "no delete() method found for " + entity["att_tech"] + " adapter"} 
    else:
        return {"error" : "no adapter found for attestation technology " + entity["att_tech"] }

def status(verifier):

    refresh_adapters()

    if verifier["att_tech"] in classes.keys():
        if hasattr(classes[verifier["att_tech"]], 'status') and callable(getattr(classes[verifier["att_tech"]], 'status')):
            classes[verifier["att_tech"]].status(verifier)
        else:
            return {"error" : "no status() method found for " + verifier["att_tech"] + " adapter"} 
    else:
        return {"error" : "no adapter found for attestation technology " + verifier["att_tech"] }