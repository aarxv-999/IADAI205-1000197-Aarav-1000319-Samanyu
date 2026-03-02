"""
Itinerary generation and display component
"""

import streamlit as st
from modules.gemini_utils import generate_itinerary, gemini_translate
from modules.pdf_utils import generate_itinerary_pdf, create_pdf_filename


def render_itinerary_form(selected_city_row):
    """Render form for itinerary customization"""
    st.header(f"📅 Create Itinerary for {selected_city_row['city']}")

    col1, col2 = st.columns(2)

    with col1:
        duration = st.number_input(
            "Duration (days)",
            min_value=1,
            max_value=30,
            value=int(selected_city_row["ideal_duration_days"]),
            step=1
        )

        translate_to = st.selectbox(
            "Translate itinerary to:",
            ["English", "Spanish", "French", "German", "Japanese", "Mandarin"]
        )

    with col2:
        interests = st.multiselect(
            "Focus areas:",
            ["Culture", "Adventure", "Nature", "Beach", "Food"],
            default=[st.session_state.current_user_input["interest"]]
        )

    st.divider()

    return {
        "duration": duration,
        "translate_to": translate_to,
        "interests": interests
    }


def render_itinerary_content(itinerary_text):
    """Render generated itinerary content"""
    st.markdown(itinerary_text)


def render_itinerary_generation(city, country, duration, user_input, city_row):
    """Handle itinerary generation with progress tracking"""
    with st.spinner(f"✨ Generating {duration}-day itinerary for {city}..."):
        itinerary = generate_itinerary(city, country, duration, user_input, city_row)

    if itinerary and len(itinerary) > 100:
        return itinerary
    else:
        st.error("Failed to generate itinerary. Please try again.")
        return None


def render_itinerary_actions(city, country, weather, season, itinerary_text, city_row, user_input):
    """Render action buttons for itinerary (download, translate, etc.)"""
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Download as PDF"):
            try:
                pdf_buffer = generate_itinerary_pdf(
                    city, country, weather, season, itinerary_text, city_row, user_input
                )
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_buffer,
                    file_name=create_pdf_filename(city, country),
                    mime="application/pdf"
                )
                st.success("✅ PDF generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

    with col2:
        if st.button("🔄 Regenerate"):
            st.session_state.current_itinerary = None
            st.rerun()

    with col3:
        if st.button("👎 Not Satisfied"):
            st.session_state.current_itinerary = None
            st.info("Try another destination from the recommendations!")


def render_itinerary_translator(itinerary_text):
    """Render translation interface"""
    with st.expander("🌐 Translate Itinerary"):
        language = st.selectbox(
            "Select language:",
            ["Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Mandarin"],
            key="translate_language"
        )

        if st.button("Translate"):
            with st.spinner(f"Translating to {language}..."):
                translated = gemini_translate(itinerary_text, language)
                st.write(translated)


def render_feedback_form(city):
    """Render feedback form for the itinerary"""
    with st.form("feedback_form", clear_on_submit=True):
        st.subheader("💬 Share Your Feedback")

        rating = st.slider("How helpful was this itinerary?", 1, 5, 4)
        feedback = st.text_area(
            "Additional comments (optional):",
            max_chars=500,
            placeholder="Tell us what you think..."
        )

        submitted = st.form_submit_button("Submit Feedback")

        return {
            "submitted": submitted,
            "rating": rating,
            "feedback": feedback
        }
