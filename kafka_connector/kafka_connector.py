import configparser
import json
import sys
#from time import sleep
from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from datetime import datetime
import core
import requests

config = configparser.ConfigParser()
config.read('config/config.ini')
#print(config["kafka_producer"]["bootstrap.servers"])
admin = AdminClient({'bootstrap.servers': config["kafka_producer"]["bootstrap.servers"]})

def new_topic(topic):
    """
    topic (string): name of the topic
    """
    #print(admin.list_topics().topics)
    fs = admin.create_topics( [NewTopic(topic, num_partitions=3, replication_factor=1)] )

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            raise Exception("Failed to create topic {}: {}".format(topic, e))


def remove_topic(topic):
    """
    topic (string): name of the topic
    """
    fs = admin.delete_topics( [topic] , operation_timeout=30)

    # Wait for operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except Exception as e:
            raise Exception("Failed to delete topic {}: {}".format(topic, e))


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err), file=sys.stderr)
    # else:
        # print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def run_kafka_consumer(stop_event, entity, topics):
    properties = {}
    for property in config["kafka_consumer"].keys():
        properties[property] = config["kafka_consumer"][property]
    print(properties)
    kafka_consumer = Consumer(properties)

    #topics = [config["kafka_topics"]["attestation_result_topic"]]
    kafka_consumer.subscribe(topics)

    report = {
        "pilot": "SADE",
        "entity_uuid": entity["entity_uuid"],
        "trust": False,
        "state": []
    }

    msg = None

    while not stop_event.is_set() or msg is not None:
        msg = kafka_consumer.poll(5) # every 5 seconds check if there is some message

        if msg is None:
            #print("No message found!")
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        if msg.topic() is None:
            print("Received message has None topic")
            continue

        _str = msg.value().decode('utf-8')
        # print("Message value: %s", _str)
        result = json.loads(_str)

        #if result["entity_uuid"] != report["entity_uuid"]:
        #    continue

        key_list = map(lambda x: x["att_tech"], report["state"])

        #
        # update the result, in the report, if it's already present
        #
        if result["att_tech"] in key_list:
            for i in range(len(report["state"])):
                if report["state"][i]["att_tech"] == result["att_tech"]:
                    del report["state"][i]
                    report["state"].append(
                        {
                            "att_tech": result["att_tech"],
                            "trust": result["trust"]
                        }
                    )
                    break
        else:
            #
            # add the result, in the report, if it's NOT present
            #
            report["state"].append(
                        {
                            "att_tech": result["att_tech"],
                            "trust": result["trust"]
                        }
                    )

        #
        # build the report if it's possible, and clear the report state
        #
        if len(report["state"]) == len(entity["att_tech"]):

            report["time"] = str(datetime.now())

            for res in report["state"]:
                if res["trust"] == False:
                    report["trust"] = False
                    break
                else:
                    report["trust"] = True
            #
            # POST on the SPI DM
            #
            requests.post("https://" + config["spi-dm"]["address"] + ":" + config["spi-dm"]["port"] + "/api/normalize/trustmonitor",
                          json=report,
                          verify=False
            )
            #run_kafka_producer(report, config["kafka_topics"]["attestation_report_topic"])
            ret = core.insert_report(report)   # store the report in the DB
            #print(ret)
            report["state"] = []
            
            if '_id' in report.keys():  # remove '_id' attribute added after the insert_report
                del report["_id"]

def run_kafka_producer(message, topic):
    """
    message -> json object
    """
    properties = {}
    for property in config["kafka_producer"].keys():
        properties[property] = config["kafka_producer"][property]
    #print(properties)
    kafka_producer = Producer(properties)
    # print(message)
    kafka_producer.produce(topic, json.dumps(message) ,callback=delivery_report)

    kafka_producer.flush()