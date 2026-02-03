import streamlit as st

# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Cultural Tourism Platform",
    layout="wide"
)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
def home_page():
    st.title("🌍 AI-Powered Cultural Tourism Platform")
    st.write(
        """
        Plan personalized cultural trips using AI.
        
        This platform generates:
        - Personalized destinations
        - Smart itineraries
        - PDF travel plans
        - Travel recap videos
        - Multilingual AI chatbot assistance
        """
    )

# -------------------------------------------------
# PERSONALIZATION PAGE
# -------------------------------------------------
def personalization_page():
    st.title("🧭 Travel Personalization")
    st.subheader("Tell us about your travel preferences")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 10, 80)
        interests = st.multiselect(
            "Interests",
            ["Culture", "Adventure", "Nature", "Food", "History", "Beaches"]
        )
        duration = st.selectbox("Trip Duration (days)", [3, 5, 7, 10])

    with col2:
        season = st.selectbox(
            "Preferred Season",
            ["Summer", "Winter", "Spring", "Autumn"]
        )
        weather = st.selectbox(
            "Preferred Weather",
            ["Cold", "Moderate", "Hot"]
        )
        accessibility = st.checkbox("Accessibility needs")
        language = st.selectbox(
            "Preferred Language",
            ["English", "Hindi", "French", "Japanese"]
        )

    if st.button("Generate Personalized Destinations"):
        st.success("Showing AI-recommended destinations")

        # ---- BACKEND PLACEHOLDER ----
        sample_destinations = [
            {"name": "Kyoto", "country": "Japan", "type": "Culture"},
            {"name": "Paris", "country": "France", "type": "History"},
            {"name": "Bali", "country": "Indonesia", "type": "Nature"}
        ]

        for place in sample_destinations:
            st.markdown(f"### {place['name']} ({place['country']})")
            st.write(f"Experience Type: {place['type']}")
            st.info("AI-generated description will appear here.")

            col1, col2 = st.columns(2)
            with col1:
                st.button(f"👍 Like {place['name']}")
            with col2:
                st.button(f"👎 Dislike {place['name']}")

# -------------------------------------------------
# ITINERARY PAGE
# -------------------------------------------------
def itinerary_page():
    st.title("📅 Personalized Itinerary")

    st.write("Your AI-generated day-wise itinerary")

    # ---- BACKEND PLACEHOLDER ----
    itinerary = {
        "Day 1": "Arrival, cultural walking tour, local cuisine",
        "Day 2": "Museum visit, heritage site exploration",
        "Day 3": "Nature excursion and relaxation"
    }

    for day, plan in itinerary.items():
        with st.expander(day):
            st.write(plan)
            st.info("Weather & seasonal notes will appear here")

    st.radio(
        "Would you like to modify this itinerary?",
        ["Yes", "No"]
    )

# -------------------------------------------------
# SMART RECOMMENDATIONS PAGE
# -------------------------------------------------
def recommendations_page():
    st.title("✨ Smart Recommendations")

    st.write("Similar destinations you may like")

    # ---- BACKEND PLACEHOLDER ----
    recommendations = [
        {"name": "Rome", "country": "Italy"},
        {"name": "Istanbul", "country": "Turkey"},
        {"name": "Athens", "country": "Greece"}
    ]

    for rec in recommendations:
        st.markdown(f"### {rec['name']} ({rec['country']})")
        st.write("AI-generated recommendation reason will appear here.")

        col1, col2 = st.columns(2)
        with col1:
            st.button(f"👍 Like {rec['name']}")
        with col2:
            st.button(f"👎 Dislike {rec['name']}")

# -------------------------------------------------
# PDF GENERATOR PAGE
# -------------------------------------------------
def pdf_page():
    st.title("📄 PDF Itinerary Generator")

    st.write("Download your personalized travel itinerary")

    st.info("PDF generation logic will be connected here")

    st.button("Download Itinerary PDF")

# -------------------------------------------------
# VIDEO GENERATOR PAGE
# -------------------------------------------------
def video_page():
    st.title("🎬 Travel Recap Video")

    st.write("AI-generated video summary of your trip")

    st.warning("Video preview will appear here once generated")

    st.button("Generate Travel Video")

# -------------------------------------------------
# CHATBOT PAGE
# -------------------------------------------------
def chatbot_page():
    st.title("💬 Multilingual Travel Chatbot")

    st.write("Ask anything about your trip")

    user_input = st.text_input("Type your question here")

    if st.button("Send"):
        st.success("AI Response:")
        st.write("Gemini-generated response will appear here")

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------
pages = {
    "Home": home_page,
    "Personalization": personalization_page,
    "Itinerary": itinerary_page,
    "Recommendations": recommendations_page,
    "PDF Generator": pdf_page,
    "Video Generator": video_page,
    "Chatbot": chatbot_page
}

choice = st.sidebar.selectbox("Navigate", list(pages.keys()))
pages[choice]()
