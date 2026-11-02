from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')
model = pickle.load(open(MODEL_PATH, 'rb'))

MODEL_ACCURACY = "98.53%"

# In-memory history (resets on cold start — Vercel serverless)
prediction_history = []

@app.route("/")
def home():
    total = len(prediction_history)
    latest = prediction_history[0]['prediction'] if prediction_history else 0
    return render_template(
        "index.html",
        total_predictions=total,
        latest_prediction=latest,
        accuracy=MODEL_ACCURACY,
        history=prediction_history[:20],
        graph=False,
        prediction_text=None
    )

@app.route("/predict", methods=["POST"])
def predict():
    temperature     = float(request.form["temperature"])
    humidity        = float(request.form["humidity"])
    squarefootage   = float(request.form["squarefootage"])
    occupancy       = float(request.form["occupancy"])
    renewable       = float(request.form["renewable"])
    hvac            = request.form["hvac"]
    lighting        = request.form["lighting"]
    day             = request.form["day"]
    holiday         = request.form["holiday"]

    # Encode — must match training column order exactly:
    # Temperature, Humidity, SquareFootage, Occupancy, RenewableEnergy,
    # DayOfWeek_Monday, DayOfWeek_Saturday, DayOfWeek_Sunday,
    # DayOfWeek_Thursday, DayOfWeek_Tuesday, DayOfWeek_Wednesday,
    # Holiday_Yes, HVACUsage_On, LightingUsage_On

    features = np.array([[
        temperature,
        humidity,
        squarefootage,
        occupancy,
        renewable,
        1 if day == "Monday"    else 0,
        1 if day == "Saturday"  else 0,
        1 if day == "Sunday"    else 0,
        1 if day == "Thursday"  else 0,
        1 if day == "Tuesday"   else 0,
        1 if day == "Wednesday" else 0,
        1 if holiday == "Yes"   else 0,
        1 if hvac == "On"       else 0,
        1 if lighting == "On"   else 0,
    ]])

    prediction = round(float(model.predict(features)[0]), 2)

    from datetime import datetime
    prediction_history.insert(0, {
        "temperature":   temperature,
        "humidity":      humidity,
        "squarefootage": squarefootage,
        "occupancy":     occupancy,
        "prediction":    prediction,
        "date":          datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    total = len(prediction_history)

    return render_template(
        "index.html",
        prediction_text=f"Predicted Energy Consumption: {prediction}",
        graph=False,
        history=prediction_history[:20],
        total_predictions=total,
        latest_prediction=prediction,
        accuracy=MODEL_ACCURACY
    )
