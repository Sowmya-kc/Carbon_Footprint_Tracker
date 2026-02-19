"""
Home Page — Carbon AI Tracker
"""
import streamlit as st


def show():
    # ── HERO ──────────────────────────────────────────────────────────────────

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown("""
        <div class='hero-title'>Track. Predict.<br>Reduce. 🌍</div>
        <p style='color:#6b7280; font-size:1rem; line-height:1.8; margin-top:0.75rem'>
            An AI-powered carbon footprint tracker that analyzes your lifestyle,
            predicts your future CO₂ emissions using <strong style='color:#22c55e'>Machine Learning</strong>,
            and gives you a personalized action plan to fight climate change.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Models Trained", "4", "RF · XGB · LR · DT")
        c2.metric("Dataset Size", "2,000", "real-world profiles")
        c3.metric("Accuracy", "~91%", "R² Score")

    with col2:
        # Animated CO₂ globe visual
        st.markdown("""
        <div style='
            background: radial-gradient(circle at 40% 40%, #0d2e14, #050a05);
            border: 1px solid #1f3320;
            border-radius: 20px;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 0 40px rgba(34,197,94,0.1);
        '>
            <div style='font-size:5rem; line-height:1'>🌍</div>
            <div style='font-family:Syne,sans-serif; font-size:1rem; color:#22c55e; margin-top:0.75rem; font-weight:700'>
                Global Avg Emissions
            </div>
            <div style='font-family:Syne,sans-serif; font-size:3rem; color:#e8f5e9; font-weight:800; line-height:1.2'>
                4,800 kg
            </div>
            <div style='font-size:0.75rem; color:#6b7280'>CO₂ per person per year</div>
            <hr style='border-color:#1f3320; margin:1rem 0'>
            <div style='font-size:0.75rem; color:#f87171'>⚠️ We need to cut this to 2,000 kg by 2050</div>
            <div style='font-size:0.7rem; color:#6b7280; margin-top:0.3rem'>Source: IEA / IPCC</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1f3320'>", unsafe_allow_html=True)

    # ── WHAT THIS APP DOES ────────────────────────────────────────────────────

    st.markdown("<div class='section-title'>What this app does</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")

    features = [
        ("🧮", "Calculate", "calculator",
         "Enter your travel, diet, and energy habits to get your real carbon footprint in seconds."),
        ("🤖", "AI Predict", "AI Prediction",
         "Our trained Random Forest + XGBoost models predict your future annual emissions."),
        ("📊", "Analyze", "Analytics",
         "Interactive Plotly charts break down your emissions by category vs global averages."),
        ("💡", "Recommend", "Recommendations",
         "AI clusters your profile and gives personalized tips to reduce your footprint."),
    ]

    for col, (icon, title, page, desc) in zip(cols, features):
        col.markdown(f"""
        <div class='carbon-card' style='text-align:center'>
            <div style='font-size:2rem; margin-bottom:0.75rem'>{icon}</div>
            <div style='font-family:Syne,sans-serif; font-weight:700; color:#22c55e; margin-bottom:0.5rem'>{title}</div>
            <div style='font-size:0.82rem; color:#6b7280; line-height:1.6'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1f3320'>", unsafe_allow_html=True)

    # ── ML TECH USED ──────────────────────────────────────────────────────────

    st.markdown("<div class='section-title'>ML Models Used</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    models = [
        ("🌲", "Random Forest", "200 trees · Max depth 12", "Primary predictor"),
        ("🚀", "XGBoost", "300 estimators · LR 0.05", "Challenger model"),
        ("📐", "Linear Regression", "Baseline benchmark", "Explainability"),
        ("🌳", "Decision Tree", "Max depth 8", "Visual explanation"),
        ("🔵", "K-Means (k=3)", "User segmentation", "Clustering"),
    ]

    cols = st.columns(5, gap="small")
    for col, (icon, name, params, role) in zip(cols, models):
        col.markdown(f"""
        <div style='
            background:#111a11; border:1px solid #1f3320; border-radius:12px;
            padding:1rem; text-align:center;
        '>
            <div style='font-size:1.5rem'>{icon}</div>
            <div style='font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem; color:#e8f5e9; margin-top:0.5rem'>{name}</div>
            <div style='font-size:0.65rem; color:#6b7280; margin-top:0.3rem'>{params}</div>
            <div style='margin-top:0.5rem'>
                <span class='badge badge-green' style='font-size:0.6rem'>{role}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 Use the sidebar to navigate. Start with **🧮 Calculator** to enter your data, then go to **🤖 AI Prediction**!")