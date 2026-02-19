"""
Calculator Page — Real-time carbon footprint calculator
Works with the actual Carbon Emission dataset features
"""
import streamlit as st
import pandas as pd
import json


def show():
    st.markdown("<div class='hero-title' style='font-size:2rem'>🧮 Carbon Calculator</div>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b7280; margin-bottom:1.5rem'>Fill in your lifestyle habits below. "
        "The calculator estimates your carbon footprint based on real-world emission factors.</p>",
        unsafe_allow_html=True)

    # Load encoders to know what options we have
    try:
        with open('data/label_encoders.json', 'r') as f:
            encoders = json.load(f)
    except:
        encoders = {}

    # ── INPUT FORM ──────────────────────────────────────────────────────────

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("#### 🚗 Transport & Travel")
        
        transport = st.selectbox(
            "Primary mode of transport",
            options=['walk/bicycle', 'public', 'private'],
            index=2
        )
        
        vehicle_type = 'none'
        vehicle_distance = 0
        
        if transport == 'private':
            vehicle_type = st.selectbox(
                "Vehicle type",
                options=['petrol', 'diesel', 'hybrid', 'electric', 'lpg'],
                index=0
            )
            vehicle_distance = st.slider(
                "Monthly vehicle distance (km)", 0, 5000, 500, step=50,
                help="Total km driven per month"
            )
        else:
            st.info("💡 No private vehicle - you're already reducing emissions!")
            vehicle_distance = st.slider(
                "Public transport usage (km/month)", 0, 2000, 100, step=50
            )

        air_travel = st.selectbox(
            "How often do you fly?",
            options=['never', 'rarely', 'frequently', 'very frequently'],
            index=1
        )

        st.markdown("#### 🍽️ Diet & Food")
        
        diet = st.selectbox(
            "Diet type",
            options=['vegan', 'vegetarian', 'pescatarian', 'omnivore'],
            index=3,
            help="Vegan has lowest carbon footprint, omnivore highest"
        )
        
        grocery_bill = st.slider(
            "Monthly grocery bill ($)", 50, 500, 150, step=10,
            help="Higher spending often correlates with more consumption"
        )

    with col_right:
        st.markdown("#### ⚡ Home & Energy")
        
        heating_source = st.selectbox(
            "Primary heating energy source",
            options=['electricity', 'natural gas', 'wood', 'coal'],
            index=0,
            help="Coal has highest emissions, electricity varies by grid"
        )
        
        energy_efficient = st.selectbox(
            "Do you use energy-efficient appliances?",
            options=['Yes', 'Sometimes', 'No'],
            index=1
        )
        
        tv_pc_hours = st.slider(
            "Daily TV/PC usage (hours)", 0, 16, 5, step=1
        )
        
        internet_hours = st.slider(
            "Daily internet usage (hours)", 0, 24, 8, step=1
        )

        st.markdown("#### 🛍️ Lifestyle")
        
        social_activity = st.selectbox(
            "Social activity frequency",
            options=['never', 'sometimes', 'often'],
            index=1,
            help="Going out, events, dining = more emissions"
        )
        
        new_clothes_monthly = st.slider(
            "New clothes purchased per month", 0, 30, 3, step=1,
            help="Fast fashion has a significant carbon footprint"
        )
        
        waste_bag_size = st.selectbox(
            "Waste bag size",
            options=['small', 'medium', 'large', 'extra large'],
            index=1
        )
        
        waste_bags_weekly = st.slider(
            "Waste bags per week", 0, 10, 2, step=1
        )

    # Additional inputs in expander
    with st.expander("🔧 Additional Details (Optional)"):
        body_type = st.selectbox("Body type", ['underweight', 'normal', 'overweight', 'obese'], index=1)
        sex = st.selectbox("Sex", ['male', 'female'], index=0)
        shower_freq = st.selectbox("Shower frequency", ['less frequently', 'daily', 'more frequently', 'twice a day'], index=1)

    # ── ENCODE VALUES (matching the training data encoding) ─────────────────

    # Map categorical values to encoded integers
    encode_map = {
        'body_type': {'normal': 0, 'obese': 1, 'overweight': 2, 'underweight': 3},
        'sex': {'female': 0, 'male': 1},
        'diet': {'omnivore': 0, 'pescatarian': 1, 'vegan': 2, 'vegetarian': 3},
        'how_often_shower': {'daily': 0, 'less frequently': 1, 'more frequently': 2, 'twice a day': 3},
        'heating_energy_source': {'coal': 0, 'electricity': 1, 'natural gas': 2, 'wood': 3},
        'transport': {'private': 0, 'public': 1, 'walk/bicycle': 2},
        'vehicle_type': {'diesel': 0, 'electric': 1, 'hybrid': 2, 'lpg': 3, 'none': 4, 'petrol': 5},
        'social_activity': {'never': 0, 'often': 1, 'sometimes': 2},
        'frequency_of_traveling_by_air': {'frequently': 0, 'never': 1, 'rarely': 2, 'very frequently': 3},
        'waste_bag_size': {'extra large': 0, 'large': 1, 'medium': 2, 'small': 3},
        'energy_efficiency': {'No': 0, 'Sometimes': 1, 'Yes': 2},
    }

    # Create input dictionary with encoded values
    user_inputs = {
        'body_type': encode_map['body_type'][body_type],
        'sex': encode_map['sex'][sex],
        'diet': encode_map['diet'][diet],
        'how_often_shower': encode_map['how_often_shower'][shower_freq],
        'heating_energy_source': encode_map['heating_energy_source'][heating_source],
        'transport': encode_map['transport'][transport],
        'vehicle_type': encode_map['vehicle_type'][vehicle_type],
        'social_activity': encode_map['social_activity'][social_activity],
        'monthly_grocery_bill': grocery_bill,
        'frequency_of_traveling_by_air': encode_map['frequency_of_traveling_by_air'][air_travel],
        'vehicle_monthly_distance_km': vehicle_distance,
        'waste_bag_size': encode_map['waste_bag_size'][waste_bag_size],
        'waste_bag_weekly_count': waste_bags_weekly,
        'how_long_tv_pc_daily_hour': tv_pc_hours,
        'how_many_new_clothes_monthly': new_clothes_monthly,
        'how_long_internet_daily_hour': internet_hours,
        'energy_efficiency': encode_map['energy_efficiency'][energy_efficient],
        'transport_distance_interaction': encode_map['transport'][transport] * vehicle_distance,
        'energy_efficiency_heating': encode_map['energy_efficiency'][energy_efficient] * encode_map['heating_energy_source'][heating_source],
    }

    # Store in session state
    st.session_state['user_inputs'] = user_inputs

    # Simple estimation (before ML prediction)
    # This is a rough estimate based on emission factors
    car_emissions = vehicle_distance * 0.21 * 12  # avg petrol car
    air_emissions = {'never': 0, 'rarely': 255, 'frequently': 510, 'very frequently': 1020}[air_travel]
    diet_emissions = {'vegan': 365, 'vegetarian': 730, 'pescatarian': 1095, 'omnivore': 1825}[diet]
    energy_emissions = {'electricity': 800, 'natural gas': 600, 'wood': 500, 'coal': 1200}[heating_source]
    lifestyle_emissions = grocery_bill * 3 + new_clothes_monthly * 25 + waste_bags_weekly * 52 * 15

    estimated_total = car_emissions + air_emissions + diet_emissions + energy_emissions + lifestyle_emissions
    st.session_state['estimated_co2'] = estimated_total

    # ── RESULT DISPLAY ───────────────────────────────────────────────────────

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1f3320'>", unsafe_allow_html=True)

    global_avg = 2260  # from our dataset

    # Color-code the result
    if estimated_total < 1500:
        color = "#22c55e"; level = "🟢 Low Emitter"; badge = "badge-green"
    elif estimated_total < 3000:
        color = "#fbbf24"; level = "🟡 Medium Emitter"; badge = "badge-yellow"
    else:
        color = "#f87171"; level = "🔴 High Emitter"; badge = "badge-red"

    c1, c2, c3 = st.columns([2, 1, 1], gap="medium")

    with c1:
        st.markdown(f"""
        <div class='co2-meter'>
            <div style='font-size:0.75rem; color:#6b7280; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem'>
                Estimated Annual Carbon Footprint
            </div>
            <div class='co2-value' style='color:{color}'>{estimated_total:,.0f}</div>
            <div style='font-size:1rem; color:#6b7280; margin-top:0.25rem'>kg CO₂ / year</div>
            <div style='margin-top:1rem'>
                <span class='badge {badge}' style='font-size:0.8rem; padding:0.4rem 1.2rem'>{level}</span>
            </div>
            <div style='font-size:0.7rem; color:#6b7280; margin-top:0.75rem'>
                ℹ️ This is a rough estimate. Go to AI Prediction for ML-powered accuracy.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        pct = round((estimated_total / global_avg) * 100, 1)
        delta_pct = f"{pct - 100:+.1f}% vs dataset avg"
        st.metric("vs Dataset Average", f"{pct}%", delta_pct, delta_color="inverse")
        st.metric("Dataset Average", "2,260 kg", "From 10K profiles")

    with c3:
        trees_needed = int(estimated_total / 21)
        months = round(12 * estimated_total / (global_avg or 1), 1)
        st.metric("Trees to Offset", f"{trees_needed:,}", "trees/year needed")
        st.metric("Time Equivalent", f"{months:.1f} mo", "of avg person")

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("✅ Your data is saved! Go to **🤖 AI Prediction** to see what the trained ML models predict for you.")
    
    st.info("💡 **How the estimate works:** We use emission factors from IPCC/IEA for each category. "
            "The ML model in the next page uses your exact input pattern to predict more accurately based on "
            "10,000 real profiles.")