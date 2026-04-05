# Fraud Detection Dashboard

A Machine Learning web application that detects **fraudulent financial transactions** in real time using a trained classification model and an interactive dashboard.

---

## 📌 Project Overview

This project predicts whether a transaction is **Fraudulent** or **Safe** based on transaction details such as amount, balances, and transaction type.

The application allows users to:

- Enter transaction details
- Get fraud prediction instantly
- View fraud probability
- Understand fraud reasoning
- Track past transaction history

---

## Machine Learning Workflow

### Data Preprocessing
- Handled missing values
- Feature engineering
- One-Hot Encoding for transaction types
- Balance consistency validation

### Model Training
A classification model trained on financial transaction data to learn fraud behaviour patterns such as:

- Large transaction amounts
- Sudden balance mismatches
- Suspicious transfer types
- Inactive destination accounts

### Model Deployment
- Model saved using **Joblib**
- Integrated with Flask backend
- Real-time prediction through web interface

---

## Dashboard Features

### Transaction Input
Users provide:

- Transaction Step (Time)
- Transaction Type
- Amount
- Sender Old Balance
- Sender New Balance
- Receiver Old Balance
- Receiver New Balance

---

### Prediction Output
Dashboard displays:

- Fraud / Safe Status
- Fraud Probability Score
- Fraud Risk Insights
- Transaction History

---

## Tech Stack

| Category | Tools |
|---|---|
| Backend | Flask |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Frontend | HTML, CSS |
| Deployment | Render |
| Model Storage | Joblib |

Live on: https://automated-fraud-detection-system-1.onrender.com
