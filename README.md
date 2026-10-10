# Coal Safe Hub — AI/ML Coal Mine Safety Monitoring

## 1. Project Overview
Coal Safe Hub is an academic M.Tech project that combines a Streamlit dashboard, hazard reporting, simulated environmental monitoring, and machine-learning-based risk estimation. It helps demonstrate how mine safety information can be recorded, analyzed, and presented in one application.

## 2. Objectives
- Record and review coal mine hazard reports.
- Monitor simulated environmental sensor readings.
- Estimate risk levels using a Random Forest classifier.
- Display charts and model prediction probabilities.
- Generate downloadable CSV and PDF reports.
- Explore machine learning for academic coal mine safety research.

## 3. Technologies Used
- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- Joblib
- Plotly
- ReportLab
- CSV files for local data storage

## 4. Main Modules
1. Dashboard
2. Report a Hazard
3. View Reports
4. Environment Monitoring
5. ML Risk Prediction
6. Safety Guidelines
7. About

## 5. Machine Learning
The project uses a Random Forest classifier trained on a synthetic dataset with six input features:
- Methane percentage
- Carbon monoxide concentration (CO)
- Temperature
- Humidity
- Airflow speed
- Vibration

The model estimates one of three risk categories: low, medium, or high.

The current demonstration dataset contains 2,500 rows. A single 80/20 train-test split produced 99.4% test accuracy. This result applies only to the synthetic dataset and must not be interpreted as real-world mine safety performance.

## 6. Installation and Execution
Run the following commands from the project directory on macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

To stop the application, press `Control + C` in Terminal.

## 7. Project Data
The application uses local CSV files for demonstration data and records. The included sensor readings are simulated; the application is not connected to physical mine sensors.

## 8. Limitations and Safety
- The demonstration dataset is synthetic and may reflect the rules used to generate its labels.
- High test accuracy on synthetic data does not establish real-world predictive ability.
- Environmental readings are not collected from live mine equipment.
- The application is not a certified safety system. Its predictions must not be used for real mine operations, evacuation decisions, or equipment shutdown.
- Real deployment would require validated sensors, expert-approved thresholds, independent datasets, external validation, and appropriate safety and regulatory approval.

## 9. Future Scope
- Integrate real sensor data after suitable validation.
- Evaluate models on independent real-world datasets.
- Investigate time-series forecasting of methane concentration.
- Add user authentication and role-based access.
- Add secure database storage and audit logging.
- Improve model explainability and monitoring.

## 10. Conclusion
Coal Safe Hub demonstrates an integrated academic approach to hazard reporting, simulated environmental monitoring, and machine-learning-based risk estimation. It provides a foundation for further research and validation, rather than a deployable mine safety system.
## Live Demo

Try the deployed application here:

[Coal Safe Hub — Open Live App](https://coal-safe-app-tbuqtfrnkgvbmnvgwihaje.streamlit.app/)

## Project Features

- Coal mine sensor monitoring dashboard
- Hazard reporting and alerts
- Machine Learning-based risk prediction
- Model comparison dashboard

**Note:** This is an academic prototype using demonstration data, not a certified real-world mine safety system.
