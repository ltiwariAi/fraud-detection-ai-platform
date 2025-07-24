import json
import random
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

# Kafka config
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'transactions'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample merchants and locations
MERCHANTS = ['Amazon', 'Walmart', 'Starbucks', 'Apple Store', 'Target']
LOCATIONS = ['New York', 'San Francisco', 'Chicago', 'Houston', 'Seattle']

def generate_transaction():
    return {
        'transaction_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat(),
        'amount': round(random.uniform(1.0, 2000.0), 2),
        'merchant': random.choice(MERCHANTS),
        'location': random.choice(LOCATIONS),
        'device': random.choice(['mobile', 'web', 'POS']),
        'customer_id': str(random.randint(1000, 9999)),
        'is_fraud': random.choices([0,1], weights=[0.98,0.02])[0]  # 2% fraud rate
    }

def produce_transactions(rate_per_sec=5):
    print(f"Starting transaction stream at {rate_per_sec} txn/sec...")
    while True:
        txn = generate_transaction()
        producer.send(TOPIC, txn)
        print(f"Produced: {txn}")
        time.sleep(1.0 / rate_per_sec)

if __name__ == "__main__":
    produce_transactions()
