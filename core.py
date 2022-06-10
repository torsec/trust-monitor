import configparser
import threading
from database_connectors.instances import (retrieve_entity, store_entity, purge_entity, edit_entity)
from database_connectors.verifiers import (store_verifier, purge_verifier, retrieve_verifier)
from database_connectors.whitelists import (purge_whitelist, store_whitelist, retrieve_whitelist)
from database_connectors.policies import (store_policy, purge_policy, retrieve_policy)
from adapters_connector import (register_entity, verify_entity)
from kafka_connector.kafka_connector import run_kafka_consumer

config = configparser.ConfigParser()
config.read('config.ini')

consumers = {}

def insert_entity(entity):
    """
    Store the new entity in the instances database
    """
    ret = store_entity(entity)

    if "error" in entity.keys() or "error_value" in entity.keys():
        return ret

    """
    Register entity for every attestation technology
    """
    whitelist = None   
    if entity["whitelist_uuid"] is not None:
        whitelist = retrieve_whitelist({ "_id": entity["whitelist_uuid"] })  # get the whitelist for the specified entity
    
    for tech in entity["att_tech"]:
        verifier = retrieve_verifier(tech)
        #print(verifier["att_tech"])
        register_entity(entity, whitelist, verifier) # we pass the same whitelist for all technologies

    return ret

def read_entity(entity):
    """
    Read an entity in the instances database
    """
    ret = retrieve_entity(entity)

    return ret

def update_entity(entity):
    """
    Update an entity in the instances database
    """
    ret = edit_entity(entity)

    return ret


def attest_entity(entity_, se):
    """
    Prameters:
        - entity_ = entity object containing all information about the object
        - se = stop event for the verify thread
    """
    t_attestation = []

    entity = retrieve_entity(entity_)
    if "error" in entity:
        return entity

    if entity["whitelist_uuid"] is None:
        return {"error": "no whitelist_uuid specified for the entity " + entity["entity_uuid"]}
    whitelist = retrieve_whitelist({ "_id": entity["whitelist_uuid"] })  # get the whitelist for the specified entity

    #return

    stop_event = threading.Event()  # stop event for kafka consumer
    kafka_consumer_thread = threading.Thread(target=run_kafka_consumer, args=[stop_event, entity, [config["kafka_topics"]["attestation_result_topic"]]])
    kafka_consumer_thread.start()

    if "att_tech" in entity.keys():
        for tech in entity["att_tech"]:
            verifier = retrieve_verifier({ "att_tech": tech })
            t_entity = threading.Thread(target=verify_entity, args=[entity, verifier, whitelist, se])

            t_attestation.append(t_entity)

        for t in t_attestation:
            t.start()
        #
        # wait untill all verifiers stop the attestation
        #
        for t in t_attestation:
            t.join()
    #
    # stop the consumer
    #
    stop_event.set()
    kafka_consumer_thread.join()  

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

def retrieve_att_tech(verifier):

    """
    Read a verifier in the attestation technologies database
    """
    ret = retrieve_verifier(verifier)

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

def read_whitelist(whitelist):

    """
    Read a whitelist in the whitelists database
    """
    ret = retrieve_whitelist(whitelist)

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

def read_policy(policy):

    """
    read a policy for an entity in the policy database
    """
    ret = retrieve_policy(policy)

    return ret

def delete_policy(policy):

    """
    Delete a policy for an entity from the policy database
    """
    ret = purge_policy(policy)

    return ret