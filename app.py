"""
Carbon Footprint Tracker & AI Predictor
==========================================
Main Streamlit application entry point.

Run:
    streamlit run app.py
"""

import streamlit as st

# ─── PAGE CONFIG (must be FIRST streamlit call) ───────────────────────────────

st.set_page_config(
    page_title="🌍 Carbon AI Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0f0a 0%, #0f1a0f 50%, #0a1010 100%);
    color: #e8f5e9;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d150d !important;
    border-right: 1px solid #1f3320;
}
[data-testid="stSidebar"] .stMarkdown { color: #a7c9a8; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #111a11;
    border: 1px solid #1f3320;
    border-radius: 12px;
    padding: 1rem 1.25rem !important;
    transition: all 0.3s;
}
[data-testid="stMetric"]:hover { border-color: #22c55e; }
[data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
[data-testid="stMetricValue"] { color: #22c55e !important; font-family: 'Syne', sans-serif !important; font-size: 1.8rem !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 15px rgba(34,197,94,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(34,197,94,0.5) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div {
    background: #22c55e !important;
}

/* ── Select boxes ── */
.stSelectbox [data-baseweb="select"] {
    background: #111a11 !important;
    border-color: #1f3320 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #111a11 !important;
    border: 1px solid #1f3320 !important;
    border-radius: 8px !important;
    color: #e8f5e9 !important;
}

/* ── Info boxes ── */
.stInfo { background: rgba(45,212,191,0.08) !important; border-color: #2dd4bf !important; }
.stSuccess { background: rgba(34,197,94,0.08) !important; border-color: #22c55e !important; }
.stWarning { background: rgba(251,191,36,0.08) !important; border-color: #fbbf24 !important; }
.stError { background: rgba(248,113,113,0.08) !important; border-color: #f87171 !important; }

/* ── Custom cards ── */
.carbon-card {
    background: #111a11;
    border: 1px solid #1f3320;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    transition: all 0.3s;
}
.carbon-card:hover { border-color: #22c55e; box-shadow: 0 0 20px rgba(34,197,94,0.1); }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #22c55e, #a3e635);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: #e8f5e9;
    margin-bottom: 0.25rem;
}

.co2-meter {
    text-align: center;
    padding: 2rem;
    background: #0d150d;
    border: 2px solid #1f3320;
    border-radius: 20px;
    margin: 1rem 0;
}

.co2-value {
    font-family: 'Syne', sans-serif;
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
}

.badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 2rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-green  { background: rgba(34,197,94,0.15);  color: #22c55e;  border: 1px solid rgba(34,197,94,0.3); }
.badge-yellow { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-red    { background: rgba(248,113,113,0.15);color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.badge-teal   { background: rgba(45,212,191,0.15); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.3); }

.tip-card {
    background: #0d1f0d;
    border-left: 4px solid #22c55e;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
}

div[data-testid="stHorizontalBlock"] { gap: 1rem; }

/* hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── IMPORT PAGE MODULES ──────────────────────────────────────────────────────

from pages import home, calculator, predictions, analytics, recommendations

# ─── SIDEBAR NAVIGATION ───────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0'>
        <div style='font-size:2.5rem'>🌍</div>
        <div style='font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem; color:#22c55e'>Carbon AI</div>
        <div style='font-size:0.7rem; color:#6b7280; letter-spacing:0.1em'>TRACKER & PREDICTOR</div>
    </div>
    <hr style='border-color:#1f3320; margin: 0.5rem 0 1.5rem'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠  Home", "🧮  Calculator", "🤖  AI Prediction", "📊  Analytics", "💡  Recommendations"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border-color:#1f3320; margin: 1.5rem 0 1rem'>
    <div style='font-size:0.7rem; color:#374b38; text-align:center; line-height:1.8'>
        Built with Python · Scikit-Learn<br>XGBoost · Streamlit · Plotly<br>
        <span style='color:#22c55e'>● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

# ─── ROUTE TO PAGE ────────────────────────────────────────────────────────────

if   "Home"            in page: home.show()
elif "Calculator"      in page: calculator.show()
elif "AI Prediction"   in page: predictions.show()
elif "Analytics"       in page: analytics.show()
elif "Recommendations" in page: recommendations.show()