from kafka import KafkaConsumer
import json

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'transactions'

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detection-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Starting transaction consumer...")
for message in consumer:
    txn = message.value
    print(f"Consumed: {txn}")
