import configparser
import threading
from database_connectors.instances import (retrieve_entity, retrieve_all_entities, store_entity, purge_entity, edit_entity, edit_state_entity)
from database_connectors.verifiers import (store_verifier, purge_verifier, retrieve_verifier, retrieve_all_verifiers)
from database_connectors.whitelists import (purge_whitelist, store_whitelist, retrieve_whitelist)
from database_connectors.policies import (store_policy, purge_policy, retrieve_policy)
from database_connectors.reports import (store_report, retrieve_reports)
from adapters_connector import (register_entity, verify_entity)
from kafka_connector.kafka_connector import (run_kafka_consumer, new_topic, remove_topic)
import time
import importlib

config = configparser.ConfigParser()
config.read('config/config.ini')

REGISTERED_STATUS = "registered"
ATTESTING_STATUS = "attesting"

#consumers = {}
tm_status = {
    "att_processes": []
}
tm_status_lock = threading.Lock()

threads = {}
t_lock = threading.Lock()

def insert_entity(entity):
    """
    Store the new entity in the instances database
    """
    
    ret = store_entity(entity)

    if "error" in entity.keys() or "error_value" in entity.keys():
        return ret

    edit_state_entity( {"state": REGISTERED_STATUS, "entity_uuid": entity["entity_uuid"]} )
    
    """
    Register entity for every attestation technology
    """
    whitelist = None   
    if "whitelist_uuid" in entity.keys():
        whitelist = retrieve_whitelist({ "_id": entity["whitelist_uuid"] })  # get the whitelist for the specified entity
    
    for tech in entity["att_tech"]:
        verifier = retrieve_verifier( {"att_tech": tech, "inf_id": entity["inf_id"]} )
        #print(verifier["att_tech"])
        register_entity(entity, whitelist, verifier) # we pass the same whitelist for all technologies

    return ret

def read_entity(entity):
    """
    Read an entity or the whole list in the instances database
    """
    if entity["entity_uuid"] is None:
        ret = retrieve_all_entities()
    else:
        ret = retrieve_entity(entity)

    return ret

def update_entity(entity):
    """
    Update an entity in the instances database
    """
    ret = edit_entity(entity)

    return ret

def start_attestation(entity):
    """
    Start the attestation process for the specified entity
    """
    if entity["entity_uuid"] in threads:
        return {"error": "attestation process already started for entity_uuid " + str(entity["entity_uuid"])} # 409

    try:
        se = threading.Event()
        t = threading.Thread(target=attest_entity, args=[entity, se])
        #t = threading.Thread(target=test, args=[body, se])
        
        t.start()
        time.sleep(1) # wait the thread has the time to start
        
        if not t.is_alive():
            #
            # si potrebbe aggiungere piu di un tentativo di far partire il thread
            #
            return {"error": "entity " + str(entity["entity_uuid"]) + " - attestation thread failed to start"}
    
        t_lock.acquire()
        threads[entity["entity_uuid"]] = { "thread": t, "stop_event": se }
        t_lock.release()

        return {"message": "entity " + str(entity["entity_uuid"]) + " - attestation thread started successfully"}

    except Exception as error:
        t_lock.release()
        return {"error": error.__str__()}

def stop_attestation(entity):
    """
    Stop the attestation process for the specified entity
    """
    if entity["entity_uuid"] not in threads:
        return {"error": "there is no attestation process for entity_uuid " + str(entity["entity_uuid"])} # 422

    try:
        threads[entity["entity_uuid"]]["stop_event"].set()
        threads[entity["entity_uuid"]]["thread"].join()
        if entity["entity_uuid"] in threads:
            t_lock.acquire()
            del threads[entity["entity_uuid"]]
            t_lock.release()

        return {"message": "entity " + str(entity["entity_uuid"]) + " - attestation stopped successfully"}

    except Exception as error:
        t_lock.release()
        return {"error": error.__str__()}, 500

