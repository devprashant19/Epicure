

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

# --- UI STYLING (UPGRADED & FIXED) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background-color: #0B090C;
            color: #EAE6F0;
        }

        #MainMenu, footer, header { visibility: hidden; }
        .stDeployButton { display: none !important; }

        .title {
            text-align: center;
            font-size: 3.5rem;
            font-weight: 700;
            padding-top: 2rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #A99EB8;
            padding-bottom: 2rem;
        }

        .result-card {
            background-color: #16161a;
            border: 1px solid #242629;
            border-radius: 16px;
            margin-bottom: 2rem;
            transition: all 0.2s ease-in-out;
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 1.5rem;
            padding: 1.5rem;
        }
        .result-card:hover {
            border-color: #7f5af0;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .card-image img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
        }
        .card-info {
            display: flex;
            flex-direction: column;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .card-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: #fffffe;
            margin: 0;
            line-height: 1.2;
        }
        .card-rating {
            background-color: #2cb67d;
            color: #fffffe;
            padding: 0.3rem 0.8rem;
            border-radius: 1rem;
            font-weight: 600;
            font-size: 1rem;
            flex-shrink: 0;
            margin-left: 1rem;
        }
        .card-details, .card-links {
            font-size: 1rem;
            color: #94a1b2;
            margin: 0.5rem 0;
        }
        .card-links span, .card-links a {
            color: #7f5af0;
            text-decoration: none;
            margin-right: 1.5rem;
            font-weight: 600;
        }
      
        .card-review {
    overflow: hidden; /* Prevent text overflow */
    white-space: normal; /* Allow text to wrap */
    word-wrap: break-word; /* Break long words */
    max-width: 100%; /* Control max width */
    padding: 10px; /* Optional padding for better appearance */
    margin: 10px 0; /* Space around the review */
    border: 1px solid #ccc; /* Optional styling */
    border-radius: 5px; /* Optional rounded corners */
}
    </style>
""", unsafe_allow_html=True)


# --- API & HELPER FUNCTIONS ---

@st.cache_data(ttl=3600)
def get_llm_params(query):
    """Uses Gemini to parse a query into structured search parameters."""
    prompt = f"""
    You are an expert restaurant recommendation assistant. From the user's query: "{query}", extract the following entities:
    - "keyword": The main food, cuisine, or type of place.
    - "vibe": Any specific ambiance or occasion (e.g., "romantic", "casual", "instagram-worthy").
    - "diet": Specifically identify if the user asks for "veg" or "non-veg". Default to "any".
    - "location": The city or area to search in.
    Return ONLY a single, compact JSON object. If a value isn't mentioned, set it to null.
    """
    try:
        response = llm.generate_content(prompt)
        json_str = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(json_str)
    except Exception:
        return {"keyword": query, "location": None, "vibe": None, "diet": "any"}
