from importlib.metadata import entry_points
from database_connectors.instances import store_entity
from database_connectors.verifiers import store_verifier
from adapters_connector import register_entity

def insert_entity(entity):

    """
    Store the new entity in the instances database
    """
    store_entity(entity)

    """
    Register entity for every attestation technology
    """
    if "att_tech" in entity.keys():
        register_entity(entity)

    return

def delete_entity():
    return

def store_att_tech(verifier):

    store_verifier(verifier)

    return