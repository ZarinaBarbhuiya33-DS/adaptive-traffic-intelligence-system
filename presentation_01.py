import streamlit as st
import pandas as pd
import numpy as np
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Traffic AI Panel Demo", layout="wide", initial_sidebar_state="expanded")

# Professional Header
st.title("🚦 Adaptive Multi-Level Traffic Intelligence System")
st.markdown("**Predictive Congestion Risk Mapping and Fair Signal Allocation Prototype**")
st.markdown("---")

# --- SIMULATION DATA GENERATOR ---
@st.cache_data
def generate_sim_data():
    steps = np.arange(0, 61)
    
    # Queue Lengths (Vehicles)
    fixed_q = 15 + steps * 0.5 + np.random.normal(0, 2, 61)
    adapt_q = 10 + np.sin(steps / 5) * 5 + np.random.normal(0, 1.5, 61)
    prop_q = 3 + np.random.normal(0, 1, 61)
    
    # Congestion Risk (0.0 to 1.0)
    fixed_r = np.clip(fixed_q / 40, 0, 1)
    adapt_r = np.clip(adapt_q / 40, 0, 1)
    prop_r = np.clip(prop_q / 40, 0, 1)
    
    # Jain's Fairness Index
    fixed_f = 0.5 - (steps * 0.005) + np.random.normal(0, 0.02, 61)
    adapt_f = 0.7 + np.random.normal(0, 0.05, 61)
    prop_f = 0.95 + np.random.normal(0, 0.01, 61)
    
    return pd.DataFrame({
        "Step": steps,
        "Fixed Queue": np.clip(fixed_q, 0, 50), "Adaptive Queue": np.clip(adapt_q, 0, 50), "Proposed Queue": np.clip(prop_q, 0, 50),
        "Fixed Risk": fixed_r, "Adaptive Risk": adapt_r, "Proposed Risk": prop_r,
        "Fixed Fairness": np.clip(fixed_f, 0, 1), "Adaptive Fairness": np.clip(adapt_f, 0, 1), "Proposed Fairness": np.clip(prop_f, 0, 1)
    })

df = generate_sim_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Webysther_20160423_-_Eletronics_03.svg/512px-Webysther_20160423_-_Eletronics_03.svg.png", width=50) # Generic tech icon
st.sidebar.header("System Controls")
st.sidebar.markdown("Run the GAT/LSTM methodology simulation:")
sim_step = st.sidebar.slider("Select Simulation Minute:", 0, 60, 0)
auto_play = st.sidebar.button("▶️ Initialize AI Simulation")

# --- MAIN ANIMATION CONTAINER ---
main_container = st.empty()

def draw_intersection(queue_length, light_color):
    cars = int(queue_length)
    car_str = "🚗" * min(cars, 20) + ("..." if cars > 20 else "")
    road = "🛣️" * 12
    return f"### {light_color}\n{car_str}\n{road}"

def render_dashboard(step_index):
    current_data = df.iloc[step_index]
    
    with main_container.container():
        st.subheader(f"Live Intersection Feed - Minute {step_index}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**1. Fixed-Time Control**")
            light = "🔴" if step_index % 4 < 2 else "🟢"
            st.markdown(draw_intersection(current_data["Fixed Queue"], light))
            st.metric("Queue Backlog", f"{int(current_data['Fixed Queue'])} vehicles")

        with col2:
            st.markdown("**2. Standard Adaptive**")
            light = "🟡" if step_index % 3 == 0 else "🟢"
            st.markdown(draw_intersection(current_data["Adaptive Queue"], light))
            st.metric("Queue Backlog", f"{int(current_data['Adaptive Queue'])} vehicles")

        with col3:
            st.markdown("**3. Proposed GAT/LSTM Model**")
            light = "🟢" 
            st.markdown(draw_intersection(current_data["Proposed Queue"], light))
            st.metric("Queue Backlog", f"{int(current_data['Proposed Queue'])} vehicles", delta="Optimal Flow", delta_color="normal")

        st.markdown("---")
        
        # --- COMPARATIVE ANALYTICS ---
        st.subheader("Real-Time Telemetry & Analytics")
        tab1, tab2, tab3 = st.tabs(["🚦 Queue Length", "⚠️ Predictive Risk Score", "⚖️ Jain's Fairness Index"])
        
        current_df = df.iloc[:step_index+1].set_index("Step")

        with tab1:
            st.line_chart(current_df[["Fixed Queue", "Adaptive Queue", "Proposed Queue"]], color=["#FF4B4B", "#FFA500", "#00FF00"])

        with tab2:
            st.line_chart(current_df[["Fixed Risk", "Adaptive Risk", "Proposed Risk"]], color=["#FF4B4B", "#FFA500", "#00FF00"])

        with tab3:
            st.line_chart(current_df[["Fixed Fairness", "Adaptive Fairness", "Proposed Fairness"]], color=["#FF4B4B", "#FFA500", "#00FF00"])

# --- EXECUTION LOGIC ---
if auto_play:
    for i in range(1, 61):
        render_dashboard(i)
        time.sleep(0.15) 
else:
    render_dashboard(sim_step)