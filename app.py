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
# Using a high-fidelity 3D medical render of a heart/vascular environment
background_image_url = "https://images.unsplash.com/photo-1559757175-5700dde675bc?q=80&w=2560&auto=format&fit=crop"

page_bg_img = f'''
<style>
/* Dark gradient mask to ensure your white text pops */
.stApp {{
    background: linear-gradient(rgba(10, 5, 5, 0.5), rgba(10, 5, 5, 0.5)), url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* High-contrast text with shadow for legibility */
[data-testid="stMain"] h1, 
[data-testid="stMain"] h2, 
[data-testid="stMain"] h3, 
[data-testid="stMain"] h4, 
[data-testid="stMain"] p, 
[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] {{
    color: #FFFFFF !important;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.9);
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# [KEEP THE REST OF YOUR EXISTING FUNCTIONS (show_landing_page, show_dashboard, etc.) UNCHANGED]
