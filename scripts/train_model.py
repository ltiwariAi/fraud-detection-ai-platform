import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def main():
    # Create dummy data
    data = {
        'amount': [100, 200, 300, 400, 500, 600],
        'is_fraud': [0, 0, 0, 1, 1, 1]
    }
    df = pd.DataFrame(data)

    X = df[['amount']]
    y = df['is_fraud']

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    joblib.dump(model, 'models/fraud_model_xgb.pkl')
    

if __name__ == '__main__':
    main()
