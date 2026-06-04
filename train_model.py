import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load dataset
df = pd.read_csv("Energy_consumption.csv")

# Remove timestamp if exists
if "Timestamp" in df.columns:
    df.drop("Timestamp", axis=1, inplace=True)

# Convert categorical columns
df = pd.get_dummies(
    df,
    columns=["DayOfWeek", "Holiday", "HVACUsage", "LightingUsage"],
    drop_first=True
)

# Features and target
X = df.drop("EnergyConsumption", axis=1)
y = df["EnergyConsumption"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = LinearRegression()

# Train
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Accuracy
score = r2_score(y_test, predictions)

print("Linear Regression Accuracy:",
      round(score * 100, 2), "%")

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model saved successfully!")