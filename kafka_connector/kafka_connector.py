import configparser
from confluent_kafka import Consumer

config = configparser.ConfigParser()
config.read('config.ini')


def run_kafka_consumer():
    kafka_consumer = Consumer(
        {
            "bootstrap.servers": config["kafka_consumer"]["bootstrap.servers"],
            "group.id": config["kafka_consumer"]["group.id"]
        }
    )

    kafka_consumer.subscribe([config["kafka_consumer"]["attestation_result_topic"]])

    while True:
        msg = kafka_consumer.poll(1.0)
            
        if msg is None:
            print("No message found!")
            continue
        if msg.error():
            #app.logger.info("Consumer error: {}".format(msg.error()))
            print("Consumer error: {}".format(msg.error()))
            continue
        if msg.topic() is None:
            print("Received message has None topic")
            continue
        
        #app.logger.info("Received message: {}".format(msg.value()))
        print("Message value: %s", msg.value().decode('utf-8'))