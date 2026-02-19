"""
Recommendations Page — AI-powered personalized action plan
"""
import streamlit as st


RECOMMENDATIONS = {
    'Low Emitter': {
        'color': '#22c55e', 'badge': 'badge-green',
        'headline': "You're a Climate Champion 🌟",
        'summary': "Your footprint is well below the global average. Focus on maintaining and optimizing these last-mile improvements.",
        'actions': [
            ("🌱", "Go fully plant-based 2 days/week",
             "Even reducing meat 2 days/week saves ~200 kg CO₂/year.",
             "High Impact", "#22c55e"),
            ("☀️", "Install rooftop solar if renting allows",
             "Full solar can cut your home energy footprint by 90%.",
             "High Impact", "#22c55e"),
            ("🚲", "Replace short car trips with cycling",
             "Trips under 5 km by bike save avg 0.21 kg CO₂ each.",
             "Medium Impact", "#a3e635"),
            ("♻️", "Switch to a zero-waste lifestyle",
             "Avoiding fast fashion and single-use plastics saves ~300 kg CO₂/year.",
             "Medium Impact", "#a3e635"),
            ("🌍", "Offset remaining emissions via verified projects",
             "Use Gold Standard certified offsets for emissions you can't eliminate.",
             "Offset", "#2dd4bf"),
        ]
    },
    'Medium Emitter': {
        'color': '#fbbf24', 'badge': 'badge-yellow',
        'headline': "Room to Improve — Big Wins Available 🎯",
        'summary': "You're near the global average. 3-4 targeted changes can drop you into Low Emitter territory within a year.",
        'actions': [
            ("🚗", "Reduce car use by 30%",
             "Carpooling, working from home 2 days/week, or switching to public transit can save 500–1,200 kg CO₂/year.",
             "Highest Impact", "#f87171"),
            ("✈️", "Replace 1 flight/year with train travel",
             "One avoided return flight saves 255–500 kg CO₂ depending on distance.",
             "High Impact", "#fbbf24"),
            ("🥗", "Shift to vegetarian diet 4 days/week",
             "Reducing meat consumption is one of the single most impactful personal choices: saves up to 700 kg/year.",
             "High Impact", "#fbbf24"),
            ("💡", "Switch all lights to LED + smart power strips",
             "Eliminating standby power and upgrading bulbs saves 150–300 kWh/year.",
             "Medium Impact", "#a3e635"),
            ("🌡️", "Lower heating by 2°C in winter",
             "Each degree reduction saves approx 6% on heating bills and ~80 kg CO₂/year.",
             "Medium Impact", "#a3e635"),
            ("🛍️", "Buy secondhand for clothing and electronics",
             "Manufacturing a single laptop emits 300 kg CO₂. Buying refurbished cuts this by 70%.",
             "Medium Impact", "#a3e635"),
        ]
    },
    'High Emitter': {
        'color': '#f87171', 'badge': 'badge-red',
        'headline': "High Impact — Maximum Reduction Potential 🔥",
        'summary': "Your footprint is significantly above average, which means you have the most potential to reduce. Even one major change makes a huge difference.",
        'actions': [
            ("✈️", "Eliminate or drastically cut air travel",
             "If flights are a major part of your footprint, cutting 2–3 flights saves 500–1,500 kg CO₂. Take trains where possible.",
             "Critical Impact", "#f87171"),
            ("🚗", "Switch to electric or hybrid vehicle",
             "Switching from a petrol car to an EV saves 1,500–2,500 kg CO₂/year at average Indian grid electricity.",
             "Critical Impact", "#f87171"),
            ("🥩", "Cut heavy meat consumption by 50%",
             "High meat diet = ~1,600 kg CO₂/year. Reducing by 50% saves 600–800 kg CO₂/year.",
             "Critical Impact", "#f87171"),
            ("⚡", "Optimize home electricity — insulation + solar",
             "Home energy upgrades + solar panel installation can slash home emissions by 60–90%.",
             "High Impact", "#fbbf24"),
            ("🏠", "Work from home 3+ days/week",
             "Eliminating a 30 km daily commute saves ~1,300 kg CO₂/year for a petrol car driver.",
             "High Impact", "#fbbf24"),
            ("📱", "Stop buying new electronics every year",
             "Production of a smartphone emits ~70 kg CO₂. Keep devices longer, buy refurbished.",
             "Medium Impact", "#a3e635"),
        ]
    }
}


