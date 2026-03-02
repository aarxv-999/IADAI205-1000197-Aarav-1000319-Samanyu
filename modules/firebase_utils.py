"""
Firebase utilities for storing and retrieving tourism recommendations
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Global state
FIREBASE_AVAILABLE = False
db = None


# =========================
# FIREBASE INITIALIZATION
# =========================
def initialize_firebase():
    """Initialize Firebase with proper error handling"""
    global FIREBASE_AVAILABLE, db

    try:
        if firebase_admin._apps:
            FIREBASE_AVAILABLE = True
            return firestore.client()

        if "FIREBASE_CREDENTIALS" not in st.secrets:
            st.warning("Firebase credentials not found. Recommendations won't be saved.")
            return None

        firebase_creds = dict(st.secrets["FIREBASE_CREDENTIALS"])

        if "private_key" in firebase_creds:
            firebase_creds["private_key"] = str(firebase_creds["private_key"])

        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

        FIREBASE_AVAILABLE = True
        db = firestore.client()
        return db

    except Exception as e:
        st.warning(f"Firebase initialization failed: {str(e)}")
        FIREBASE_AVAILABLE = False
        return None


# =========================
# SAVE RECOMMENDATIONS
# =========================
def save_to_firebase(user_input, ranked_results, session_id, db):
    """Save recommendations to Firebase"""
    if not FIREBASE_AVAILABLE or db is None:
        return None

    try:
        recommendations = []
        for _, row in ranked_results.iterrows():
            recommendations.append({
                "city": row["city"],
                "country": row["country"],
                "continent": row["continent"],
                "rating": float(row["avg_rating"]),
                "match_score": float(row["final_score"]),
                "budget_level": row["budget_level"],
                "ideal_duration": int(row["ideal_duration_days"]),
                "description": row["description"],
                "culture_score": float(row.get("culture_score", 0)),
                "adventure_score": float(row.get("adventure_score", 0)),
                "nature_score": float(row.get("nature_score", 0)),
                "beach_score": float(row.get("beach_score", 0))
            })

        doc_data = {
            "session_id": session_id,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "user_preferences": {
                "age": user_input["age"],
                "interest": user_input["interest"],
                "duration": user_input["duration"],
                "weather": user_input["weather"],
                "season": user_input["season"],
                "budget": user_input["budget"]
            },
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "itinerary_generated": False
        }

        doc_ref = db.collection("tourism_recommendations").add(doc_data)
        return doc_ref[1].id

    except Exception as e:
        st.error(f"Failed to save to Firebase: {e}")
        return None


# =========================
# RETRIEVE RECOMMENDATIONS
# =========================
def get_session_recommendations(session_id, db):
    """Get recommendations for current session from Firebase"""
    if not FIREBASE_AVAILABLE or db is None:
        return None

    try:
        docs = db.collection("tourism_recommendations") \
            .where("session_id", "==", session_id) \
            .order_by("timestamp", direction=firestore.Query.DESCENDING) \
            .limit(1) \
            .stream()

        for doc in docs:
            return doc.to_dict()

        return None

    except Exception as e:
        st.error(f"Failed to retrieve session data: {e}")
        return None


# =========================
# HELPER FUNCTIONS
# =========================
def is_firebase_available():
    """Check if Firebase is available"""
    return FIREBASE_AVAILABLE


def get_db_client():
    """Get Firebase database client"""
    return db
