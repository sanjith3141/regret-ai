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

# COLOR PALETTE FROM IMAGE
# Dark Teal: #0f3a47
# Medium Teal: #1b5e6b
# Bright Teal: #2ba5bf
# Tan/Gold: #d4a574
# Cream: #f5f0e8

st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f3a47 0%, #1b5e6b 50%, #0a2730 100%);
        background-attachment: fixed;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    
    .main {
        background-color: transparent;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* HERO CARD */
    .hero-card {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.15) 0%, rgba(212, 165, 116, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(43, 165, 191, 0.3);
        border-radius: 28px;
        padding: 48px 40px;
        text-align: center;
        margin: 40px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(135deg, #2ba5bf 0%, #d4a574 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.1em;
        color: #d4a574;
        margin-top: 12px;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* GLASSMORPHIC CARDS */
    .glass-card {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.08) 0%, rgba(43, 165, 191, 0.03) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(43, 165, 191, 0.2);
        border-radius: 24px;
        padding: 32px;
        margin: 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        border-color: rgba(43, 165, 191, 0.35);
        box-shadow: 0 12px 48px rgba(43, 165, 191, 0.15);
        transform: translateY(-2px);
    }
    
    /* DIVIDER - SINGLE LINE ONLY */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(43, 165, 191, 0.3), transparent);
        margin: 24px 0;
        border: none;
    }
    
    /* SECTION HEADERS */
    .section-header {
        font-size: 1.4em;
        font-weight: 600;
        color: #f5f0e8;
        margin-bottom: 24px;
        margin-top: 0;
        letter-spacing: -0.3px;
    }
    
    /* INPUT LABELS & HINTS */
    .input-label {
        font-size: 0.95em;
        font-weight: 500;
        color: #f5f0e8;
        margin-bottom: 10px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85em;
    }
    
    .input-hint {
        font-size: 0.8em;
        color: #a89968;
        margin-top: 6px;
        display: block;
    }
    
    /* CUSTOM SLIDER - NO DOUBLE LINES */
    .stSlider > div {
        padding: 0 !important;
    }
    
    .stSlider > div > div {
        padding: 0 !important;
    }
    
    .stSlider > div > div > div {
        padding: 0 !important;
    }
    
    .stSlider [role="slider"] {
        background: transparent !important;
    }
    
    /* Slider track */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, rgba(27, 94, 107, 0.5), rgba(43, 165, 191, 0.8)) !important;
        border-radius: 10px !important;
        height: 8px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Slider thumb */
    .stSlider > div > div > div > div > div {
        background: linear-gradient(135deg, #2ba5bf 0%, #d4a574 100%) !important;
        border-radius: 50% !important;
        height: 20px !important;
        width: 20px !important;
        box-shadow: 0 4px 12px rgba(43, 165, 191, 0.5), 0 0 0 3px rgba(43, 165, 191, 0.2) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: grab !important;
    }
    
    .stSlider > div > div > div > div > div:hover {
        box-shadow: 0 6px 16px rgba(43, 165, 191, 0.6), 0 0 0 5px rgba(43, 165, 191, 0.25) !important;
        transform: scale(1.1) !important;
    }
    
    .stSlider > div > div > div > div > div:active {
        cursor: grabbing !important;
    }
    
    /* NUMBER INPUT */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(43, 165, 191, 0.08) !important;
        border: 1.5px solid rgba(43, 165, 191, 0.25) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1em !important;
        color: #f5f0e8 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #2ba5bf !important;
        box-shadow: 0 0 0 3px rgba(43, 165, 191, 0.2) !important;
        background: rgba(43, 165, 191, 0.12) !important;
    }
    
    .stNumberInput > div > div > input::placeholder {
        color: #a89968;
    }
    
    /* CUSTOM BUTTON */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2ba5bf 0%, #d4a574 100%);
        color: #0f3a47;
        border: none;
        border-radius: 14px;
        padding: 16px 24px;
        font-size: 1.05em;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(43, 165, 191, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 12px 32px rgba(43, 165, 191, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* RESULT CARDS */
    .result-safe {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.15) 0%, rgba(212, 165, 116, 0.08) 100%);
        border: 1.5px solid rgba(43, 165, 191, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-safe-title {
        color: #2ba5bf;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0 0 8px 0;
    }
    
    .result-safe-text {
        color: #d4a574;
        font-size: 0.95em;
        margin: 0;
    }
    
    .result-warning {
        background: linear-gradient(135deg, rgba(212, 165, 116, 0.15) 0%, rgba(43, 165, 191, 0.08) 100%);
        border: 1.5px solid rgba(212, 165, 116, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-warning-title {
        color: #d4a574;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0 0 8px 0;
    }
    
    .result-warning-text {
        color: #f5f0e8;
        font-size: 0.95em;
        margin: 0;
    }
    
    .result-danger {
        background: linear-gradient(135deg, rgba(212, 165, 116, 0.2) 0%, rgba(43, 165, 191, 0.1) 100%);
        border: 1.5px solid rgba(212, 165, 116, 0.5);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        animation: slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-danger-title {
        color: #f5b847;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0 0 8px 0;
    }
    
    .result-danger-text {
        color: #f5f0e8;
        font-size: 0.95em;
        margin: 0;
    }
    
    /* ADVICE BOX */
    .advice-box {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.1) 0%, rgba(43, 165, 191, 0.05) 100%);
        border-left: 4px solid #2ba5bf;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 0.95em;
        color: #f5f0e8;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .advice-box:hover {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.15) 0%, rgba(43, 165, 191, 0.08) 100%);
        border-left-color: #d4a574;
        transform: translateX(4px);
    }
    
    /* METRIC CARD */
    .metric-card {
        background: linear-gradient(135deg, rgba(43, 165, 191, 0.1) 0%, rgba(43, 165, 191, 0.05) 100%);
        border: 1px solid rgba(43, 165, 191, 0.25);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 12px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        border-color: rgba(43, 165, 191, 0.45);
        box-shadow: 0 8px 24px rgba(43, 165, 191, 0.2);
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 700;
        background: linear-gradient(135deg, #2ba5bf 0%, #d4a574 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #a89968;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* FOOTER */
    .footer {
        text-align: center;
        color: #a89968;
        font-size: 0.85em;
        padding: 40px 20px;
        border-top: 1px solid rgba(43, 165, 191, 0.15);
        margin-top: 40px;
        letter-spacing: 0.3px;
    }
    
    /* ANIMATIONS */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes gaugeFill {
        from {
            stroke-dashoffset: 250;
        }
        to {
            stroke-dashoffset: 0;
        }
    }
    
    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("regret_model.pkl")

model = load_model()

# HERO SECTION
st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">RegretAI</h1>
    <p class="hero-subtitle">Smart purchase decisions powered by AI intelligence</p>
</div>
""", unsafe_allow_html=True)

# FINANCIAL DETAILS CARD
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Financial Details</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<label class="input-label">Product Price</label>', unsafe_allow_html=True)
    price = st.number_input(
        "Product Price",
        min_value=0,
        step=100,
        label_visibility="collapsed",
        placeholder="Enter amount"
    )
    st.markdown('<span class="input-hint">How much does it cost?</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<label class="input-label">Monthly Income</label>', unsafe_allow_html=True)
    income = st.number_input(
        "Monthly Income",
        min_value=0,
        step=1000,
        label_visibility="collapsed",
        placeholder="Enter income"
    )
    st.markdown('<span class="input-hint">Your monthly earnings</span>', unsafe_allow_html=True)

with col3:
    st.markdown('<label class="input-label">Savings Rate</label>', unsafe_allow_html=True)
    savings = st.slider(
        "Savings Rate",
        0, 50, 20,
        label_visibility="collapsed"
    )
    st.markdown('<span class="input-hint">% of income saved</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# DIVIDER
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# BEHAVIOR CARD
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Shopping Behavior</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<label class="input-label">Impulsiveness</label>', unsafe_allow_html=True)
    impulse = st.slider(
        "Impulsiveness Level",
        1, 10, 5,
        label_visibility="collapsed"
    )
    st.markdown('<span class="input-hint">1 = Deliberate, 10 = Impulse</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<label class="input-label">Research Time</label>', unsafe_allow_html=True)
    research = st.slider(
        "Research Time",
        0, 60, 15,
        label_visibility="collapsed"
    )
    st.markdown('<span class="input-hint">Minutes of research</span>', unsafe_allow_html=True)

with col3:
    st.markdown('<label class="input-label">Current Mood</label>', unsafe_allow_html=True)
    mood = st.selectbox(
        "Current Mood",
        ["Happy", "Neutral", "Stressed", "Excited"],
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

# DIVIDER
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# PURCHASE CONTEXT CARD
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Purchase Context</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<label class="input-label">Discount Offered</label>', unsafe_allow_html=True)
    discount = st.slider(
        "Discount Offered",
        0, 60, 10,
        label_visibility="collapsed"
    )
    st.markdown('<span class="input-hint">Discount percentage</span>', unsafe_allow_html=True)
    
    st.markdown('<label class="input-label" style="margin-top: 20px;">Urgency Level</label>', unsafe_allow_html=True)
    urgency = st.selectbox(
        "Urgency Level",
        ["Low", "Medium", "High"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<label class="input-label">Brand Familiarity</label>', unsafe_allow_html=True)
    brand = st.selectbox(
        "Brand Familiarity",
        ["Low", "Medium", "High"],
        label_visibility="collapsed"
    )
    
    st.markdown('<label class="input-label" style="margin-top: 20px;">Product Category</label>', unsafe_allow_html=True)
    category = st.selectbox(
        "Product Category",
        ["Electronics", "Clothing", "Food", "Home", "Accessories"],
        label_visibility="collapsed"
    )

st.markdown('<label class="input-label" style="margin-top: 20px;">Peer Influence</label>', unsafe_allow_html=True)
peer = st.selectbox(
    "Peer Influence",
    ["None", "Low", "High"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# DIVIDER
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# CTA BUTTON
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    predict = st.button("Analyze Purchase Decision", use_container_width=True)

# RESULTS SECTION
if predict:
    # Smooth scroll to results
    st.markdown("""
    <script>
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
    </script>
    """, unsafe_allow_html=True)
    
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
    
    # DIVIDER
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Analysis Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Analysis Result</h2>', unsafe_allow_html=True)
    
    gauge_placeholder = st.empty()
    
    # Color based on probability
    if prob < 0.3:
        color = "#2ba5bf"
    elif prob < 0.6:
        color = "#d4a574"
    else:
        color = "#f5b847"
    
    # Smooth gauge animation with easing
    target_value = int(prob * 100)
    current_value = 0
    
    # Easing function for smooth animation
    def ease_out_cubic(t):
        return 1 - pow(1 - t, 3)
    
    for step in range(101):
        progress = step / 100
        eased_progress = ease_out_cubic(progress)
        current_value = int(target_value * eased_progress)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_value,
            title={'text': "Regret Probability", 'font': {'size': 18, 'color': '#f5f0e8'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#1b5e6b'},
                'bar': {'color': color, 'thickness': 0.85},
                'steps': [
                    {'range': [0, 33], 'color': 'rgba(43, 165, 191, 0.08)'},
                    {'range': [33, 66], 'color': 'rgba(212, 165, 116, 0.08)'},
                    {'range': [66, 100], 'color': 'rgba(245, 184, 71, 0.08)'},
                ],
                'threshold': {
                    'line': {'color': color, 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            },
            number={'font': {'size': 48, 'color': color}, 'suffix': '%'}
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'family': "-apple-system, BlinkMacSystemFont", 'size': 14, 'color': '#f5f0e8'},
            height=420,
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        gauge_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.015)
    
    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    
    # Risk Assessment with animation
    if prob > 0.6:
        st.markdown("""
        <div class="result-danger">
            <p class="result-danger-title">High Regret Risk</p>
            <p class="result-danger-text">We recommend reconsidering this purchase. Take time to evaluate your decision carefully.</p>
        </div>
        """, unsafe_allow_html=True)
    elif prob > 0.3:
        st.markdown("""
        <div class="result-warning">
            <p class="result-warning-title">Moderate Risk</p>
            <p class="result-warning-text">Consider the recommendations below before making your final decision.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-safe">
            <p class="result-safe-title">Safe to Purchase</p>
            <p class="result-safe-text">This appears to be a well-considered decision. You can proceed with confidence.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # DIVIDER
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Recommendations Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Recommendations</h2>', unsafe_allow_html=True)
    
    advice = []
    
    if price > income * 0.3:
        advice.append("Consider a more budget-friendly alternative to reduce financial strain")
    
    if research < 5:
        advice.append("Invest more time in researching this product before committing")
    
    if impulse > 7:
        advice.append("Give yourself 24 hours before making this purchase decision")
    
    if discount < 10:
        advice.append("Look for better deals elsewhere before finalizing this purchase")
    
    if urgency == "High":
        advice.append("Avoid making rushed decisions influenced by artificial urgency")
    
    if len(advice) == 0:
        st.markdown("""
        <div class="advice-box" style="border-left-color: #2ba5bf; background: linear-gradient(135deg, rgba(43, 165, 191, 0.15) 0%, rgba(43, 165, 191, 0.08) 100%);">
            <p style="color: #f5f0e8; margin: 0;">Your decision-making process is excellent. Trust your judgment.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, suggestion in enumerate(advice):
            st.markdown(
                f'<div class="advice-box" style="animation-delay: {idx * 0.1}s;"><p style="margin: 0;">{suggestion}</p></div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # DIVIDER
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Feature Importance Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Key Factors</h2>', unsafe_allow_html=True)
    
    feature_names = [
        "Price", "Income", "Savings", "Discount", "Mood",
        "Urgency", "Research Time", "Brand", "Category", "Peer Influence", "Impulsiveness"
    ]
    
    df_imp = pd.DataFrame({
        "Factor": feature_names,
        "Influence": model.feature_importances_
    }).sort_values(by="Influence", ascending=False).head(6)
    
    fig = go.Figure(
        data=[go.Bar(
            x=df_imp["Influence"],
            y=df_imp["Factor"],
            orientation='h',
            marker=dict(
                color="rgba(43, 165, 191, 0.8)",
                line=dict(color="rgba(212, 165, 116, 0.4)", width=2)
            ),
            text=[f"{x:.3f}" for x in df_imp["Influence"]],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Influence: %{x:.4f}<extra></extra>'
        )]
    )
    
    fig.update_layout(
        xaxis_title="Influence Score",
        yaxis_title="",
        height=350,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=120, r=40),
        font={'family': "-apple-system, BlinkMacSystemFont", 'color': '#f5f0e8'},
        xaxis={'gridcolor': 'rgba(43, 165, 191, 0.15)'},
        yaxis={'tickfont': {'size': 12}, 'tickcolor': '#a89968'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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

# FOOTER
st.markdown("""
<div class="footer">
    <p>RegretAI — Intelligent purchase decision analysis powered by machine learning</p>
</div>
""", unsafe_allow_html=True)
