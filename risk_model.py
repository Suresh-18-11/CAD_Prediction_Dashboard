def calculate_cad_risk(features):
    """
    Rule-based CAD risk scoring system.
    Returns risk score and category (Low, Moderate, High).
    """
    risk_score = 0

    # Assign risk points
    if features["total_cholesterol"] > 240:
        risk_score += 3
    elif features["total_cholesterol"] > 200:
        risk_score += 2

    if features["ldl_cholesterol"] > 160:
        risk_score += 3
    elif features["ldl_cholesterol"] > 130:
        risk_score += 2

    if features["hdl_cholesterol"] < 40:
        risk_score += 2

    if features["triglycerides"] > 200:
        risk_score += 3

    if features["systolic_bp"] > 140 or features["diastolic_bp"] > 90:
        risk_score += 3

    if features["c_reactive_protein"] > 3:
        risk_score += 2

    if features["resting_heart_rate"] > 90:
        risk_score += 2

    if features["smoking"] == 1:
        risk_score += 3

    if features["diabetes"] == 1:
        risk_score += 3

    if features["age"] > 60:
        risk_score += 2

    # Categorize risk
    if risk_score >= 10:
        risk_category = "High Risk"
    elif risk_score >= 5:
        risk_category = "Moderate Risk"
    else:
        risk_category = "Low Risk"

    return risk_score, risk_category
