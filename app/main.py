

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
