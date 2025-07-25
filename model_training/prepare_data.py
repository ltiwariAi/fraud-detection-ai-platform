import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load feature-engineered CSV
df = pd.read_csv('data/processed/feature_engineered_transactions.csv')

# Drop irrelevant columns (or keep if you want to encode later)
df = df.drop(columns=['transaction_id', 'timestamp', 'merchant', 'location', 'device', 'customer_id'], errors='ignore')

# Separate features and target
X = df.drop(columns=['is_fraud'])
y = df['is_fraud']

# One-hot encode categorical variables if any
X = pd.get_dummies(X)

# Split into train/test sets with stratified sampling (keep fraud distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# Scale features (mean=0, std=1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the preprocessed data for later use
import numpy as np
import os

os.makedirs('data/processed', exist_ok=True)
np.save('data/processed/X_train.npy', X_train_scaled)
np.save('data/processed/X_test.npy', X_test_scaled)
np.save('data/processed/y_train.npy', y_train.to_numpy())
np.save('data/processed/y_test.npy', y_test.to_numpy())

# Save scaler to disk for inference pipeline
joblib.dump(scaler, 'models/scaler.save')

print("Data preparation completed and saved.")