def attest_entity(entity_, se):
    """
    Prameters:
        - entity_ = entity object containing just the entity_uuid
        - se = stop event for the verify thread
    """
    t_attestation = []
    topic = ""          # topic created for each attestation process


    #startTime = time.time()
        

    entity = retrieve_entity(entity_)
    if "error" in entity:
        return entity

    if entity["whitelist_uuid"] is None:
        print({"error": "no whitelist_uuid specified for the entity " + entity["entity_uuid"]})
        return {"error": "no whitelist_uuid specified for the entity " + entity["entity_uuid"]}
    whitelist = retrieve_whitelist({ "_id": entity["whitelist_uuid"] })  # get the whitelist for the specified entity

    if entity["att_tech"] is None or entity["att_tech"] is []:
        print({"error": "no attestation technologies specified for the entity " + entity["entity_uuid"]})
        return {"error": "no attestation technologies specified for the entity " + entity["entity_uuid"]}

    #
    # start the attestation results' consumer
    #
    try:
        # create a new topic for the entity
        topic = config["kafka_topics"]["attestation_result_topic"] + "_entity_" + str(entity["entity_uuid"])
        #print("PRIMA creazione topic")
        new_topic(topic)
        #print("DOPO creazione topic")
    except Exception as error:
        print({"error": error.__str__()})
        return {"error": error.__str__()}

    try:
        stop_event = threading.Event()  # stop event for kafka consumer

        kafka_consumer_thread = threading.Thread(target=run_kafka_consumer, args=[stop_event, entity, [topic]])
        kafka_consumer_thread.start()
    except Exception as error:
        if entity["entity_uuid"] in threads:
            t_lock.acquire()
            del threads[entity["entity_uuid"]]
            t_lock.release()

        remove_topic(topic)
        print({"error": error.__str__()})
        return {"error": error.__str__()}

    #
    # start a thread for each attestation technology
    #
    for tech in entity["att_tech"]:
        verifier = retrieve_verifier({ "att_tech": tech, "inf_id": entity["inf_id"] })
        if 'error' in verifier:
            remove_topic(topic)
            print({"error": verifier['error']})
            return {"error": verifier['error']}
        t_entity = threading.Thread(target=verify_entity, args=[entity, verifier, whitelist, se, topic])

        t_attestation.append(t_entity)
    try:
        for t in t_attestation:
            t.start()
    except Exception as error:
        if entity["entity_uuid"] in threads:
            t_lock.acquire()
            del threads[entity["entity_uuid"]]
            t_lock.release()

        se.set()
        stop_event.set()
        kafka_consumer_thread.join()
        remove_topic(topic)
        return {"error": error.__str__()}

    edit_state_entity( {"entity_uuid": entity["entity_uuid"], "state": ATTESTING_STATUS} )

    tm_status_lock.acquire()
    tm_status["att_processes"].append(
        {
            "entity_uuid": entity["entity_uuid"],
            "name": entity["name"],
            "external_id": entity["external_id"],
            "att_tech": entity["att_tech"]
        }
    )
    tm_status_lock.release()

    #executionTime = (time.time() - startTime)
    #print("EXECUTION TIME: " + str(executionTime) + " s")

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

    edit_state_entity( {"entity_uuid": entity["entity_uuid"], "state": REGISTERED_STATUS} )

    tm_status_lock.acquire()
    for i in range(len(tm_status["att_processes"])):
        if tm_status["att_processes"][i]["entity_uuid"] == entity["entity_uuid"]:
            del tm_status["att_processes"][i]
            break
    tm_status_lock.release()

    try:
        if entity["entity_uuid"] in threads:
            t_lock.acquire()
            del threads[entity["entity_uuid"]]
            t_lock.release()

        remove_topic(topic)
    except Exception as error:
        return {"error": error.__str__()}


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

def retrieve_all_att_tech():
    """
    Read all verifiers in the attestation technologies database
    """
    ret = retrieve_all_verifiers()

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

def read_tm_status():
    """
    read the TM status
    """
    config.read('config/config.ini')

    classes = []
    for module in config["adapters"].keys():
        class_ = config["adapters"][module]
        #try:
        val = getattr(importlib.import_module("."+module, "adapters"), class_) #__import__("adapters."+module, fromlist=[module]), class_
        classes.append(module)
        #except:
            #print("Adapter " + module + " NOT found!")
    
    tm_status_lock.acquire()
    tmp = tm_status
    tm_status_lock.release()

    tmp["adapters_loaded"] = classes

    return tmp

def read_report(request):
    """
    read from db reports for a specific entity
    """
    ret = retrieve_reports(request)

    return ret

def insert_report(report):
    """
    save a report into the db
    """
    ret = store_report(report)

    return ret