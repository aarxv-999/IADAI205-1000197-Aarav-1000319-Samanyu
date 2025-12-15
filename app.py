import streamlit as st

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Cultural Tourism Platform",
    layout="wide"
)

# -----------------------------------------------------
# PERSONALIZATION PAGE (MAIN UI REQUIRED FOR WEEK 3)
# -----------------------------------------------------
def personalization_page():
    st.title("Travel Personalization")
    st.subheader("Tell us about your travel preferences")

    # -------- User Input Form --------
    age = st.slider("Select your age", 10, 80)

    interests = st.multiselect(
        "Choose your interests:",
        ["Culture", "Adventure", "Nature", "Food", "History", "Beaches", "Shopping"]
    )

    duration = st.selectbox("Trip Duration (days):", [3, 5, 7, 10])

    season = st.selectbox(
        "Preferred Travel Season:",
        ["Summer", "Winter", "Spring", "Autumn"]
    )

    weather_pref = st.selectbox(
        "Preferred Weather:",
        ["Cold", "Moderate", "Hot"]
    )

    accessibility = st.checkbox("Accessibility needs")

    language = st.selectbox(
        "Preferred Language:",
        ["English", "Hindi", "French", "Japanese"]
    )

    # -------- Button --------
    if st.button("Generate Suggestions"):
        st.info("Backend will generate personalized travel suggestions here…")

        st.subheader("Suggested Destinations")

        # SAMPLE OUTPUT (Placeholder – backend connects later)
        sample_results = [
            {"name": "Kyoto", "country": "Japan"},
            {"name": "Paris", "country": "France"},
            {"name": "Bali", "country": "Indonesia"}
        ]

        for place in sample_results:
            st.write(f"### {place['name']} ({place['country']})")
            st.write("Description: (AI generated text will appear here)")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"👍 Like {place['name']}"):
                    st.success(f"Feedback saved for {place['name']}")

            with col2:
                if st.button(f"👎 Dislike {place['name']}"):
                    st.error(f"Feedback saved for {place['name']}")


# -----------------------------------------------------
# SIMPLE PLACEHOLDER PAGES FOR WEEKS 1–4
# -----------------------------------------------------
def home_page():
    st.title("AI Cultural Tourism Platform")
    st.write("Welcome! Explore destinations powered by AI.")
    st.write("Use the sidebar to navigate to different features.")


def itinerary_page():
    st.title("Itinerary Page (Coming Soon)")
    st.write("Your personalized itinerary will appear here in Week 4–5.")


def recommendations_page():
    st.title("Recommendations Page (Coming Soon)")
    st.write("Smart AI suggestions will be shown here in Week 5.")


def pdf_page():
    st.title("PDF Generator (Coming Soon)")
    st.write("PDF itinerary export will be added in Week 6.")


def video_page():
    st.title("Travel Video Generator (Coming Soon)")
    st.write("AI-generated travel video will be added in Week 7.")


def chatbot_page():
    st.title("Multilingual Chatbot (Coming Soon)")
    st.write("The AI travel assistant will be available in Week 8.")


# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
pages = {
    "Home": home_page,
    "Personalization": personalization_page,
    "Itinerary": itinerary_page,
    "Recommendations": recommendations_page,
    "PDF Generator": pdf_page,
    "Video Generator": video_page,
    "Chatbot": chatbot_page
}

selection = st.sidebar.selectbox("Navigate", list(pages.keys()))
pages[selection]()   # call the selected page function
