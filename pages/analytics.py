"""
Analytics Page — Interactive Plotly visualizations
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,21,13,0.6)',
    font=dict(family='Inter, sans-serif', color='#9ca3af', size=12),
    xaxis=dict(gridcolor='#1f3320', linecolor='#1f3320', zerolinecolor='#1f3320'),
    yaxis=dict(gridcolor='#1f3320', linecolor='#1f3320', zerolinecolor='#1f3320'),
    margin=dict(l=20, r=20, t=40, b=20),
)


def show():
    st.markdown("<div class='hero-title' style='font-size:2rem'>📊 Analytics Dashboard</div>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280; margin-bottom:1.5rem'>"
        "Deep-dive into your emission profile with interactive charts. "
        "See exactly where your CO₂ comes from and how you stack up globally.</p>",
        unsafe_allow_html=True)

    if 'user_inputs' not in st.session_state:
        st.warning("⚠️ Please fill in the **🧮 Calculator** first.")
        return

    # Get the estimated total from calculator
    total = st.session_state.get('estimated_co2', 2000)
    global_avg = 2260  # Dataset average
    
    # Create a simple breakdown based on inputs
    inputs = st.session_state['user_inputs']
    
    # Estimate breakdown (rough approximation)
    car_emissions = inputs['vehicle_monthly_distance_km'] * 0.21 * 12 if inputs['transport'] == 0 else 0
    air_emissions = {0: 510, 1: 0, 2: 255, 3: 1020}.get(inputs['frequency_of_traveling_by_air'], 255)
    diet_emissions = {0: 1825, 1: 1095, 2: 365, 3: 730}.get(
    inputs.get('diet_type', 1), 
    1095
)
    energy_emissions = {0: 1200, 1: 800, 2: 600, 3: 500}.get(inputs['heating_energy_source'], 800)
    lifestyle_emissions = inputs.get('monthly_grocery_bill', 150) * 3 + inputs.get('how_many_new_clothes_monthly', 3) * 25
    
    breakdown = {
        'Car Travel': max(0, car_emissions),
        'Public Transport': 300 if inputs.get('transport', 0) == 1 else 0,
        'Flights': air_emissions,
        'Home Energy': energy_emissions,
        'Diet': diet_emissions,
        'Shopping': lifestyle_emissions,
        'Electronics': inputs.get('how_long_tv_pc_daily_hour', 5) * 0.05 * 365 + inputs.get('how_long_internet_daily_hour', 8) * 0.03 * 365,
    }

    # ── ROW 1: Pie + Bar comparison ──────────────────────────────────────────

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("##### 🥧 Your Emissions by Category")
        labels  = list(breakdown.keys())
        values  = list(breakdown.values())
        colors  = ['#22c55e','#2dd4bf','#a3e635','#fbbf24','#fb923c','#f87171','#a78bfa']

        fig_pie = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color='#0a0f0a', width=2)),
            textinfo='label+percent',
            textfont=dict(size=11, color='white'),
            hovertemplate='<b>%{label}</b><br>%{value:,.0f} kg CO₂<br>%{percent}<extra></extra>'
        ))
        fig_pie.add_annotation(
            text=f"<b>{total:,.0f}</b><br>kg CO₂",
            x=0.5, y=0.5, font=dict(size=14, color='white'), showarrow=False
        )
        fig_pie.update_layout(**PLOTLY_THEME, showlegend=True,
                               legend=dict(orientation='h', y=-0.15, font=dict(size=10)),
                               height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("##### 🌍 You vs The World")
        benchmarks = {
            'You': total,
            'Global Avg': 4800,
            'US Avg': 14600,
            'EU Avg': 6700,
            'India Avg': 1900,
            'Paris Target 2050': 2000,
        }
        bench_colors = ['#2dd4bf' if k == 'You' else
                        ('#22c55e' if k == 'Paris Target 2050' else '#374b38')
                        for k in benchmarks]

        fig_bar = go.Figure(go.Bar(
            x=list(benchmarks.keys()),
            y=list(benchmarks.values()),
            marker=dict(color=bench_colors, line=dict(color='#0a0f0a', width=1)),
            text=[f'{v:,}' for v in benchmarks.values()],
            textposition='outside',
            textfont=dict(color='white', size=10),
            hovertemplate='<b>%{x}</b><br>%{y:,} kg CO₂/year<extra></extra>'
        ))
        fig_bar.update_layout(**PLOTLY_THEME, height=380,
                               yaxis_title='kg CO₂ / year',
                               bargap=0.3)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── ROW 2: Radar + Gauge ─────────────────────────────────────────────────

    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.markdown("##### 🕸️ Emission Profile Radar")

        # Normalize each category 0–10 scale
        max_values = {
            'Car Travel': 8000, 'Public Transport': 500, 'Flights': 3000,
            'Home Energy': 4000, 'Diet': 1700, 'Shopping': 1600, 'Electronics': 300
        }
        radar_scores = [
            min(10, round(breakdown.get(k, 0) / max_values.get(k, 1) * 10, 1))
            for k in max_values
        ]

        cats = list(max_values.keys())
        cats_closed = cats + [cats[0]]
        scores_closed = radar_scores + [radar_scores[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores_closed, theta=cats_closed,
            fill='toself',
            fillcolor='rgba(34,197,94,0.15)',
            line=dict(color='#22c55e', width=2),
            name='You'
        ))
        # Global average radar
        avg_scores = [4.5, 3.0, 2.5, 4.0, 7.0, 2.5, 5.0]
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_scores + [avg_scores[0]], theta=cats_closed,
            fill='toself',
            fillcolor='rgba(251,191,36,0.05)',
            line=dict(color='#fbbf24', width=1.5, dash='dot'),
            name='Global Avg'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(13,21,13,0.6)',
                radialaxis=dict(visible=True, range=[0,10],
                                gridcolor='#1f3320', linecolor='#1f3320',
                                tickfont=dict(color='#6b7280', size=9)),
                angularaxis=dict(gridcolor='#1f3320', linecolor='#1f3320',
                                 tickfont=dict(color='#9ca3af', size=10))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#9ca3af'),
            legend=dict(orientation='h', y=-0.1),
            height=380, margin=dict(l=30,r=30,t=30,b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col4:
        st.markdown("##### 🎯 Carbon Gauge")
        # Gauge meter
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=total,
            delta={'reference': global_avg, 'suffix': ' kg',
                   'font': {'size': 14, 'color': '#9ca3af'}},
            number={'suffix': ' kg/yr', 'font': {'size': 22, 'color': 'white'}},
            title={'text': "Your CO₂ vs Global Avg", 'font': {'size': 13, 'color': '#9ca3af'}},
            gauge={
                'axis': {'range': [0, 16000], 'tickwidth': 1, 'tickcolor': '#374b38',
                         'tickfont': {'color': '#6b7280', 'size': 9}},
                'bar': {'color': '#2dd4bf', 'thickness': 0.25},
                'bgcolor': '#111a11',
                'bordercolor': '#1f3320',
                'steps': [
                    {'range': [0, 2000],    'color': 'rgba(34,197,94,0.2)'},
                    {'range': [2000, 6000], 'color': 'rgba(251,191,36,0.15)'},
                    {'range': [6000, 16000],'color': 'rgba(248,113,113,0.15)'},
                ],
                'threshold': {
                    'line': {'color': '#fbbf24', 'width': 3},
                    'thickness': 0.8,
                    'value': global_avg
                }
            }
        ))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                                 font=dict(color='white'),
                                 height=380,
                                 margin=dict(l=30,r=30,t=50,b=30))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # ── ROW 3: Monthly breakdown ──────────────────────────────────────────────

    st.markdown("<hr style='border-color:#1f3320'>", unsafe_allow_html=True)
    st.markdown("##### 📅 Monthly Carbon Trend (Simulated)")
    st.markdown("<p style='color:#6b7280; font-size:0.82rem; margin-bottom:1rem'>"
                "Estimated monthly variation based on seasonal patterns (heating in winter, AC in summer, holiday travel peaks)</p>",
                unsafe_allow_html=True)

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    seasonal = np.array([1.18, 1.10, 1.00, 0.92, 0.88, 0.95, 1.05, 1.02, 0.90, 0.93, 1.05, 1.20])
    monthly_vals = ((total / 12) * seasonal).round(0)

    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=months, y=monthly_vals,
        marker=dict(
            color=monthly_vals,
            colorscale=[[0,'#22c55e'], [0.5,'#fbbf24'], [1,'#f87171']],
            showscale=False
        ),
        text=[f'{v:.0f}' for v in monthly_vals],
        textposition='outside',
        textfont=dict(color='white', size=9),
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} kg CO₂<extra></extra>'
    ))
    fig_monthly.add_hline(
        y=total/12,
        line=dict(color='#fbbf24', dash='dash', width=1.5),
        annotation_text=f"Monthly avg: {total/12:,.0f} kg",
        annotation_font=dict(color='#fbbf24', size=11)
    )
    fig_monthly.update_layout(**PLOTLY_THEME, height=300,
                               yaxis_title='kg CO₂ / month', xaxis_title='Month')
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.info("💡 Go to **📊 Analytics** page and **💡 Recommendations** to see what actions will move your needle the most.")