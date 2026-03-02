"""
Configuration and constants for the Tourism Engine app
"""

import streamlit as st
import uuid

# =========================
# STREAMLIT PAGE CONFIG
# =========================
def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="AI Cultural Tourism Engine",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# =========================
# SESSION STATE INITIALIZATION
# =========================
def initialize_session_state():
    """Initialize all session state variables"""
    session_defaults = {
        'ranked_results': None,
        'user_input': None,
        'session_id': str(uuid.uuid4()),
        'firebase_doc_id': None,
        'show_itinerary_form': False,
        'personalization_complete': False,
        'pdf_buffer': None,
        'current_itinerary': None,
        'current_city': None,
        'current_user_input': None,
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# =========================
# GLOBAL FLAGS
# =========================
FIREBASE_AVAILABLE = False
GEMINI_AVAILABLE = False
GEMINI_ERROR_MESSAGE = ""

# =========================
# API CONFIGURATION
# =========================
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_WEATHER_TEMP = 0.7
GEMINI_WEATHER_TOKENS = 200
GEMINI_TRANSLATE_TEMP = 0.3
GEMINI_TRANSLATE_TOKENS = 500
GEMINI_ITINERARY_TEMP = 0.7
GEMINI_ITINERARY_TOKENS = 1000

# =========================
# DATA PATHS
# =========================
MASTER_DATA_PATH = "datasets/master_destinations.csv"
PATTERNS_DATA_PATH = "datasets/user_preference_patterns.csv"
FEEDBACK_DIR = "feedback"
FEEDBACK_FILE = "feedback/feedback.csv"

# =========================
# WEIGHTS AND SCORING
# =========================
DEFAULT_WEIGHTS = {
    "experience": 0.6,
    "rating": 0.25,
    "duration": 0.15
}

# =========================
# AGE GROUPS
# =========================
AGE_GROUPS = {
    (0, 25): "18-25",
    (26, 35): "26-35",
    (36, 45): "36-45",
    (46, 55): "46-55",
    (56, 150): "56+"
}

# =========================
# WEATHER ICONS
# =========================
WEATHER_ICONS = {
    "Cold": "❄️",
    "Pleasant": "🌤️",
    "Warm": "☀️"
}
