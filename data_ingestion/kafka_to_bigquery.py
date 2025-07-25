from kafka import KafkaConsumer
from google.cloud import bigquery
import json
from datetime import datetime

# Constants
PROJECT_ID = 'fraud-detection-ai-466902'
DATASET_ID = 'fraud_data'
TABLE_ID = 'transactions_stream'
TOPIC = 'transactions'
KAFKA_BROKER = 'localhost:9092'

# Init BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Init Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='bq-ingestor',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening to Kafka topic and writing to BigQuery...")

for message in consumer:
    txn = message.value

    # Convert timestamp string to datetime object
    txn["timestamp"] = datetime.strptime(txn["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")

    row = [{
        "transaction_id": txn["transaction_id"],
        "timestamp": txn["timestamp"].isoformat(),  # Convert to ISO format for BigQuery - LT
        "amount": txn["amount"],
        "merchant": txn["merchant"],
        "location": txn["location"],
        "device": txn["device"],
        "customer_id": txn["customer_id"],
         "is_fraud": txn["is_fraud"] in [1, "1", True, "true", "True"] # Ensure is_fraud is boolean - LT
    }]

    errors = client.insert_rows_json(f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", row)

    if not errors:
        print(f"✅ Inserted: {txn['transaction_id']}")
    else:
        print(f"❌ Errors: {errors}")
