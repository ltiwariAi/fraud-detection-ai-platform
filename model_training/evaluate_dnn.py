import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix

# Load test data and model
X_test = np.load('data/processed/X_test.npy')
y_test = np.load('data/processed/y_test.npy')
model = load_model('models/fraud_model_dnn.keras')

# Predict probabilities and threshold at 0.5
y_pred_probs = model.predict(X_test)
y_pred = (y_pred_probs > 0.5).astype(int)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
