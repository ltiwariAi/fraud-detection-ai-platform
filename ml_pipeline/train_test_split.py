# ml_pipeline/train_test_split.py

import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# Load feature data
FEATURE_PATH = Path("data/processed/engineered_features.csv")
df = pd.read_csv(FEATURE_PATH)

# --- Drop non-numeric and identifier columns
drop_cols = ['transaction_id', 'timestamp', 'merchant', 'location', 'device', 'customer_id']
df_model = df.drop(columns=[col for col in drop_cols if col in df.columns])

# --- One-hot encode categorical features
df_model = pd.get_dummies(df_model)

# --- Separate features and target
X = df_model.drop(columns=['is_fraud'])
y = df_model['is_fraud']

# --- Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# --- Save splits (optional for reuse)
Path("data/processed/").mkdir(parents=True, exist_ok=True)
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
y_train.to_csv("data/processed/y_train.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

print("✅ Train-test split complete.")
print(f"Training samples: {X_train.shape[0]} | Test samples: {X_test.shape[0]}")
