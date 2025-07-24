# 🛡️ Fraud Detection AI Platform

A real-time fraud detection system built for BFSI (Banking, Financial Services, Insurance) using GCP, Apache Kafka, BigQuery, Dataflow, and Machine Learning models (XGBoost, Deep Learning).

---

## 📌 Project Overview

This platform ingests real-time transaction data, extracts fraud-relevant features, applies trained ML models, and generates alerts. The system is modular, scalable, and integrates with GCP services like Vertex AI, BigQuery, and Looker Studio.

---

## 🧱 Architecture Overview

- **Data Ingestion**: Apache Kafka / GCP Pub/Sub
- **Streaming ETL**: Dataflow / Apache Beam
- **Storage**: BigQuery
- **Feature Engineering**: Pandas, Beam
- **Modeling**: XGBoost, TensorFlow (Keras)
- **Serving**: FastAPI (local), Vertex AI (cloud)
- **MLOps**: Vertex AI Pipelines, TFX, Docker, CI/CD
- **Alerting**: BigQuery triggers, LangChain GenAI summaries
- **Visualization**: Looker Studio, Streamlit

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ltiwariAi/fraud-detection-ai-platform.git
cd fraud-detection-ai-platform
