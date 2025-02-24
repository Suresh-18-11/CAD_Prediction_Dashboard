import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from risk_model import calculate_cad_risk

# Set page configuration
st.set_page_config(page_title="CAD Risk Prediction", page_icon="🫀", layout="wide")

# Title
st.title("🫀 Coronary Artery Disease (CAD) Risk Prediction")
st.write("Enter your health parameters to estimate your risk of CAD.")

# Sidebar for user input
st.sidebar.header("User Input Features")

# User Inputs
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

# Collect inputs into a dictionary
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

# Predict CAD risk when button is clicked
if st.sidebar.button("Predict CAD Risk"):
    risk_score, risk_category = calculate_cad_risk(input_data)

    # Display the results
    st.subheader("Prediction Result:")
    if risk_category == "High Risk":
        st.error(f"⚠️ You are at **High Risk** for CAD! Risk Score: {risk_score}/20")
    elif risk_category == "Moderate Risk":
        st.warning(f"⚠️ You are at **Moderate Risk** for CAD. Risk Score: {risk_score}/20")
    else:
        st.success(f"✅ You are at **Low Risk** for CAD. Risk Score: {risk_score}/20")

    # Visualization - Risk Score Bar
    st.subheader("Risk Score Breakdown")
    risk_factors = list(input_data.keys())
    factor_values = list(input_data.values())

    fig, ax = plt.subplots()
    ax.barh(risk_factors, factor_values, color="teal")
    ax.set_xlabel("Feature Values")
    ax.set_title("Feature Contribution to CAD Risk")
    st.pyplot(fig)
