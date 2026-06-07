

import streamlit as st
import pandas as pd
import requests
import json
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Epicure AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- API CONFIGURATION ---
try:
    # Ensure you have your API keys in Streamlit's secrets
    GOOGLE_API_KEY = st.secrets["google"]["api_key"]
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    llm = genai.GenerativeModel('gemini-1.5-flash')
except (KeyError, AttributeError):
    st.error("🚨 API key not found. Please ensure 'google' and 'gemini' keys are in your secrets.toml.")
    st.stop()

