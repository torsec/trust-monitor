import configparser
import json
from confluent_kafka import Consumer, Producer
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def run_kafka_consumer(stop_event, entity, topics):
    properties = {}
    for property in config["kafka_consumer"].keys():
        properties[property] = config["kafka_consumer"][property]

    kafka_consumer = Consumer(properties)

    #topics = [config["kafka_topics"]["attestation_result_topic"]]
    kafka_consumer.subscribe(topics)

    report = {
        "entity_uuid": entity["entity_uuid"],
        "trust": True,
        "state": []
    }

    while not stop_event.is_set():
        msg = kafka_consumer.poll(1.0) # every second check if there is some message

        if msg is None:
            print("No message found!")
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        if msg.topic() is None:
            print("Received message has None topic")
            continue

        _str = msg.value().decode('utf-8')
        print("Message value: %s", _str)
        result = json.loads(_str)
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

            run_kafka_producer(report, config["kafka_topics"]["attestation_report_topic"])
            report["state"] = []

def run_kafka_producer(message, topic):
    """
    message -> json object
    """
    properties = {}
    for property in config["kafka_producer"].keys():
        properties[property] = config["kafka_producer"][property]

    kafka_producer = Producer(properties)

    kafka_producer.produce(topic, json.dumps(message) ,callback=delivery_report)

    kafka_producer.flush()
