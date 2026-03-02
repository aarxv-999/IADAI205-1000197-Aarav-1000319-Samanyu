"""
Data utilities for loading, filtering, and ranking tourism destinations
"""

import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime
from config import (
    MASTER_DATA_PATH,
    PATTERNS_DATA_PATH,
    DEFAULT_WEIGHTS,
    AGE_GROUPS,
    FEEDBACK_DIR,
    FEEDBACK_FILE,
)

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_data():
    """Load datasets with error handling"""
    try:
        master = pd.read_csv(MASTER_DATA_PATH)
        patterns = pd.read_csv(PATTERNS_DATA_PATH)
        return master, patterns
    except FileNotFoundError as e:
        st.error(f"Dataset not found: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()


# =========================
# USER PROFILE UTILITIES
# =========================
def get_age_group(age):
    """Map age to age group category"""
    for (min_age, max_age), group in AGE_GROUPS.items():
        if min_age <= age <= max_age:
            return group
    return "56+"


def get_user_pattern(patterns, interest, age_group):
    """Get user preference pattern from dataset"""
    if patterns is None:
        return None
    row = patterns[
        (patterns["interest"] == interest) &
        (patterns["age_group"] == age_group)
    ]
    return row.iloc[0] if len(row) > 0 else None


def get_dynamic_weights(pattern_row):
    """Get dynamic weights for ranking (extensible for future ML)"""
    if pattern_row is None:
        return DEFAULT_WEIGHTS
    # Can be extended to use pattern_row data for dynamic weight calculation
    return DEFAULT_WEIGHTS


# =========================
# FILTERING AND RANKING
# =========================
def filter_cities(df, user):
    """Filter cities based on user preferences"""
    return df[
        (df["budget_level"] == user["budget"]) &
        (df[f"climate_{user['season'].lower()}_label"] == user["weather"])
    ]


def rank_cities(df, user, patterns):
    """Rank and score filtered cities based on user profile"""
    age_group = get_age_group(user["age"])
    pattern_row = get_user_pattern(patterns, user["interest"], age_group)
    weights = get_dynamic_weights(pattern_row)

    df = df.copy()
    df["rating_norm"] = df["avg_rating"] / 5
    df["experience_match"] = df[f"{user['interest'].lower()}_score"]

    df["duration_match"] = 1 - (
        abs(df["ideal_duration_days"] - user["duration"]) /
        df["ideal_duration_days"]
    ).clip(0, 1)

    df["final_score"] = (
        weights["experience"] * df["experience_match"] +
        weights["rating"] * df["rating_norm"] +
        weights["duration"] * df["duration_match"]
    )

    return df.sort_values("final_score", ascending=False)


# =========================
# IMAGE UTILITIES
# =========================
def get_city_image(city):
    """Generate consistent image URL for city based on hash"""
    city_hash = int(hashlib.md5(city.encode()).hexdigest(), 16)
    image_id = city_hash % 1000
    return f"https://picsum.photos/seed/{image_id}/800/500"


# =========================
# FEEDBACK
# =========================
def save_feedback(city, feedback, session_id, db=None):
    """Save user feedback locally and to Firebase if available"""
    os.makedirs(FEEDBACK_DIR, exist_ok=True)

    row = {
        "city": city,
        "feedback": feedback,
        "timestamp": datetime.now()
    }

    # Save to CSV
    try:
        df = pd.read_csv(FEEDBACK_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=row.keys())

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

    # Save to Firebase if available
    if db is not None:
        try:
            from firebase_admin import firestore
            db.collection("user_feedback").add({
                "session_id": session_id,
                "city": city,
                "feedback": feedback,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            st.warning(f"Failed to save feedback to Firebase: {e}")
