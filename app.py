import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="RegretAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# TRUE MODERN DARK MODE PALETTE
# Background: Deep OLED Blue/Black (#0B0F19 to #111827)
# Cards: Dark Slate (#151B28)
# Primary Accent: Neon Cyan (#00E5FF)
# Text: Slate White (#F3F4F6)
# Secondary Text: Cool Gray (#94A3B8)

st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 100%);
        background-attachment: fixed;
        color: #F3F4F6;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    
    .main {
        background-color: transparent;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* HERO CARD - Golden Ratio Typography */
    .hero-card {
        background: linear-gradient(135deg, rgba(21, 27, 40, 0.8) 0%, rgba(11, 15, 25, 0.9) 100%);
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 26px;
        padding: 42px 26px;
        text-align: center;
        margin: 42px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    .hero-title {
        font-size: 2.618em;
        font-weight: 700;
        color: #00E5FF;
        margin: 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1em;
        color: #94A3B8;
        margin-top: 16px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* NATIVE STREAMLIT CONTAINERS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #151B28 !important;
        border: 1px solid rgba(0, 229, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 26px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(0, 229, 255, 0.3) !important;
        box-shadow: 0 8px 26px rgba(0, 229, 255, 0.08) !important;
    }
    
    /* SECTION HEADERS */
    .section-header {
        font-size: 1.618em;
        font-weight: 600;
        color: #F3F4F6;
        margin-bottom: 26px;
        margin-top: 0;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* INPUT LABELS & HINTS */
    .input-label {
        font-size: 0.85em;
        font-weight: 600;
        color: #00E5FF;
        margin-bottom: 10px;
        display: block;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .input-hint {
        font-size: 0.8em;
        color: #94A3B8;
        margin-top: 6px;
        display: block;
    }
    
    /* FIXED SLIDER - Only styling the thumb so the track response works natively */
    div[role="slider"] {
        background-color: #00E5FF !important;
        border: 2px solid #0B0F19 !important;
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.6) !important;
        width: 20px !important;
        height: 20px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    
    div[role="slider"]:hover, div[role="slider"]:focus {
        transform: scale(1.15) !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.9) !important;
        outline: none !important;
    }
    
    /* INPUT FIELDS */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: #0B0F19 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        color: #F3F4F6 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.2) !important;
    }
    
    /* CUSTOM BUTTON */
    .stButton > button {
        width: 100%;
        background: #00E5FF;
        color: #0B0F19;
        border: none;
        border-radius: 10px;
        padding: 16px 26px;
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: #33EAFF;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
    }
    
    /* RESULT BOXES */
    .result-box {
        border-radius: 16px;
        padding: 26px;
        margin: 26px 0;
        background: #0B0F19;
        border: 1px solid;
    }
    .result-safe { border-color: rgba(0, 229, 255, 0.5); box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.05); }
    .result-warning { border-color: rgba(251, 191, 36, 0.5); box-shadow: inset 0 0 20px rgba(251, 191, 36, 0.05); }
    .result-danger { border-color: rgba(239, 68, 68, 0.5); box-shadow: inset 0 0 20px rgba(239, 68, 68, 0.05); }
    
    .result-title {
        font-weight: 700;
        font-size: 1.618em;
        margin: 0 0 10px 0;
    }
    
    .advice-box {
        background: rgba(11, 15, 25, 0.8);
        border-left: 3px solid #00E5FF;
        border-radius: 8px;
        padding: 16px 26px;
        margin: 16px 0;
        font-size: 1em;
        color: #E2E8F0;
    }
    
    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load("regret_model.pkl")
    except:
        # Fallback dummy model if file is missing during UI testing
        class DummyModel:
            def predict_proba(self, X): return [[0.2, 0.65]]
            @property
            def feature_importances_(self): return np.random.rand(11)
        return DummyModel()

model = load_model()

# HERO SECTION
st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">RegretAI</h1>
    <p class="hero-subtitle">Mindful purchase decisions powered by intelligence</p>
</div>
""", unsafe_allow_html=True)

# FINANCIAL DETAILS SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Financial Details</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<label class="input-label">Product Price</label>', unsafe_allow_html=True)
        price = st.number_input("Product Price", min_value=0, step=100, label_visibility="collapsed", placeholder="Amount")
        st.markdown('<span class="input-hint">Total cost of item</span>', unsafe_allow_html=True)

    with col2:
        st.markdown('<label class="input-label">Monthly Income</label>', unsafe_allow_html=True)
        income = st.number_input("Monthly Income", min_value=0, step=1000, label_visibility="collapsed", placeholder="Income")
        st.markdown('<span class="input-hint">Your monthly earnings</span>', unsafe_allow_html=True)

    with col3:
        st.markdown('<label class="input-label">Savings Rate</label>', unsafe_allow_html=True)
        savings = st.slider("Savings Rate", 0, 50, 20, label_visibility="collapsed")
        st.markdown('<span class="input-hint">% of income saved</span>', unsafe_allow_html=True)


# BEHAVIOR SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Shopping Behavior</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<label class="input-label">Impulsiveness</label>', unsafe_allow_html=True)
        impulse = st.slider("Impulsiveness Level", 1, 10, 5, label_visibility="collapsed")
        st.markdown('<span class="input-hint">1 = Deliberate, 10 = Impulse</span>', unsafe_allow_html=True)

    with col2:
        st.markdown('<label class="input-label">Research Time</label>', unsafe_allow_html=True)
        research = st.slider("Research Time", 0, 60, 15, label_visibility="collapsed")
        st.markdown('<span class="input-hint">Minutes spent researching</span>', unsafe_allow_html=True)

    with col3:
        st.markdown('<label class="input-label">Current Mood</label>', unsafe_allow_html=True)
        mood = st.selectbox("Current Mood", ["Neutral", "Happy", "Stressed", "Excited"], label_visibility="collapsed")


# PURCHASE CONTEXT SECTION
with st.container(border=True):
    st.markdown('<h2 class="section-header">Purchase Context</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<label class="input-label">Discount Offered</label>', unsafe_allow_html=True)
        discount = st.slider("Discount Offered", 0, 60, 10, label_visibility="collapsed")
        
        st.markdown('<label class="input-label" style="margin-top: 26px;">Urgency Level</label>', unsafe_allow_html=True)
        urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"], label_visibility="collapsed")

    with col2:
        st.markdown('<label class="input-label">Brand Familiarity</label>', unsafe_allow_html=True)
        brand = st.selectbox("Brand Familiarity", ["Low", "Medium", "High"], label_visibility="collapsed")
        
        st.markdown('<label class="input-label" style="margin-top: 26px;">Product Category</label>', unsafe_allow_html=True)
        category = st.selectbox("Product Category", ["Electronics", "Clothing", "Food", "Home", "Accessories"], label_visibility="collapsed")

    st.markdown('<label class="input-label" style="margin-top: 26px;">Peer Influence</label>', unsafe_allow_html=True)
    peer = st.selectbox("Peer Influence", ["None", "Low", "High"], label_visibility="collapsed")


# CTA BUTTON
st.markdown('<div style="margin: 42px 0;"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1.618, 1])

with col2:
    predict = st.button("Analyze Purchase Decision", use_container_width=True)

# RESULTS SECTION
if predict:
    # Prepare input data
    mood_mapping = {"Happy": 1, "Neutral": 2, "Stressed": 3, "Excited": 4}
    urgency_mapping = {"Low": 1, "Medium": 2, "High": 3}
    brand_mapping = {"Low": 1, "Medium": 2, "High": 3}
    peer_mapping = {"None": 1, "Low": 2, "High": 3}
    category_mapping = {
        "Electronics": 1, "Clothing": 2, "Food": 3, "Home": 4, "Accessories": 5
    }
    
    input_data = np.array([[
        price, income, savings, discount,
        mood_mapping[mood], urgency_mapping[urgency],
        research, brand_mapping[brand],
        category_mapping[category], peer_mapping[peer],
        impulse
    ]])
    
    prob = model.predict_proba(input_data)[0][1]
    
    # Analysis Container
    with st.container(border=True):
        st.markdown('<h2 class="section-header">Mindful Analysis</h2>', unsafe_allow_html=True)
        
        # Color based on probability (Neon/Dark Mode equivalents)
        if prob < 0.3:
            color = "#00E5FF" # Cyan
        elif prob < 0.6:
            color = "#FBBF24" # Amber
        else:
            color = "#EF4444" # Crimson Red
            
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=int(prob * 100),
            title={'text': "Regret Probability", 'font': {'size': 16, 'color': '#F3F4F6'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#F3F4F6'},
                'bar': {'color': color, 'thickness': 0.8},
                'steps': [
                    {'range': [0, 33], 'color': 'rgba(0, 229, 255, 0.05)'},
                    {'range': [33, 66], 'color': 'rgba(251, 191, 36, 0.05)'},
                    {'range': [66, 100], 'color': 'rgba(239, 68, 68, 0.05)'},
                ],
            },
            number={'font': {'size': 42, 'color': color}, 'suffix': '%'}
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "-apple-system, BlinkMacSystemFont", 'color': '#F3F4F6'},
            height=350,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk Assessment
        if prob > 0.6:
            st.markdown(f"""
            <div class="result-box result-danger">
                <p class="result-title" style="color: {color}">High Regret Risk</p>
                <p style="margin: 0; color: #E2E8F0;">It is highly recommended to pause on this purchase. Take a day to evaluate if this aligns with your goals.</p>
            </div>
            """, unsafe_allow_html=True)
        elif prob > 0.3:
            st.markdown(f"""
            <div class="result-box result-warning">
                <p class="result-title" style="color: {color}">Moderate Risk</p>
                <p style="margin: 0; color: #E2E8F0;">Consider the mindful recommendations below before making your final decision.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box result-safe">
                <p class="result-title" style="color: {color}">Safe to Purchase</p>
                <p style="margin: 0; color: #E2E8F0;">This appears to be a well-considered and balanced decision.</p>
            </div>
            """, unsafe_allow_html=True)

    # Recommendations Container
    with st.container(border=True):
        st.markdown('<h2 class="section-header">Gentle Reminders</h2>', unsafe_allow_html=True)
        
        advice = []
        if price > income * 0.3:
            advice.append("Consider a more budget-friendly alternative to maintain financial peace.")
        if research < 5:
            advice.append("Take a few more minutes to read reviews or find alternatives.")
        if impulse > 7:
            advice.append("Implement the '24-hour rule' before finalizing this transaction.")
        if discount < 10:
            advice.append("There might be better deals available. Consider waiting for a sale.")
        if urgency == "High":
            advice.append("Remember that 'limited time' offers are often designed to bypass logical decision-making.")
            
        if len(advice) == 0:
            st.markdown('<div class="advice-box" style="border-left-color: #00E5FF;">Your decision-making process is well-balanced. Trust your judgment.</div>', unsafe_allow_html=True)
        else:
            for suggestion in advice:
                st.markdown(f'<div class="advice-box">{suggestion}</div>', unsafe_allow_html=True)

    # Save history
    new_data = pd.DataFrame([{
        "Timestamp": pd.Timestamp.now(),
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
