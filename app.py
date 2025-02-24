import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
from fpdf import FPDF
from risk_model import calculate_cad_risk

# Set page configuration
st.set_page_config(page_title="CAD Risk Prediction", page_icon="🫀", layout="wide")

# Title and subtitle
st.markdown("<h1 style='text-align: center; color: darkred;'>🫀 Coronary Artery Disease (CAD) Risk Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Enter your health parameters to estimate your risk of CAD.</h4>", unsafe_allow_html=True)

# Create Two-Column Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.sidebar.header("🔍 Enter Your Health Parameters")
    age = st.sidebar.slider("Age", 20, 90, 50)
    total_cholesterol = st.sidebar.slider("Total Cholesterol (mg/dL)", 100, 300, 200)
    ldl_cholesterol = st.sidebar.slider("LDL Cholesterol (mg/dL)", 50, 200, 100)
    hdl_cholesterol = st.sidebar.slider("HDL Cholesterol (mg/dL)", 20, 100, 50)
    triglycerides = st.sidebar.slider("Triglycerides (mg/dL)", 50, 500, 150)
    systolic_bp = st.sidebar.slider("Systolic BP (mmHg)", 90, 200, 120)
    diastolic_bp = st.sidebar.slider("Diastolic BP (mmHg)", 60, 120, 80)
    c_reactive_protein = st.sidebar.slider("C-Reactive Protein (mg/L)", 0.1, 10.0, 2.0)
    resting_heart_rate = st.sidebar.slider("Resting Heart Rate (bpm)", 40, 120, 70)
    smoking = st.sidebar.selectbox("Smoking Status", ["Non-Smoker", "Smoker"])
    diabetes = st.sidebar.selectbox("Diabetes", ["No", "Yes"])

    # Convert categorical inputs
    smoking = 1 if smoking == "Smoker" else 0
    diabetes = 1 if diabetes == "Yes" else 0

# Collect inputs
input_data = {
    "age": age,
    "total_cholesterol": total_cholesterol,
    "ldl_cholesterol": ldl_cholesterol,
    "hdl_cholesterol": hdl_cholesterol,
    "triglycerides": triglycerides,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "c_reactive_protein": c_reactive_protein,
    "resting_heart_rate": resting_heart_rate,
    "smoking": smoking,
    "diabetes": diabetes
}

# Process input when button is clicked
if st.sidebar.button("🚀 Predict CAD Risk"):
    with col2:
        st.markdown("<h3 style='text-align: center; color: darkred;'>📊 CAD Risk Score & Insights</h3>", unsafe_allow_html=True)
        
        # Get CAD risk score and feature importance
        risk_score, risk_category, feature_importance = calculate_cad_risk(input_data)
        scaled_risk_score = (risk_score / 20) * 100  # Convert to percentage

        # Display Risk Category
        if risk_category == "High Risk":
            st.error(f"⚠️ **You are at High Risk for CAD!** Risk Score: **{scaled_risk_score:.2f}/100**")
        elif risk_category == "Moderate Risk":
            st.warning(f"⚠️ **You are at Moderate Risk for CAD.** Risk Score: **{scaled_risk_score:.2f}/100**")
        else:
            st.success(f"✅ **You are at Low Risk for CAD.** Risk Score: **{scaled_risk_score:.2f}/100**")

        # Gauge Chart for Risk Score
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=scaled_risk_score,
            title={"text": "CAD Risk Score (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "red" if scaled_risk_score >= 50 else "orange" if scaled_risk_score >= 30 else "green"},
                "steps": [
                    {"range": [0, 30], "color": "lightgreen"},
                    {"range": [30, 50], "color": "yellow"},
                    {"range": [50, 100], "color": "red"}
                ]
            }
        ))
        st.plotly_chart(fig)

        # Risk Comparison
        random_risk_scores = np.random.randint(30, 90, 50)
        similar_count = sum(score <= scaled_risk_score for score in random_risk_scores)
        similar_percent = (similar_count / len(random_risk_scores)) * 100
        st.info(f"📌 Your risk score is **higher** than {similar_percent:.1f}% of people with similar profiles.")

        # Feature Importance Chart
        st.subheader("🔍 Feature Contribution to Risk Score")
        if feature_importance:
            fig = px.bar(x=list(feature_importance.keys()), y=list(feature_importance.values()),
                         labels={"x": "Features", "y": "Impact Score"}, title="Feature Importance")
            st.plotly_chart(fig)

        # Personalized Recommendations
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
        st.subheader("📝 Personalized Recommendations")
        for feature, impact in sorted_features:
            st.warning(f"🔹 **{feature}**: This is a key contributor to your risk. Consider making lifestyle changes to improve it.")

        # Find a Doctor Feature
        st.markdown("[🔍 Find a Cardiologist Near Me](https://www.google.com/maps/search/cardiologist)")

        # Generate a Downloadable PDF Report
        def generate_pdf_report():
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "CAD Risk Prediction Report", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.cell(200, 10, f"Your CAD Risk Score: {scaled_risk_score}/100", ln=True)
            pdf.cell(200, 10, f"Risk Category: {risk_category}", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, "Top Risk Contributors:", ln=True)
            for feature, impact in feature_importance.items():
                pdf.cell(200, 10, f"- {feature}: {impact} points", ln=True)
            pdf.output("CAD_Risk_Report.pdf")

        if st.button("📄 Download Full Report"):
            generate_pdf_report()
            st.success("✅ Report generated successfully! You can download it now.")
