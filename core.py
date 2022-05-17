from importlib.metadata import entry_points
from database_connectors.instances import (
    store_entity,
    purge_entity
)
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

    """
    Delete an entity from the instances database
    """
    ret = purge_entity(entity)

    return ret

def insert_att_tech(verifier):

    """
    Store the new verifier in the attestation technologies database
    """
    ret = store_verifier(verifier)

    return ret

def delete_att_tech(verifier):

    return

def insert_whitelist(whitelist):

    """
    Store the new whitelist in the whitelists database
    """
    ret = store_whitelist(whitelist)

    return ret