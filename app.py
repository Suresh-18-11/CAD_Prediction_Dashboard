import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from risk_model import calculate_cad_risk

# Set page configuration
st.set_page_config(page_title="CAD Risk Prediction", page_icon="🫀", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: darkred;'>🫀 Coronary Artery Disease (CAD) Risk Prediction</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Enter your health parameters to estimate your risk of CAD.</h4>", unsafe_allow_html=True)

# Sidebar for User Inputs
st.sidebar.header("🔍 Enter Your Health Parameters")

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

# Collect input data
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

# Prediction Button
if st.sidebar.button("🚀 Predict CAD Risk"):
    # Calculate risk score
    risk_score, risk_category, feature_importance = calculate_cad_risk(input_data)
    scaled_risk_score = (risk_score / 20) * 100  # Convert to percentage scale

    # Display Prediction Result
    st.subheader("📢 Prediction Result:")
    if risk_category == "High Risk":
        st.error(f"⚠️ **You are at High Risk for CAD!** Risk Score: **{scaled_risk_score:.2f}/100**")
    elif risk_category == "Moderate Risk":
        st.warning(f"⚠️ **You are at Moderate Risk for CAD.** Risk Score: **{scaled_risk_score:.2f}/100**")
    else:
        st.success(f"✅ **You are at Low Risk for CAD.** Risk Score: **{scaled_risk_score:.2f}/100**")

    # Gauge Chart for Risk Score
    st.subheader("📊 CAD Risk Score")
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

    # Feature Contribution Chart
    st.subheader("🔍 Feature Contribution to Risk Score")
    if feature_importance:
        fig = px.bar(x=list(feature_importance.keys()), y=list(feature_importance.values()),
                     labels={"x": "Features", "y": "Impact Score"}, title="Feature Importance")
        st.plotly_chart(fig)

    # Personalized Recommendations
    st.subheader("📝 Personalized Recommendations")
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
    for feature, impact in sorted_features:
        if feature == "Total Cholesterol":
            st.warning("🟡 **High Total Cholesterol:** Consider a diet low in saturated fats and cholesterol. Increase intake of fruits, vegetables, and whole grains.")
        elif feature == "LDL Cholesterol":
            st.warning("🟡 **High LDL Cholesterol:** Incorporate healthy fats like omega-3s, and reduce trans fats. Regular physical activity can help lower LDL levels.")
        elif feature == "HDL Cholesterol":
            st.warning("🟢 **Low HDL Cholesterol:** Engage in regular exercise, quit smoking, and maintain a healthy weight to boost HDL levels.")
        elif feature == "Triglycerides":
            st.warning("🟡 **High Triglycerides:** Limit sugar and refined carbohydrates. Avoid excessive alcohol consumption and aim for regular physical activity.")
        elif feature == "Systolic BP":
            st.warning("🟡 **High Systolic Blood Pressure:** Reduce sodium intake, manage stress, and engage in regular physical activity.")
        elif feature == "C-Reactive Protein":
            st.warning("🟡 **Elevated C-Reactive Protein:** This indicates inflammation. Consider an anti-inflammatory diet rich in antioxidants.")
        elif feature == "Smoking":
            st.error("🔴 **Smoking:** Quitting smoking can significantly reduce your risk of CAD. Seek support if needed.")
        elif feature == "Diabetes":
            st.error("🔴 **Diabetes:** Manage blood sugar levels through diet, exercise, and medication as prescribed.")

    # Medical Comparison Table
    st.subheader("📊 How Do Your Values Compare to Normal Ranges?")
    df_reference = pd.DataFrame({
        "Feature": ["Total
::contentReference[oaicite:0]{index=0}
 
