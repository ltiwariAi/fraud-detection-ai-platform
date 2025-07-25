# ml_pipeline/train_xgboost_model.py

import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from pathlib import Path

# Load train/test data
X_train = pd.read_csv("data/processed/X_train.csv")
X_test = pd.read_csv("data/processed/X_test.csv")
y_train = pd.read_csv("data/processed/y_train.csv").squeeze()  # to convert DataFrame → Series
y_test = pd.read_csv("data/processed/y_test.csv").squeeze()

# --- Handle class imbalance: fraud cases are rare
# You can dynamically calculate imbalance ratio if needed:
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# --- Train XGBoost Model
model = XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)
model.fit(X_train, y_train)

# --- Predict and Evaluate
y_pred = model.predict(X_test)

print("\n✅ Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred, digits=4))

# --- Save trained model
Path("models/").mkdir(parents=True, exist_ok=True)
joblib.dump(model, "models/fraud_model_xgb.pkl")

print("\n🎉 Model training complete. Model saved to: models/fraud_model_xgb.pkl")
