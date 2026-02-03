import streamlit as st

# -------------------------------------------------
# APP CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="AI Cultural Tourism Platform",
    layout="wide"
)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
def home_page():
    st.title("AI Cultural Tourism Platform")
    st.write("Plan personalized cultural trips powered by AI.")
    st.write("Use the sidebar to navigate through the application.")

# -------------------------------------------------
# PERSONALIZATION PAGE (MAIN AARAV UI WORK)
# -------------------------------------------------
def personalization_page():
    st.title("Travel Personalization")
    st.subheader("Tell us about your travel preferences")

    age = st.slider("Select your age", 10, 80)

    interests = st.multiselect(
        "Choose your interests",
        ["Culture", "Adventure", "Nature", "Food", "History", "Beaches"]
    )

    duration = st.selectbox("Trip Duration (days)", [3, 5, 7, 10])

    season = st.selectbox(
        "Preferred Travel Season",
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

    if st.button("Generate Suggestions"):
        st.info("Personalized destinations will appear here.")

        st.subheader("Suggested Destinations")

        # Placeholder results (backend will replace later)
        sample_results = [
            {"name": "Kyoto", "country": "Japan"},
            {"name": "Paris", "country": "France"},
            {"name": "Bali", "country": "Indonesia"}
        ]

        for place in sample_results:
            st.write(f"### {place['name']} ({place['country']})")
            st.write("AI‑generated description will appear here.")

            col1, col2 = st.columns(2)
            with col1:
                st.button(f"👍 Like {place['name']}")
            with col2:
                st.button(f"👎 Dislike {place['name']}")

# -------------------------------------------------
# ITINERARY PAGE
# -------------------------------------------------
def itinerary_page():
    st.title("Itinerary Generator")
    st.write("Your personalized day‑wise itinerary will appear here.")

# -------------------------------------------------
# RECOMMENDATIONS PAGE
# -------------------------------------------------
def recommendations_page():
    st.title("Smart Recommendations")
    st.write("AI‑based similar destination suggestions will appear here.")

# -------------------------------------------------
# PDF PAGE
# -------------------------------------------------
def pdf_page():
    st.title("PDF Generator")
    st.write("Download your travel itinerary as a PDF.")

# -------------------------------------------------
# VIDEO PAGE
# -------------------------------------------------
def video_page():
    st.title("Travel Recap Video")
    st.write("AI‑generated travel video will appear here.")

# -------------------------------------------------
# CHATBOT PAGE
# -------------------------------------------------
def chatbot_page():
    st.title("Multilingual Chatbot")
    st.write("Chat with the AI travel assistant here.")

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
