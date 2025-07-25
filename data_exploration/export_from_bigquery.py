from google.cloud import bigquery
import pandas as pd

# Replace with your project ID
client = bigquery.Client(project='fraud-detection-ai-466902')

query = """
SELECT * 
FROM `fraud-detection-ai-466902.fraud_data.transactions_stream`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
"""

df = client.query(query).to_dataframe()

# Save for backup or exploratory analysis
df.to_csv('data/raw/raw_transactions.csv', index=False)
