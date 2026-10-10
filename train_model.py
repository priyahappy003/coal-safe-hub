
"""Train a Random Forest model on synthetic Coal Safe Hub data.
Academic demonstration only; not validated for real mine safety.
"""
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# 1. Load the synthetic dataset
df = pd.read_csv("demo_coal_mine_sensors_v2.csv")

# 2. Select sensor features and target
features = [
    "methane_pct",
    "co_ppm",
    "temperature_c",
    "humidity_pct",
    "airflow_mps",
    "vibration",
]

X = df[features]
y = df["risk_level"]

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# 4. Create and train the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
)

model.fit(X_train, y_train)

# 5. Make predictions on test data
y_pred = model.predict(X_test)

# 6. Display evaluation results
print("COAL SAFE HUB - RANDOM FOREST MODEL")
print("=" * 45)
print("Dataset rows:", len(df))
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("\nRisk categories:")
print(y.value_counts())

print("\nTest accuracy:", round(accuracy_score(y_test, y_pred), 4))

print("\nClassification report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("Confusion matrix (low, medium, high):")
print(confusion_matrix(y_test, y_pred, labels=["low", "medium", "high"]))
# Save the trained model for later use
joblib.dump(model, "coal_risk_model.pkl")
print("\nModel saved successfully as coal_risk_model.pkl")
