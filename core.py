from importlib.metadata import entry_points
from database_connectors.instances import store_entity,purge_entity
from database_connectors.verifiers import store_verifier
from adapters_connector import register_entity
from database_connectors.whitelists import store_whitelist

def insert_entity(entity):

    """
    Store the new entity in the instances database
    """
    ret = store_entity(entity)

    """
    Register entity for every attestation technology
    """
    if "att_tech" in entity.keys():
        register_entity(entity)

    return ret

def delete_entity(entity):

    ret = purge_entity(entity)

    return ret

def insert_att_tech(verifier):

    ret = store_verifier(verifier)

    return ret

def insert_whitelist(whitelist):

    ret = store_whitelist(whitelist)

    return ret