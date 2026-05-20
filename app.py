import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Liposome Digital Twin", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Landing"

# --- CINEMATIC BACKGROUND & TEXT READABILITY CSS ---
background_image_url = "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?q=80&w=2560&auto=format&fit=crop"

page_bg_img = f'''
<style>
.stApp {{
    background: linear-gradient(rgba(5, 5, 10, 0.5), rgba(5, 5, 10, 0.5)), url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stMain"] h1, 
[data-testid="stMain"] h2, 
[data-testid="stMain"] h3, 
[data-testid="stMain"] h4, 
[data-testid="stMain"] p, 
[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] {{
    color: #FFFFFF !important;
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
        st.write(
            "Welcome to the research portal. This tool allows you to simulate the efficacy and stability of various liposome formulations under high shear stress environments.")
        st.write("---")

        if st.button("Enter Simulation Dashboard ➡️", type="primary", use_container_width=True):
            st.session_state.current_page = "Dashboard"
            st.rerun()


# ==========================================
# PAGE 2: MAIN DASHBOARD
# ==========================================
def show_dashboard():
    # --- HEADER WITH BACK BUTTON ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📊 Simulation Dashboard")
    with col2:
        if st.button("⬅️ Return Home", use_container_width=True):
            st.session_state.current_page = "Landing"
            st.rerun()

    st.markdown("Enter your precise lipid formulation to simulate efficacy under high shear stress.")

    # --- SIDEBAR: LIPID CONCENTRATIONS ---
    st.sidebar.header("Lipid Formulation (mM)")
    st.sidebar.markdown("Adjust the concentrations to create your specific liposome mixture.")

    cholesterol = st.sidebar.number_input("Cholesterol-rich", min_value=0.0, max_value=50.0, value=10.0, step=0.5)
    dppc = st.sidebar.number_input("DPPC-based", min_value=0.0, max_value=50.0, value=20.0, step=0.5)
    dppe = st.sidebar.number_input("DPPE-based", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    popc = st.sidebar.number_input("POPC-based", min_value=0.0, max_value=50.0, value=5.0, step=0.5)
    pope = st.sidebar.number_input("POPE-based", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

    st.sidebar.divider()
    st.sidebar.header("Environmental Factors")
    shear_stress = st.sidebar.slider("Shear Stress (dyn/cm²)", 10, 500, 70)

    # --- MAIN DASHBOARD LAYOUT ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Current Mixture Profile")

        total_conc = cholesterol + dppc + dppe + popc + pope

        if total_conc == 0:
            st.warning("⚠️ Total lipid concentration is 0. Please add lipids to the formulation.")
        else:
            st.write(f"**Total Concentration:** {total_conc} mM")
            st.write(f"**Shear Stress Applied:** {shear_stress} dyn/cm²")

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
            st.caption("Waiting for DeepXDE model integration...")

    with col_right:
        st.subheader("Comparative Activation Response")

        # --- ADVANCED COMPARATIVE MODEL ---
        # 1. Base Control Line (Worst-case scenario baseline under this mechanical shear stress)
        base_activation = (shear_stress / 500) * 45 + 25
        time_steps = np.arange(0, 20)
        control_curve = base_activation + np.log1p(time_steps) * 6.0

        # 2. Stabilized Line (Your actual custom composition calculations)
        stabilization_effect = (
                (cholesterol * 0.45) +  # High packing effect
                (dppc * 0.28) +  # Saturated protection
                (dppe * 0.15) +
                (popc * 0.08) +
                (pope * 0.10)
        )
        stabilized_curve = control_curve - stabilization_effect

        # Apply strict experimental clipping & minimal clean noise
        control_final = np.clip(control_curve + np.random.normal(0, 0.2, 20), 0, 100)
        stabilized_final = np.clip(stabilized_curve + np.random.normal(0, 0.2, 20), 0, 100)

        # 3. Structural formatting for comparison view inside a single DataFrame
        chart_data = pd.DataFrame({
            'Time (ms)': np.concatenate([time_steps, time_steps]),
            'Activation (%)': np.concatenate([control_final, stabilized_final]),
            'Formulation Profile': ['Control (Fluid-only Baseline)'] * 20 + ['Your Stabilized Formulation'] * 20
        })

        # Render a dual-line chart using a high-contrast palette
        fig_line = px.line(
            chart_data,
            x='Time (ms)',
            y='Activation (%)',
            color='Formulation Profile',
            markers=True,
            color_discrete_sequence=["#FF4B4B", "#00CC96"]  # Red for bad control, Green for stabilization
        )

        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Display a live metric calculation of the protective reduction benefit
        peak_reduction = max(0.0, float(control_final[-1] - stabilized_final[-1]))
        st.metric(
            label="Total Activation Reduction Efficiency",
            value=f"{peak_reduction:.1f}% Lower",
            delta="Membrane Shielded"
        )


# ==========================================
# APP ROUTING LOGIC
# ==========================================
if st.session_state.current_page == "Landing":
    show_landing_page()
elif st.session_state.current_page == "Dashboard":
    show_dashboard()
