from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

fraud_model = joblib.load("fraud_model.pkl")

TRANSACTION_CATEGORIES = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    probability = None
    safe_prob = None
    fraud_prob = None
    status_class = None
    reasons = []
    updated = pd.DataFrame()

    if request.method == "POST":
        try:
            # Inputs
            amount = float(request.form.get("amount"))
            step = float(request.form.get("step"))
            oldbalance_org = float(request.form.get("oldbalanceOrg"))
            newbalance_org = float(request.form.get("newbalanceOrig"))
            oldbalance_dest = float(request.form.get("oldbalanceDest"))
            newbalance_dest = float(request.form.get("newbalanceDest"))
            selected_type = request.form.get("type")

            # One-hot encoding
            encoded_type = [1 if selected_type == t else 0 for t in TRANSACTION_CATEGORIES]

            # Model input
            model_input = np.array([[
                amount,
                step,
                oldbalance_org,
                newbalance_org,
                oldbalance_dest,
                newbalance_dest,
                *encoded_type
            ]])

            # Prediction
            prediction_score = fraud_model.predict(model_input)[0]

            probs= fraud_model.predict_proba(model_input)[0]
            fraud_index = list(fraud_model.classes_).index(1)

            fraud_prob = round(probs[fraud_index] * 100, 2)
            safe_prob = round(100 - fraud_prob, 2)

            probability = fraud_prob
            
            if prediction_score == 1:
                result = "Fraud Detected"
                status_class = "fraud"
            else:
                result = "Transaction Safe"
                status_class = "safe"

            # print("Prediction Score:", prediction_score)

            print("Classes:", fraud_model.classes_)
            print("Prediction:", prediction_score)
            print("Probabilities:", probs)
            print("Fraud Prob:", fraud_prob)

            # Fraud Insights
            if amount > 200000:
                reasons.append("High transaction amount")

            if oldbalance_org - amount != newbalance_org:
                reasons.append("Balance mismatch detected")

            if selected_type in ["TRANSFER", "CASH_OUT"]:
                reasons.append("High-risk transaction type")

            if oldbalance_dest == 0:
                reasons.append("Receiver account inactive")

            # Save history
            history_file = "history.csv"

            new_data = pd.DataFrame([{
                "Amount": amount,
                "Type": selected_type,
                "Prediction": result,
                "Confidence": fraud_prob
            }])

            try:
                old = pd.read_csv(history_file)
                updated = pd.concat([old, new_data])
            except:
                updated = new_data

            updated.to_csv(history_file, index=False)

        except Exception as e:
            result = "Invalid Input Data"
            status_class = "error"
            print(e)

    return render_template(
        "index.html",
        result=result,
        probability=probability,
        safe_prob=safe_prob,
        reasons=reasons,
        tables=updated.tail().to_html(classes='table'),
        status_class=status_class
    )

@app.route("/history")
def history():
    try:
        df = pd.read_csv("history.csv")
    except:
        df = pd.DataFrame()

    return render_template("history.html",
                           tables=df.tail(20).to_html(classes='table'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
