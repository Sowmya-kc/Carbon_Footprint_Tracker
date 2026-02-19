"""
AI Prediction Page — ML model inference + comparison
Updated for Carbon Emission dataset
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os


# ── Load models once and cache ─────────────────────────────────────────────────

@st.cache_resource
def load_models():
    models = {}
    try:
        models['rf']     = joblib.load('models/random_forest.pkl')
        models['kmeans'] = joblib.load('models/kmeans.pkl')
        models['scaler'] = joblib.load('models/scaler.pkl')
        models['xgb']    = joblib.load('models/xgboost.pkl')
        with open('models/cluster_label_map.json') as f:
            models['cluster_map'] = json.load(f)
        with open('models/feature_names.json') as f:
            models['features'] = json.load(f)
        try:
            models['fi'] = pd.read_csv('models/feature_importance.csv')
        except:
            pass
        return models, None
    except FileNotFoundError as e:
        return None, f"⚠️ Models not found. Please run `python train_models.py` first.\nError: {e}"


def make_input_df(inputs, features):
    """Convert user inputs dict to DataFrame matching training features"""
    row = [inputs[feat] for feat in features]
    return pd.DataFrame([row], columns=features)


def show():
    st.markdown("<div class='hero-title' style='font-size:2rem'>🤖 AI Prediction Engine</div>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280; margin-bottom:1.5rem'>"
        "ML models trained on 10,000 real profiles predict your carbon footprint.</p>",
        unsafe_allow_html=True)

    models, error = load_models()
    if error:
        st.error(error)
        st.code("python train_models.py", language="bash")
        return

    if 'user_inputs' not in st.session_state:
        st.warning("⚠️ Please go to **🧮 Calculator** first and fill in your data.")
        return

    inputs = st.session_state['user_inputs']
    estimated_total = st.session_state.get('estimated_co2', 2000)

    try:
        input_df = make_input_df(inputs, models['features'])
    except KeyError as e:
        st.error(f"Feature mismatch: {e}")
        return

    rf_pred  = models['rf'].predict(input_df)[0]
    xgb_pred = models['xgb'].predict(input_df)[0]
    ensemble = (rf_pred * 0.6 + xgb_pred * 0.4)

    x_scaled = models['scaler'].transform(input_df)
    cluster_id = str(models['kmeans'].predict(x_scaled)[0])
    cluster_label = models['cluster_map'].get(cluster_id, "Medium Emitter")

    st.session_state['rf_pred'] = rf_pred
    st.session_state['ensemble_pred'] = ensemble
    st.session_state['cluster'] = cluster_label

    if 'Low' in cluster_label:
        color = "#22c55e"
    elif 'Medium' in cluster_label:
        color = "#fbbf24"
    else:
        color = "#f87171"

    st.markdown("### 🎯 ML Model Predictions")
    
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class='co2-meter'>
            <div style='font-size:0.7rem; color:#6b7280'>🌲 Random Forest</div>
            <div style='font-family:Syne,sans-serif; font-size:2.5rem; font-weight:800; color:#22c55e'>{rf_pred:,.0f}</div>
            <div style='font-size:0.8rem; color:#6b7280'>kg CO₂ / year</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='co2-meter' style='border-color:#2dd4bf'>
            <div style='font-size:0.7rem; color:#6b7280'>🔮 Ensemble</div>
            <div style='font-family:Syne,sans-serif; font-size:2.5rem; font-weight:800; color:#2dd4bf'>{ensemble:,.0f}</div>
            <div style='font-size:0.8rem; color:#6b7280'>kg CO₂ / year</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='co2-meter'>
            <div style='font-size:0.7rem; color:#6b7280'>🚀 XGBoost</div>
            <div style='font-family:Syne,sans-serif; font-size:2.5rem; font-weight:800; color:#a3e635'>{xgb_pred:,.0f}</div>
            <div style='font-size:0.8rem; color:#6b7280'>kg CO₂ / year</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cluster_desc = {
        'Low Emitter': ("Small climate impact. You're ahead of most!", "#22c55e"),
        'Medium Emitter': ("Around average. Room for improvement!", "#fbbf24"),
        'High Emitter': ("Above average. Great potential to reduce!", "#f87171"),
    }

    desc, clr = cluster_desc.get(cluster_label, cluster_desc['Medium Emitter'])

    st.markdown(f"""
    <div class='carbon-card' style='border-color:{clr}; border-width:2px'>
        <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:{clr}'>{cluster_label}</div>
        <div style='font-size:0.85rem; color:#9ca3af; line-height:1.7'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    years = list(range(2025, 2031))
    business_as_usual = [round(ensemble * (1 + 0.015)**i) for i in range(6)]
    with_actions = [round(ensemble * (0.95 - 0.08 * i)) for i in range(6)]
    with_actions = [max(x, 500) for x in with_actions]

    projection_df = pd.DataFrame({
        'Year': years,
        'Business as Usual': business_as_usual,
        'With Actions': with_actions,
    })

    st.markdown("#### 📅 5-Year Projection")
    st.line_chart(projection_df.set_index('Year'), color=['#f87171', '#22c55e'])

    if 'fi' in models:
        st.markdown("#### 🔍 Top Features")
        fi = models['fi'].head(10)
        st.bar_chart(fi.set_index('feature')['importance'], color="#22c55e", horizontal=True)

    st.success("✅ Go to **💡 Recommendations** for your action plan!")