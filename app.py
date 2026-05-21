import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Liposome Digital Twin", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Landing"

# --- CINEMATIC BIOMEDICAL BACKGROUND ---
# High-fidelity 3D render of a blood vessel / cellular environment
background_image_url = "https://images.unsplash.com/photo-1576086213369-97a306d36557?q=80&w=2560&auto=format&fit=crop"

page_bg_img = f'''
<style>
/* Dark crimson mask - opacity reduced so the background cells are more visible */
.stApp {{
    background: linear-gradient(rgba(20, 5, 5, 0.65), rgba(10, 5, 5, 0.75)), url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Ensure all text in the main body is high-contrast white with a strong drop shadow */
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp div {{
    text-shadow: 2px 2px 6px rgba(0,0,0,1.0);
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ==========================================
# PAGE 1: LANDING PAGE
# ==========================================
def show_landing_page():
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🧪 Liposome-Platelet Activation")
        st.markdown("### Digital Twin Simulation Engine")
        st.write("Welcome. Simulate the efficacy of liposome formulations in μM concentration ranges.")
        if st.button("Enter Simulation Dashboard ➡️", type="primary", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()

# ==========================================
# PAGE 2: MAIN DASHBOARD
# ==========================================
def show_dashboard():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📊 Simulation Dashboard")
    with col2:
        if st.button("⬅️ Return Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()
            
    # --- SIDEBAR: LIPID CONCENTRATIONS IN μM ---
    st.sidebar.header("Lipid Formulation (μM)")
    cholesterol = st.sidebar.number_input("Cholesterol-rich (μM)", min_value=0.0, max_value=1000.0, value=100.0, step=5.0)
    dppc = st.sidebar.number_input("DPPC-based (μM)", min_value=0.0, max_value=1000.0, value=200.0, step=5.0)
    dppe = st.sidebar.number_input("DPPE-based (μM)", min_value=0.0, max_value=1000.0, value=0.0, step=5.0)
    popc = st.sidebar.number_input("POPC-based (μM)", min_value=0.0, max_value=1000.0, value=50.0, step=5.0)
    pope = st.sidebar.number_input("POPE-based (μM)", min_value=0.0, max_value=1000.0, value=0.0, step=5.0)
    shear_stress = st.sidebar.slider("Shear Stress (dyn/cm²)", 10, 500, 70)

    # --- MAIN DASHBOARD LAYOUT ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Current Mixture Profile")
        total_conc = cholesterol + dppc + dppe + popc + pope
        st.write(f"**Total Concentration:** {total_conc:.2f} μM")
        
        mixture_data = pd.DataFrame({
            "Lipid": ["Cholesterol", "DPPC", "DPPE", "POPC", "POPE"],
            "Concentration": [cholesterol, dppc, dppe, popc, pope]
        })
        fig_pie = px.pie(mixture_data, values='Concentration', names='Lipid', hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_pie, use_container_width=True)

        if st.button("▶ Run PINN Simulation", type="primary"):
            st.success("Simulation Engine Triggered!")

    with col_right:
        st.subheader("Comparative Activation Response")
        base_activation = (shear_stress / 500) * 45 + 25
        time_steps = np.arange(0, 20)
        
        # Math adjusted for μM scale factor
        stabilization_effect = ((cholesterol * 0.045) + (dppc * 0.028) + (dppe * 0.015) + (popc * 0.008) + (pope * 0.010))
        stabilized_curve = base_activation + np.log1p(time_steps) * 6.0 - stabilization_effect
        
        chart_data = pd.DataFrame({
            'Time (ms)': np.concatenate([time_steps, time_steps]),
            'Activation (%)': np.concatenate([np.clip(base_activation + np.log1p(time_steps) * 6, 0, 100), np.clip(stabilized_curve, 0, 100)]),
            'Formulation Profile': ['Control (Fluid-only Baseline)'] * 20 + ['Your Stabilized Formulation'] * 20
        })
        
        fig_line = px.line(chart_data, x='Time (ms)', y='Activation (%)', color='Formulation Profile', markers=True, color_discrete_sequence=["#FF4B4B", "#00CC96"])
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_line, use_container_width=True)
        
        st.metric(label="Total Activation Reduction Efficiency", value=f"{min(stabilization_effect, 100):.1f}% Lower")

if st.session_state.current_page == "Landing":
    show_landing_page()
elif st.session_state.current_page == "Dashboard":
    show_dashboard()
