from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load the trained model
model = joblib.load('models/fraud_model_xgb.pkl')

# Add the missing 'amount' feature here (change #1)
class TransactionFeatures(BaseModel):
    amount: float                      # <-- Added this line
    hour_of_day: int
    day_of_week: int
    is_weekend: int        # Use 0 or 1
    amount_bin_low: int    # One-hot encoded amount bin features
    amount_bin_medium: int
    amount_bin_high: int
    location_device_mismatch: int
    customer_txn_count_24h: float
    avg_amount_24h: float
    # merchant_risk_score: float

@app.post("/predict")
def predict_fraud(features: TransactionFeatures):
    # Convert input features to dict
    feature_dict = features.dict()

    # Ensure columns are ordered exactly as the model expects (change #2)
    expected_order = [
        'amount', 'hour_of_day', 'day_of_week', 'is_weekend', 
        'location_device_mismatch', 'customer_txn_count_24h', 'avg_amount_24h', 
        'amount_bin_high', 'amount_bin_low', 'amount_bin_medium'
    ]

    # Create DataFrame in expected order
    input_data = pd.DataFrame([{k: feature_dict[k] for k in expected_order}])

    # Predict fraud label
    pred_label = model.predict(input_data)[0]

    # Predict fraud probability (probability of class 1)
    pred_prob = model.predict_proba(input_data)[:, 1][0]

    return {
        "fraud_prediction": int(pred_label),
        "fraud_probability": float(pred_prob)
    }

# Run with: uvicorn app:app --reload
