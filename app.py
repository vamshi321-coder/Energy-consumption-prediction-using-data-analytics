from flask import Flask, render_template, request
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="energy_project"
)

cursor = db.cursor()

# Load ML Model
model = pickle.load(open("model.pkl", "rb"))

MODEL_ACCURACY = "98.53%"


@app.route("/")
def home():

    # Fetch history
    cursor.execute("""
        SELECT temperature,
               humidity,
               squarefootage,
               occupancy,
               prediction,
               created_at
        FROM prediction_history
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    history = []

    for row in rows:
        history.append({
            "temperature": row[0],
            "humidity": row[1],
            "squarefootage": row[2],
            "occupancy": row[3],
            "prediction": round(row[4], 2),
            "date": row[5]
        })

    # Total predictions count
    cursor.execute("""
        SELECT COUNT(*)
        FROM prediction_history
    """)

    total_predictions = cursor.fetchone()[0]

    # Latest prediction
    cursor.execute("""
        SELECT prediction
        FROM prediction_history
        ORDER BY id DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()
    latest_prediction = round(latest[0], 2) if latest else 0

    # Premium Graph
    cursor.execute("""
        SELECT prediction
        FROM prediction_history
        ORDER BY id ASC
    """)

    graph_data = cursor.fetchall()
    prediction_values = [row[0] for row in graph_data]

    plt.figure(figsize=(10, 5))

    plt.plot(
        prediction_values,
        marker="o",
        linewidth=3,
        markersize=8
    )

    plt.fill_between(
        range(len(prediction_values)),
        prediction_values,
        alpha=0.2
    )

    plt.title(
        "Energy Consumption Prediction Trend",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Prediction Number")
    plt.ylabel("Energy Consumption (kWh)")

    plt.grid(
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "static/graph.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    return render_template(
        "index.html",
        total_predictions=total_predictions,
        latest_prediction=latest_prediction,
        accuracy=MODEL_ACCURACY,
        history=history,
        graph=True
    )


@app.route("/predict", methods=["POST"])
def predict():

    # Inputs
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    squarefootage = float(request.form["squarefootage"])
    occupancy = float(request.form["occupancy"])
    renewable = float(request.form["renewable"])

    hvac = request.form["hvac"]
    lighting = request.form["lighting"]
    day = request.form["day"]
    holiday = request.form["holiday"]

    # Convert categorical
    hvac_on = 1 if hvac == "On" else 0
    lighting_on = 1 if lighting == "On" else 0

    monday = 1 if day == "Monday" else 0
    saturday = 1 if day == "Saturday" else 0
    sunday = 1 if day == "Sunday" else 0
    thursday = 1 if day == "Thursday" else 0
    tuesday = 1 if day == "Tuesday" else 0

    # Features
    features = np.array([[
        temperature,
        humidity,
        squarefootage,
        occupancy,
        renewable,

        hvac_on,
        1 - hvac_on,

        lighting_on,
        1 - lighting_on,

        monday,
        saturday,
        sunday,
        thursday,
        tuesday
    ]])

    # Prediction
    prediction = model.predict(features)

    # Save to MySQL
    cursor.execute("""
        INSERT INTO prediction_history
        (
            temperature,
            humidity,
            squarefootage,
            occupancy,
            renewable,
            hvac,
            lighting,
            day_type,
            holiday,
            prediction
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        temperature,
        humidity,
        squarefootage,
        occupancy,
        renewable,
        hvac,
        lighting,
        day,
        holiday,
        float(prediction[0])
    ))

    db.commit()

    # Fetch updated history
    cursor.execute("""
        SELECT temperature,
               humidity,
               squarefootage,
               occupancy,
               prediction,
               created_at
        FROM prediction_history
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    history = []

    for row in rows:
        history.append({
            "temperature": row[0],
            "humidity": row[1],
            "squarefootage": row[2],
            "occupancy": row[3],
            "prediction": round(row[4], 2),
            "date": row[5]
        })

    # Total predictions count
    cursor.execute("""
        SELECT COUNT(*)
        FROM prediction_history
    """)

    total_predictions = cursor.fetchone()[0]

    # Premium Graph
    cursor.execute("""
        SELECT prediction
        FROM prediction_history
        ORDER BY id ASC
    """)

    graph_data = cursor.fetchall()
    prediction_values = [row[0] for row in graph_data]

    plt.figure(figsize=(10, 5))

    plt.plot(
        prediction_values,
        marker="o",
        linewidth=3,
        markersize=8
    )

    plt.fill_between(
        range(len(prediction_values)),
        prediction_values,
        alpha=0.2
    )

    plt.title(
        "Energy Consumption Prediction Trend",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Prediction Number")
    plt.ylabel("Energy Consumption (kWh)")

    plt.grid(
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "static/graph.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    return render_template(
        "index.html",
        prediction_text=f"Predicted Energy Consumption: {prediction[0]:.2f}",
        graph=True,
        history=history,
        total_predictions=total_predictions,
        latest_prediction=round(prediction[0], 2),
        accuracy=MODEL_ACCURACY
    )


if __name__ == "__main__":
    app.run(debug=True)