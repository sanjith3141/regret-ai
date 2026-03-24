import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import os

# Config
st.set_page_config(page_title="RegretAI", layout="centered")

model = joblib.load("regret_model.pkl")

# -------------------------
# HEADER
# -------------------------

st.markdown("""
# RegretAI  
### Your Smart Purchase Companion
""")

st.markdown("---")

# -------------------------
# FINANCIAL SECTION
# -------------------------

with st.container():
    st.markdown("## Financial Details")

    col1, col2 = st.columns(2)

    with col1:
        price = st.number_input("Product Price (₹)", min_value=0)

    with col2:
        income = st.number_input("Monthly Income (₹)", min_value=0)

    savings = st.slider("Savings Percentage", 0, 50)

st.markdown("---")

# -------------------------
# BEHAVIOR SECTION
# -------------------------

with st.container():
    st.markdown("## Your Behavior")

    col1, col2 = st.columns(2)

    with col1:
        impulse = st.slider("Impulsiveness Level", 1, 10)

    with col2:
        research = st.slider("Research Time (minutes)", 0, 60)

    mood = st.selectbox("Current Mood", ["Happy","Neutral","Stressed","Excited"])

st.markdown("---")

# -------------------------
# PURCHASE SECTION
# -------------------------

with st.container():
    st.markdown("## Purchase Context")

    col1, col2 = st.columns(2)

    with col1:
        discount = st.slider("Discount %", 0, 60)
        urgency = st.selectbox("Urgency Level", ["Low","Medium","High"])

    with col2:
        brand = st.selectbox("Brand Familiarity", ["Low","Medium","High"])
        category = st.selectbox("Product Category", ["Electronics","Clothing","Food","Home","Accessories"])

    peer = st.selectbox("Peer Influence", ["None","Low","High"])

st.markdown("---")

# -------------------------
# BUTTON
# -------------------------

predict = st.button("Analyze Purchase")

# -------------------------
# RESULT SECTION
# -------------------------

if predict:

    input_data = np.array([[price, income, savings, discount, 0, 0, research, 0, 0, 0, impulse]])
    prob = model.predict_proba(input_data)[0][1]

    st.markdown("## Prediction Result")

    # Animated Gauge
    gauge_placeholder = st.empty()

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

    # Result Message
    if prob > 0.6:
        st.error("High Regret Risk")
    elif prob > 0.3:
        st.warning("Moderate Risk")
    else:
        st.success("Safe Purchase")

    # Smart Advice
    st.markdown("### Smart Advice")

    advice = []

    if price > income * 0.3:
        advice.append("Consider a cheaper alternative")

    if research < 5:
        advice.append("Spend more time researching")

    if impulse > 7:
        advice.append("Wait 24 hours before buying")

    if discount < 10:
        advice.append("Look for better deals")

    if urgency == "High":
        advice.append("Avoid rushed decisions")

    if len(advice) == 0:
        st.write("Great decision-making")
    else:
        for a in advice:
            st.write("•", a)

    # Feature Importance
    st.markdown("### Feature Influence")

    feature_names = [
        "Price","Income","Savings","Discount","Mood",
        "Urgency","Research","Brand","Category","Peer","Impulse"
    ]

    df_imp = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    st.bar_chart(df_imp.set_index("Feature"))

    # Save history silently (no message)
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
