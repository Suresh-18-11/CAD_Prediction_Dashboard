def calculate_cad_risk(features):
    risk_score = 0
    feature_importance = {}

    if features["total_cholesterol"] > 240:
        risk_score += 3
        feature_importance["Total Cholesterol"] = 3
    if features["ldl_cholesterol"] > 160:
        risk_score += 3
        feature_importance["LDL Cholesterol"] = 3
    if features["hdl_cholesterol"] < 40:
        risk_score += 2
        feature_importance["HDL Cholesterol"] = 2
    if features["triglycerides"] > 200:
        risk_score += 3
        feature_importance["Triglycerides"] = 3
    if features["systolic_bp"] > 140:
        risk_score += 3
        feature_importance["Systolic BP"] = 3
    if features["diastolic_bp"] > 90:
        risk_score += 3
        feature_importance["Diastolic BP"] = 3
    if features["c_reactive_protein"] > 3:
        risk_score += 2
        feature_importance["C-Reactive Protein"] = 2
    if features["smoking"] == 1:
        risk_score += 3
        feature_importance["Smoking"] = 3
    if features["diabetes"] == 1:
        risk_score += 3
        feature_importance["Diabetes"] = 3

    risk_category = "High Risk" if risk_score >= 10 else "Moderate Risk" if risk_score >= 5 else "Low Risk"
    return risk_score, risk_category, feature_importance