def show():
    st.markdown("<div class='hero-title' style='font-size:2rem'>💡 AI Recommendations</div>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280; margin-bottom:1.5rem'>"
        "Personalized action plan generated from your K-Means cluster profile. "
        "These are ranked by CO₂ impact for your specific emission pattern.</p>",
        unsafe_allow_html=True)

    # ── CHECK SESSION STATE ───────────────────────────────────────────────────

    if 'cluster' not in st.session_state:
        if 'breakdown' not in st.session_state:
            st.warning("⚠️ Please complete the **🧮 Calculator** and **🤖 AI Prediction** first.")
            return
        # Fallback: assign based on total
        total = st.session_state.get('total_co2', 5000)
        cluster = 'Low Emitter' if total < 2000 else ('Medium Emitter' if total < 6000 else 'High Emitter')
    else:
        cluster = st.session_state['cluster']

    total    = st.session_state.get('total_co2', 0)
    ensemble = st.session_state.get('ensemble_pred', total)
    recs     = RECOMMENDATIONS[cluster]

    # ── CLUSTER HEADER ────────────────────────────────────────────────────────

    st.markdown(f"""
    <div class='carbon-card' style='border-color:{recs['color']}; border-width:2px; margin-bottom:1.5rem'>
        <div style='display:flex; align-items:flex-start; gap:1rem; flex-wrap:wrap'>
            <div style='flex:1'>
                <div style='font-size:0.7rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:0.4rem'>
                    Your Cluster → K-Means Segmentation
                </div>
                <div style='font-family:Syne,sans-serif; font-size:1.6rem; font-weight:800; color:{recs['color']}'>
                    {cluster}
                </div>
                <div style='font-family:Syne,sans-serif; font-size:1rem; color:#e8f5e9; margin:0.3rem 0'>
                    {recs['headline']}
                </div>
                <p style='color:#9ca3af; font-size:0.85rem; line-height:1.7; margin-top:0.5rem'>
                    {recs['summary']}
                </p>
            </div>
            <div style='text-align:center; min-width:140px'>
                <div style='font-size:0.7rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.1em'>
                    ML Predicted
                </div>
                <div style='font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:{recs['color']}'>
                    {ensemble:,.0f}
                </div>
                <div style='font-size:0.75rem; color:#6b7280'>kg CO₂/year</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACTION CARDS ─────────────────────────────────────────────────────────

    st.markdown("#### 🎯 Your Personalized Action Plan")
    st.markdown(f"<p style='color:#6b7280; font-size:0.85rem; margin-bottom:1.25rem'>"
                f"Ranked by CO₂ impact for a <strong style='color:{recs['color']}'>{cluster}</strong> profile:</p>",
                unsafe_allow_html=True)

    for i, (icon, title, desc, impact, imp_color) in enumerate(recs['actions'], 1):
        st.markdown(f"""
        <div class='carbon-card' style='display:flex; gap:1rem; align-items:flex-start'>
            <div style='
                background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2);
                border-radius:10px; width:44px; height:44px; min-width:44px;
                display:flex; align-items:center; justify-content:center;
                font-size:1.3rem; flex-shrink:0;
            '>{icon}</div>
            <div style='flex:1'>
                <div style='display:flex; align-items:center; gap:0.75rem; flex-wrap:wrap; margin-bottom:0.4rem'>
                    <span style='font-family:Syne,sans-serif; font-weight:700; color:#e8f5e9; font-size:0.95rem'>
                        {i}. {title}
                    </span>
                    <span style='
                        background:{imp_color}22; color:{imp_color};
                        border:1px solid {imp_color}44;
                        border-radius:1rem; padding:0.15rem 0.6rem;
                        font-size:0.65rem; font-weight:600; letter-spacing:0.05em;
                    '>{impact}</span>
                </div>
                <p style='color:#9ca3af; font-size:0.82rem; line-height:1.7; margin:0'>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1f3320'>", unsafe_allow_html=True)

    # ── POTENTIAL SAVINGS ────────────────────────────────────────────────────

    st.markdown("#### 💰 Potential Savings Summary")

    savings_map = {
        'Low Emitter':    (600, 25),
        'Medium Emitter': (1800, 38),
        'High Emitter':   (4500, 55),
    }
    saving_kg, saving_pct = savings_map[cluster]

    cols = st.columns(4)
    cols[0].metric("If you follow ALL tips", f"-{saving_kg:,} kg", f"-{saving_pct}% reduction")
    cols[1].metric("After Reduction", f"{max(0, total - saving_kg):,.0f} kg", "new annual footprint")
    cols[2].metric("Trees Equivalent", f"{int(saving_kg / 21):,}", "trees saved per year")
    cols[3].metric("Monthly Saving", f"{saving_kg//12:,} kg", "per month avg")

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("🎉 All data flows from your Calculator → AI Prediction → Recommendations. Try changing your inputs and see how recommendations shift!")