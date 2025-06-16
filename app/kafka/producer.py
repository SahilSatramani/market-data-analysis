from confluent_kafka import Producer
import json
import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def publish_price_event(event: dict, topic: str = "price-events"):
    try:
        producer.produce(
            topic=topic,
            key=event.get("symbol"),
            value=json.dumps(event),
            callback=delivery_report,
        )
        producer.flush()
    except Exception as e:
        print(f"Kafka publish error: {e}")
