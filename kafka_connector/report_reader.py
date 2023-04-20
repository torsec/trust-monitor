from confluent_kafka import Consumer
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

def consumer():
    properties = {}
    for property in config["kafka_consumer"].keys():
        properties[property] = config["kafka_consumer"][property]

    kafka_consumer = Consumer(properties)

    topics = [config["kafka_topics"]["attestation_report_topic"]]
    kafka_consumer.subscribe(topics)

    print("Start consuming reports...")
    
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

        str = msg.value().decode('utf-8')
        print("Message value: %s", str)


if __name__ == "__main__":

    consumer()