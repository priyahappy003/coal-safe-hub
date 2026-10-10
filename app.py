import random
import os
from datetime import datetime

import joblib
import numpy as np


import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


REPORT_FILE = "hazard_reports.csv"
SENSOR_FILE = "sensor_history.csv"

MODEL_FILE = "coal_risk_model.pkl"

@st.cache_resource
def load_risk_model():
    return joblib.load(MODEL_FILE)

def generate_safety_pdf(reports):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph(
        "Coal Safe Hub - Safety Incident Report",
        styles["Title"]
    ))
    content.append(Spacer(1, 12))

    content.append(Paragraph(
        f"Report Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 16))

    total = len(reports)
    serious = (
        reports["Severity"].isin(["High", "Critical"]).sum()
        if not reports.empty else 0
    )

    content.append(Paragraph(
        f"Total Reported Hazards: {total}",
        styles["Heading2"]
    ))
    content.append(Paragraph(
        f"High/Critical Incidents: {int(serious)}",
        styles["Heading2"]
    ))
    content.append(Spacer(1, 16))

    content.append(Paragraph(
        "Incident Records",
        styles["Heading2"]
    ))
    

    table_data = [[
        "Date and Time", "Location", "Hazard", "Severity"
    ]]

    if not reports.empty:
        for _, report in reports.tail(30).iterrows():
            table_data.append([
                str(report.get("Date and Time", ""))[:19],
                str(report.get("Location", ""))[:30],
                str(report.get("Hazard", ""))[:25],
                str(report.get("Severity", ""))[:15]
            ])
    else:
        table_data.append(["No incidents recorded", "", "", ""])

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[125, 130, 115, 90]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)

    content.append(Spacer(1, 16))
    
    content.append(Spacer(1, 16))
    content.append(Paragraph(
        "Latest Environment Readings (SIMULATED)",
        styles["Heading2"]
    ))

    sensor_file = SENSOR_FILE

    if (
        os.path.exists(sensor_file)
        and os.path.getsize(sensor_file) > 0
    ):
        sensor_data = pd.read_csv(sensor_file)

        if not sensor_data.empty:
            latest = sensor_data.iloc[-1]

            sensor_table_data = [
                ["Measurement", "Latest Value"],
                ["Methane", f"{latest['Methane (%)']:.1f}%"],
                ["Temperature", f"{latest['Temperature (°C)']:.1f} °C"],
                ["Humidity", f"{latest['Humidity (%)']:.1f}%"],
                ["Recorded At", str(latest["Date and Time"])]
            ]

            sensor_table = Table(
                sensor_table_data,
                colWidths=[180, 200]
            )

            sensor_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))

            content.append(sensor_table)
        else:
            content.append(Paragraph(
                "No saved sensor readings are available.",
                styles["Normal"]
            ))
    else:
        content.append(Paragraph(
            "No saved sensor readings are available.",
            styles["Normal"]
        ))

    content.append(Spacer(1, 16))
    content.append(Paragraph(
        "IMPORTANT: This is an academic prototype. Hazard records "
        "are user-submitted and environment readings are simulated. "
        "This report is not a substitute for certified mine-safety "
        "instruments, professional assessment, or emergency procedures.",
        styles["Normal"]
    ))


    document.build(content)
    buffer.seek(0)
    return buffer.getvalue()

st.set_page_config(
    page_title="Coal Safe Hub",
    page_icon="⛏️",
    layout="wide"
)


def load_reports():
    if os.path.exists(REPORT_FILE):
        try:
            return pd.read_csv(REPORT_FILE)
        except pd.errors.EmptyDataError:
            pass

    return pd.DataFrame(columns=[
        "Date and Time", "Location", "Hazard",
        "Severity", "Description"
    ])


def save_hazard_report(location, hazard, severity, description):
    report = pd.DataFrame([{
        "Date and Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Location": location,
        "Hazard": hazard,
        "Severity": severity,
        "Description": description
    }])

    report.to_csv(
        REPORT_FILE,
        mode="a",
        header=not os.path.exists(REPORT_FILE)
        or os.path.getsize(REPORT_FILE) == 0,
        index=False
    )


st.title("⛏️ Coal Safe Hub")
st.subheader("Smart Coal Mine Safety Monitoring Dashboard")


st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 24px;
        border-radius: 14px;
        background: linear-gradient(120deg, #102a43, #176b62);
        color: white;
        margin-bottom: 20px;
    }

    .hero h1 {
        color: white;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e0f2f1;
        font-size: 16px;
        margin-bottom: 0;
    }

    div[data-testid="stMetric"] {
        background: #f0f5f9;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #d9e2ec;
    }
