import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import os

# Page config
st.set_page_config(page_title="RegretAI", page_icon="🛒", layout="centered")

# Load model
model = joblib.load("regret_model.pkl")

# -------------------------
# 🎨 HEADER
# -------------------------

st.markdown("# 🛒 RegretAI")
st.markdown("### Smart Purchase Decision System 💡")

st.markdown("---")

# -------------------------
# INPUT SECTION
# -------------------------

st.subheader("Enter Purchase Details")

price = st.number_input("💰 Price", min_value=0)
income = st.number_input("💵 Monthly Income", min_value=0)

col1, col2 = st.columns(2)

with col1:
    savings = st.slider("Savings %", 0, 50)
    discount = st.slider("Discount %", 0, 60)
    research = st.slider("Research Time (minutes)", 0, 60)

with col2:
    impulse = st.slider("Impulsiveness Score", 1, 10)
    mood = st.selectbox("Mood", ["Happy","Neutral","Stressed","Excited"])
    urgency = st.selectbox("Urgency Level", ["Low","Medium","High"])

brand = st.selectbox("Brand Familiarity", ["Low","Medium","High"])
category = st.selectbox("Purchase Category", ["Electronics","Clothing","Food","Home","Accessories"])
peer = st.selectbox("Peer Influence", ["None","Low","High"])

st.markdown("---")

# -------------------------
# PREDICTION
# -------------------------

if st.button("🔍 Predict Regret"):

    input_data = np.array([[price, income, savings, discount, 0, 0, research, 0, 0, 0, impulse]])

    prob = model.predict_proba(input_data)[0][1]

    st.markdown("## 🧠 Prediction Result")

    gauge_placeholder = st.empty()

    # 🎯 Animated Gauge
    for i in range(0, int(prob * 100) + 1, 2):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=i,
            title={'text': "Regret Probability (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 30], 'color': "green"},
                    {'range': [30, 60], 'color': "yellow"},
                    {'range': [60, 100], 'color': "red"},
                ],
            }
        ))
        gauge_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.02)

    # Recommendation
    if prob > 0.6:
        st.error("⚠ High Regret Risk – Avoid buying now")
    elif prob > 0.3:
        st.warning("🤔 Moderate Risk – Think before buying")
    else:
        st.success("✅ Safe Purchase")

    time.sleep(0.3)

    # -------------------------
    # 💡 SMART ADVICE
    # -------------------------

    st.markdown("### 💡 Smart Advice")

    advice = []

    if price > income * 0.3:
        advice.append("Consider a cheaper alternative")

    if research < 5:
        advice.append("Spend more time researching the product")

    if impulse > 7:
        advice.append("Wait 24 hours before purchasing")

    if discount < 10:
        advice.append("Look for better deals or discounts")

    if urgency == "High":
        advice.append("Avoid rushed decisions")

    if len(advice) == 0:
        st.write("Great decision-making 👍")
    else:
        for a in advice:
            st.write("👉", a)

    # -------------------------
    # 📌 EXPLANATION
    # -------------------------

    st.markdown("### 📌 Why this result?")

    reasons = []

    if price > income * 0.3:
        reasons.append("Price is high compared to your income")

    if research < 5:
        reasons.append("Very little research before buying")

    if impulse > 7:
        reasons.append("High impulsiveness")

    if discount < 10:
        reasons.append("Low or no discount")

    if urgency == "High":
        reasons.append("Purchase seems rushed")

    if len(reasons) == 0:
        st.write("Good decision factors overall 👍")
    else:
        for r in reasons:
            st.write("•", r)

    # -------------------------
    # 📊 FEATURE IMPORTANCE
    # -------------------------

    st.markdown("### 📊 Feature Importance")

    feature_names = [
        "Price","Income","Savings","Discount","Mood",
        "Urgency","Research","Brand","Category","Peer","Impulse"
    ]

    importances = model.feature_importances_

    df_imp = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    st.bar_chart(df_imp.set_index("Feature"))

    # -------------------------
    # 💾 SAVE HISTORY
    # -------------------------

    new_data = pd.DataFrame([{
        "Price": price,
        "Income": income,
        "Savings": savings,
        "Discount": discount,
        "Research": research,
        "Impulse": impulse,
        "Regret_Probability": prob
    }])

    if not os.path.exists("history.csv"):
        new_data.to_csv("history.csv", index=False)
    else:
        new_data.to_csv("history.csv", mode='a', header=False, index=False)

    st.success("📁 Prediction saved to history.csv")
