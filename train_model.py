
"""Compare ML models for Coal Safe Hub.
Academic demonstration on synthetic data only.
Not validated for real mine safety.
"""

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

# 1. Load synthetic dataset
df = pd.read_csv("demo_coal_mine_sensors_v2.csv")

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

# 2. Use the same split for every model
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# 3. Define four algorithms
models = {
    "Decision Tree": DecisionTreeClassifier(
        random_state=42,
        class_weight="balanced",
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        random_state=42,
    ),
    "Logistic Regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
        ),
    ),
}

results = []
trained_models = {}

print("COAL SAFE HUB - MODEL COMPARISON")
print("=" * 55)
print("Dataset rows:", len(df))
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("\nRisk categories:")
print(y.value_counts().to_string())

# 4. Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        y_pred,
        labels=["low", "medium", "high"],
        average="macro",
        zero_division=0,
    )

    accuracy = accuracy_score(y_test, y_pred)

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Macro Precision": precision,
        "Macro Recall": recall,
        "Macro F1": f1,
    })

    trained_models[name] = model

    print(f"\n{'-' * 55}")
    print("MODEL:", name)
    print("Accuracy:", round(accuracy, 4))
    print(classification_report(
        y_test,
        y_pred,
        labels=["low", "medium", "high"],
        zero_division=0,
    ))
    print("Confusion matrix (low, medium, high):")
    print(confusion_matrix(
        y_test,
        y_pred,
        labels=["low", "medium", "high"],
    ))

# 5. Save comparison table
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(
    by="Macro F1",
    ascending=False,
)

results_df.to_csv("model_comparison_results.csv", index=False)

print("\n\nMODEL COMPARISON SUMMARY")
print(results_df.round(4).to_string(index=False))
print("\nResults saved to model_comparison_results.csv")

# 6. Save the model with the highest macro F1
best_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_name]

joblib.dump(best_model, "coal_risk_model.pkl")

print("\nSelected model:", best_name)
print("Saved selected model to coal_risk_model.pkl")
print(
    "\nWARNING: These results use synthetic data and "
    "do not establish real-world mine safety performance."
)