</style>

<div class="hero">
    <h1>⛏️ Coal Safe Hub</h1>
    <p>Smart Coal Mine Safety Monitoring Dashboard</p>
    <p>Hazard Reporting • Environment Monitoring • Safety Analytics</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Report a Hazard",
        "View Reports",
        "Environment Monitoring",
        "ML Risk Prediction",
        "Safety Guidelines",
        "About"
    ]
)

# 1. DASHBOARD

# 1. DASHBOARD
if page == "Dashboard":
    reports = load_reports()
    total_reports = len(reports)

    high_critical = int(
        reports["Severity"].isin(["High", "Critical"]).sum()
    ) if total_reports else 0

    if not reports.empty:
     st.subheader("📊 Hazard Analytics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hazard Reports", total_reports)
    col2.metric("High/Critical Reports", high_critical)
    col3.metric("Other Reports", total_reports - high_critical)

    st.subheader("🚦 Overall Safety Status")

    if high_critical > 0:
        st.error(
            f"⚠️ Attention: {high_critical} High/Critical "
            "hazard report(s) recorded. Review them promptly."
        )
    elif total_reports > 0:
        st.success(
            "No High/Critical reports are currently recorded."
        )
    else:
        st.info("No hazard reports have been submitted yet.")



    st.divider()
    st.header("🌡️ Latest Environment Readings")

    if (
        os.path.exists(SENSOR_FILE)
        and os.path.getsize(SENSOR_FILE) > 0
    ):
        sensor_data = pd.read_csv(SENSOR_FILE)

        if not sensor_data.empty:
            latest = sensor_data.iloc[-1]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Latest Methane (Simulated)",
                f"{latest['Methane (%)']:.1f}%"
            )

            col2.metric(
                "Latest Temperature (Simulated)",
                f"{latest['Temperature (°C)']:.0f} °C"
            )

            col3.metric(
                "Latest Humidity (Simulated)",
                f"{latest['Humidity (%)']:.0f}%"
            )

            st.subheader("Sensor History")

            st.line_chart(
                sensor_data.set_index("Date and Time")[[
                    "Methane (%)",
                    "Temperature (°C)",
                    "Humidity (%)"
                ]]
            )
        else:
            st.info("No sensor readings recorded yet.")
    else:
        st.info(
            "No sensor readings yet. Visit Environment Monitoring "
            "to record simulated readings."
        )

    

    
    if not reports.empty:
        st.subheader("📊 Hazard Analytics")

        fig = px.histogram(
            reports,
            x="Hazard",
            color="Severity",
            barmode="group",
            category_orders={
                "Severity": ["Low", "Medium", "High", "Critical"]
            },
            title="Hazard Reports by Type and Severity",
            labels={
                "Hazard": "Hazard Type",
                "count": "Number of Reports",
                "Severity": "Severity Level"
            },
            color_discrete_map={
                "Low": "#2E8B57",
                "Medium": "#E6AC00",
                "High": "#E87524",
                "Critical": "#C62828"
            }
        )

        fig.update_layout(
            xaxis_title="Hazard Type",
            yaxis_title="Number of Reports",
            legend_title="Severity",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Counts are based on saved hazard reports, "
            "not live mine conditions."
        )
    else:
        st.info("Submit a hazard report to populate the dashboard.")


# 2. REPORT A HAZARD
elif page == "Report a Hazard":
    st.header("🚨 Report a Mine Hazard")

    with st.form("hazard_report_form"):
        location = st.text_input("Mine location")

        hazard = st.selectbox(
            "Hazard type",
            [
                "Gas Leakage",
                "Roof Instability",
                "High Temperature",
                "Equipment Failure",
                "Water Ingress",
                "Other"
            ]
        )

        severity = st.selectbox(
            "Severity",
            ["Low", "Medium", "High", "Critical"]
        )

        description = st.text_area("Describe the hazard")
        submitted = st.form_submit_button("Submit Report")

        if submitted:
            if location.strip() and description.strip():
                save_hazard_report(
                    location.strip(),
                    hazard,
                    severity,
                    description.strip()
                )
                st.success("Hazard report saved successfully!")
            else:
                st.error("Please enter the location and description.")

# 3. VIEW REPORTS

