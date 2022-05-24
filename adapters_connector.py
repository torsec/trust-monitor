import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Import all adapters (the name of the att_tech attribute of an entity must match the name of one of the adapters' scripts)
# Adapters must be specified in the config.ini file:
# [adapters]
# file_name = class_name
classes = {}
for module in config["adapters"].keys():
    class_ = config["adapters"][module]
    classes[module] = getattr(__import__("adapters."+module, fromlist=[module]), class_)


def register_entity(entity):
    if entity["att_tech"] in classes.keys():
        classes[entity["att_tech"]].register()
    else:
        return {"error" : "no adapter found for attestation technology " + entity["att_tech"] }

def delete_entity(entity):
    if entity["att_tech"] in classes.keys():
        classes[entity["att_tech"]].delete()
    else:
        return {"error" : "no adapter found for attestation technology " + entity["att_tech"] }

def status(att_tech):
    if att_tech in classes.keys():
        classes[att_tech].status()
    else:
        return {"error" : "no adapter found for attestation technology " + att_tech }