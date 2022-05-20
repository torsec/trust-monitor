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
    for tech in classes.keys():
        if tech == entity["att_tech"]:
            classes[tech].register()
    return

def delete_entity(entity):
    for tech in classes.keys():
        if tech == entity["att_tech"]:
            classes[tech].delete()
    return

def status(att_tech):
    for tech in classes.keys():
        if tech == att_tech:
            classes[tech].status()
    return