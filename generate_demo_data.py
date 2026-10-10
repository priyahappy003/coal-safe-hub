"""Generate clearly synthetic Coal Safe Hub demo data. Not real mine measurements."""
import numpy as np
import pandas as pd

def make_demo_data(n=2500, seed=42):
    rng = np.random.default_rng(seed)
    methane = np.clip(rng.normal(0.45, 0.35, n), 0.0, 3.0)
    co = np.clip(rng.lognormal(mean=2.5, sigma=0.55, size=n), 1, 250)
    temp = np.clip(rng.normal(29, 5, n), 10, 55)
    humidity = np.clip(rng.normal(65, 12, n), 15, 100)
    airflow = np.clip(rng.normal(1.8, 0.65, n), 0.05, 5)
    vibration = np.clip(rng.lognormal(mean=-0.2, sigma=0.7, size=n), 0, 10)

    # Illustrative rules solely for generating demo labels.
    score = (
        (methane >= 1.0).astype(int)
        + (co >= 35).astype(int)
        + (temp >= 38).astype(int)
        + (airflow <= 0.7).astype(int)
        + (vibration >= 3.0).astype(int)
    )
    risk = np.where(score >= 3, "high", np.where(score >= 1, "medium", "low"))

    return pd.DataFrame({
        "methane_pct": methane.round(3),
        "co_ppm": co.round(2),
        "temperature_c": temp.round(2),
        "humidity_pct": humidity.round(2),
        "airflow_mps": airflow.round(3),
        "vibration": vibration.round(3),
        "risk_level": risk
    })

if __name__ == "__main__":
    df = make_demo_data()
    df.to_csv("demo_coal_mine_sensors.csv", index=False)
    print(f"Saved {len(df)} synthetic rows to demo_coal_mine_sensors.csv")