elif page == "View Reports":
    st.header("📋 Saved Hazard Reports")

    reports = load_reports()

    if reports.empty:
        st.info("No reports found. Submit a report first.")
    else:
        search = st.text_input("Search by mine location")
        severity_filter = st.selectbox(
            "Filter by severity",
            ["All", "Low", "Medium", "High", "Critical"]
        )

        filtered = reports.copy()

        if search.strip():
            filtered = filtered[
                filtered["Location"].astype(str).str.contains(
                    search, case=False, na=False, regex=False
                )
            ]

        if severity_filter != "All":
            filtered = filtered[
                filtered["Severity"] == severity_filter
            ]

        st.metric("Matching Reports", len(filtered))

        serious_reports = filtered[
            filtered["Severity"].isin(["High", "Critical"])
        ]

        if not serious_reports.empty:
            st.warning(
                f"⚠️ {len(serious_reports)} High/Critical "
                "incident(s) in the filtered results."
            )

            st.subheader("🚨 High-Priority Incidents")

            st.dataframe(
                serious_reports,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success(
                "No High/Critical incidents in the filtered results."
            )

        st.dataframe(filtered, use_container_width=True, hide_index=True)

        st.download_button(
            "Download Reports as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="coal_safe_hub_reports.csv",
            mime="text/csv"
        )

        pdf_data = generate_safety_pdf(reports)

        st.download_button(
            label="📄 Download PDF Safety Report",
            data=pdf_data,
            file_name="coal_safe_hub_safety_report.pdf",
            mime="application/pdf"
        )


        st.divider()
        st.subheader("📊 Safety Incident Summary")

        if not reports.empty:
            total_incidents = len(reports)

            serious_incidents = reports["Severity"].isin(
                ["High", "Critical"]
            ).sum()

            summary = pd.DataFrame({
                "Metric": [
                    "Total Reported Incidents",
                    "High/Critical Incidents"
                ],
                "Count": [
                    total_incidents,
                    int(serious_incidents)
                ]
            })

            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Incidents by Hazard Type")
            hazard_summary = (
                reports["Hazard"]
                .value_counts()
                .reset_index()
            )
            hazard_summary.columns = ["Hazard", "Count"]

            st.bar_chart(
                hazard_summary.set_index("Hazard")
            )

            st.download_button(
                "Download Incident Summary",
                data=summary.to_csv(index=False).encode("utf-8"),
                file_name="safety_incident_summary.csv",
                mime="text/csv"
            )
        else:
            st.info("No incidents available to summarize.")







# 4. ENVIRONMENT MONITORING

elif page == "Environment Monitoring":
    st.header("🌡️ Mine Environment Monitoring")

    st.warning(
        "SIMULATION ONLY — Not connected to real mine sensors."
    )

    col1, col2, col3 = st.columns(3)

    methane = col1.slider(
        "Simulated methane (%)", 0.0, 5.0, 0.5, 0.1
    )

    temperature = col2.slider(
        "Simulated temperature (°C)", 10, 60, 30
    )

    humidity = col3.slider(
        "Simulated humidity (%)", 0, 100, 65
    )

    # Live Safety Alerts
    st.subheader("🚨 Live Safety Alerts")

    alerts = []

    if methane >= 1.0:
        alerts.append(
            "HIGH ALERT: Methane reached the demonstration threshold."
        )

    if temperature >= 40:
        alerts.append(
            "HIGH ALERT: Temperature reached the demonstration threshold."
        )

    if humidity >= 85:
        alerts.append(
            "WARNING: Humidity reached the demonstration threshold."
        )

    if alerts:
        for alert in alerts:
            st.error(f"🔴 {alert}")
    else:
        st.success(
            "🟢 No demonstration alerts at the current readings."
        )

    st.caption(
        "Simulation only. These thresholds are illustrative and "
        "must not be used for real mine-safety decisions."
    )

    # Current Status
    st.subheader("Current Status")

    if methane >= 1.0:
        st.error("Demonstration methane warning")
    else:
        st.success("Below demonstration methane threshold")

    if temperature >= 40:
        st.error("Demonstration temperature warning")
    else:
        st.info("Below demonstration temperature threshold")

    if humidity >= 85:
        st.warning("Demonstration humidity warning")
    else:
        st.info("Below demonstration humidity threshold")

    # Save simulated readings
    if st.button("Record Current Readings"):
        new_reading = pd.DataFrame([{
            "Date and Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Methane (%)": methane,
            "Temperature (°C)": temperature,
            "Humidity (%)": humidity
        }])

        file_exists = (
            os.path.exists(SENSOR_FILE)
            and os.path.getsize(SENSOR_FILE) > 0
        )

        new_reading.to_csv(
            SENSOR_FILE,
            mode="a",
            header=not file_exists,
            index=False
        )

        st.success("Simulated readings saved successfully!")

    # Display saved reading history
    if (
        os.path.exists(SENSOR_FILE)
        and os.path.getsize(SENSOR_FILE) > 0
    ):
        history = pd.read_csv(SENSOR_FILE)

        if not history.empty:
            st.subheader("Reading History")

            st.line_chart(
                history.set_index("Date and Time")[[
                    "Methane (%)",
                    "Temperature (°C)",
                    "Humidity (%)"
                ]]
            )

            st.dataframe(
                history,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download Reading History",
                data=history.to_csv(index=False).encode("utf-8"),
                file_name="sensor_history.csv",
                mime="text/csv"
            )
        else:
            st.info("No saved readings yet.")
    else:
        st.info(
            "No saved readings yet. Click 'Record Current Readings' "
            "to begin."
        )


# 5. ML RISK PREDICTION

elif page == "ML Risk Prediction":
    st.header("🤖 ML-Based Mine Risk Prediction")

    st.warning(
        "Academic demonstration only. These predictions are "
        "not validated for real mine-safety decisions."
    )

    col1, col2 = st.columns(2)

    with col1:
        methane = st.number_input(
            "Methane (%)",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.1
        )
        co = st.number_input(
            "Carbon Monoxide (ppm)",
            min_value=1.0,
            max_value=250.0,
            value=20.0,
            step=1.0
        )
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=10.0,
            max_value=55.0,
            value=29.0,
            step=1.0
        )

    with col2:
        humidity = st.number_input(
            "Humidity (%)",
            min_value=15.0,
            max_value=100.0,
            value=65.0,
            step=1.0
        )
        airflow = st.number_input(
            "Airflow (m/s)",
            min_value=0.05,
            max_value=5.0,
            value=1.8,
            step=0.1
        )
        vibration = st.number_input(
            "Vibration",
            min_value=0.0,
            max_value=10.0,
            value=1.0,
            step=0.1
        )

    if st.button("Predict Risk Level"):
        try:
            model = load_risk_model()

            readings = pd.DataFrame([{
                "methane_pct": methane,
                "co_ppm": co,
                "temperature_c": temperature,
                "humidity_pct": humidity,
                "airflow_mps": airflow,
                "vibration": vibration
            }])

            prediction = model.predict(readings)[0]
            probabilities = model.predict_proba(readings)[0]
            classes = model.classes_

            st.subheader("Risk Probability")

            probability_df = pd.DataFrame({
                "Risk Level": [str(c).title() for c in classes],
                "Probability (%)": probabilities * 100
            })

            fig = px.bar(
                probability_df,
                x="Risk Level",
                y="Probability (%)",
                color="Risk Level",
                title="Predicted Mine Risk Probabilities",
                color_discrete_map={
                    "Low": "#2E8B57",
                    "Medium": "#E6AC00",
                    "High": "#C62828"
                },
                text_auto=".2f"
            )

            fig.update_layout(
                yaxis_range=[0, 100],
                template="plotly_white",
                yaxis_title="Probability (%)",
                xaxis_title="Risk Category",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)


            for risk_class, probability in zip(
                classes, probabilities
            ):
                percentage = probability * 100
                st.write(
                    f"{risk_class.title()} Risk: "
                    f"{percentage:.2f}%"
                )
                st.progress(float(probability))

            st.subheader("Prediction Result")

            if prediction == "high":
                st.error("🔴 Predicted Risk: HIGH")
            elif prediction == "medium":
                st.warning("🟠 Predicted Risk: MEDIUM")
            else:
                st.success("🟢 Predicted Risk: LOW")

            st.caption(
                "Probabilities are estimates from synthetic training "
                "data, not real-world safety assessments."
            )

        except Exception as error:
            st.error(
                f"Could not load or run the model: {error}"
            )

           
           
              


# 5. SAFETY GUIDELINES 

elif page == "Safety Guidelines":
    st.header("🦺 Coal Mine Safety Guidelines")

    st.markdown("""
    - Monitor hazardous gases using approved instruments.
    - Maintain proper mine ventilation.
    - Inspect roofs and underground supports.
    - Use required personal protective equipment.
    - Maintain emergency exits and communication systems.
    - Report unsafe conditions through established procedures.
    """)

# 6. ABOUT

elif page == "About":
    st.header("About Coal Safe Hub")

    st.write("""
    Coal Safe Hub is an academic project demonstrating
    a coal-mine safety dashboard, hazard reporting,
    report storage, and simulated environmental monitoring.
    """)

    st.info(
        "This application is a prototype, not a certified "
        "mine-safety or emergency-response system."
    )
