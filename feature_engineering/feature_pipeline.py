# feature_engineering/feature_pipeline.py

import pandas as pd
import numpy as np
from pathlib import Path

# Load raw data
RAW_DATA_PATH = Path("data/raw/raw_transactions.csv")
df = pd.read_csv(RAW_DATA_PATH)

# Ensure timestamp is datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- Basic time-based features
df['hour_of_day'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6])

# --- Amount binning
df['amount_bin'] = pd.cut(df['amount'],
                          bins=[0, 100, 500, 5000],
                          labels=['low', 'medium', 'high'])

# --- Location/Device mismatch (example logic)
def location_device_mismatch(row):
    return row['device'] == 'POS' and row['location'] == 'remote'

df['location_device_mismatch'] = df.apply(location_device_mismatch, axis=1)

# --- Simulated rolling features (simplified here)
df['customer_txn_count_24h'] = df.groupby('customer_id')['timestamp'].transform('count')
df['avg_amount_24h'] = df.groupby('customer_id')['amount'].transform('mean')

# --- Clean & Save
FEATURE_DATA_PATH = Path("data/processed/engineered_features.csv")
FEATURE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(FEATURE_DATA_PATH, index=False)

print(f"✅ Feature engineering complete. Output saved to: {FEATURE_DATA_PATH}")
