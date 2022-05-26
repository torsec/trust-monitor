import configparser
import json
from confluent_kafka import Consumer, Producer

config = configparser.ConfigParser()
config.read('config.ini')


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def run_kafka_consumer():
    properties = {}
    for property in config["kafka_consumer"].keys():
        properties[property] = config["kafka_consumer"][property]

    kafka_consumer = Consumer(properties)

    topics = [config["kafka_topics"]["attestation_result_topic"]]
    kafka_consumer.subscribe(topics)

    while True:
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
        
        print("Message value: %s", msg.value().decode('utf-8'))


def run_kafka_producer(message):
    properties = {}
    for property in config["kafka_producer"].keys():
        properties[property] = config["kafka_producer"][property]

    kafka_producer = Producer(properties)

    kafka_producer.produce(config["kafka_topics"]["attestation_result_topic"], json.dumps(message) ,callback=delivery_report)

    kafka_producer.flush()

#run_kafka_consumer()
#run_kafka_producer({"key0" : "value0"})