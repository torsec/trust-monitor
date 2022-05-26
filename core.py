from database_connectors.instances import (store_entity,purge_entity)
from database_connectors.verifiers import (store_verifier,purge_verifier,retreive_verifier)
from database_connectors.whitelists import (purge_whitelist,store_whitelist,retreive_whitelist)
from database_connectors.policies import (store_policy,purge_policy)
from adapters_connector import (register_entity)


def insert_entity(entity):

    """
    Store the new entity in the instances database
    """
    ret = store_entity(entity)

    """
    Register entity for every attestation technology
    """
    if "att_tech" in entity.keys():
        whitelist = retreive_whitelist(entity["whitelist_uuid"])  #get the whitelist for the specified entity
        for tech in entity["att_tech"]:
            verifier = retreive_verifier(tech)
            print(verifier["att_tech"])
            #register_entity(entity, whitelist, verifier)

    return ret

def attest_entity(entity):

    if "att_tech" in entity.keys():
        for tech in entity["att_tech"]:
            pass

    return

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

    """
    Delete a verifier from the attetstation technologies database
    """
    ret = purge_verifier(verifier)

    return ret

def insert_whitelist(whitelist):

    """
    Store the new whitelist in the whitelists database
    """
    ret = store_whitelist(whitelist)

    return ret

def delete_whitelist(whitelist):

    """
    Delete a whitelist from the whitelists database
    """
    ret = purge_whitelist(whitelist)

    return ret

def insert_policy(policy):

    """
    Store the new policy for an entity in the policy database
    """
    ret = store_policy(policy)

    return ret

def delete_policy(policy):

    """
    Delete a policy for an entity from the policy database
    """
    ret = purge_policy(policy)

    return ret