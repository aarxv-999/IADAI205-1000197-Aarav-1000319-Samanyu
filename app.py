"""
AI Cultural Tourism Engine - Main Application
Refactored for modularity and maintainability
"""

import streamlit as st
from config import (
    setup_page_config,
    initialize_session_state,
)
from modules import (
    load_data,
    filter_cities,
    rank_cities,
    initialize_firebase,
    save_to_firebase,
    get_session_recommendations,
    initialize_gemini,
    is_gemini_available,
    get_gemini_error,
    save_feedback,
)
from pages.sidebar import render_sidebar, render_error_message, render_success_message
from pages.results import (
    render_results_header,
    render_destination_card,
    render_results_tabs,
    render_no_results,
)
from pages.itinerary import (
    render_itinerary_form,
    render_itinerary_generation,
    render_itinerary_actions,
    render_itinerary_translator,
    render_feedback_form,
    render_itinerary_content,
)


# =========================
# INITIALIZATION
# =========================
def initialize_app():
    """Initialize the application"""
    setup_page_config()
    initialize_session_state()

    # Initialize Firebase
    global db
    db = initialize_firebase()

    # Initialize Gemini
    initialize_gemini()

    if not is_gemini_available():
        st.warning(f"⚠️ Gemini API Issue: {get_gemini_error()}")

    return load_data()


# =========================
# CALLBACKS
# =========================
def on_destination_selected(city_row, user_input):
    """Callback when user selects a destination"""
    st.session_state.current_city = city_row
    st.session_state.current_user_input = user_input
    st.session_state.show_itinerary_form = True
    st.rerun()


# =========================
# MAIN APP FLOW
# =========================
def main():
    """Main application flow"""

    # Initialize
    master, patterns = initialize_app()

    if master is None or patterns is None:
        st.error("Failed to load data. Please check your datasets.")
        return

    # Sidebar input
    user_input = render_sidebar()

    # Main content
    st.title("🌍 AI Cultural Tourism Engine")
    st.write("Discover destinations tailored to your unique travel preferences using AI-powered recommendations.")

    # Process when submit button clicked
    if user_input["submit"]:
        with st.spinner("🔍 Analyzing destinations..."):
            # Filter and rank
            filtered = filter_cities(master, user_input)

            if len(filtered) == 0:
                render_no_results()
                return

            ranked = rank_cities(filtered, user_input, patterns)
            st.session_state.ranked_results = ranked
            st.session_state.user_input = user_input

            # Save to Firebase
            if db is not None:
                doc_id = save_to_firebase(user_input, ranked, st.session_state.session_id, db)
                if doc_id:
                    st.session_state.firebase_doc_id = doc_id

    # Display results if available
    if st.session_state.ranked_results is not None:
        render_results_header(len(st.session_state.ranked_results))
        render_results_tabs(
            st.session_state.ranked_results,
            st.session_state.user_input,
            on_destination_selected
        )

    # Itinerary generation
    if st.session_state.show_itinerary_form and st.session_state.current_city is not None:
        st.divider()

        # Generate itinerary
        if st.session_state.current_itinerary is None:
            itinerary_options = render_itinerary_form(st.session_state.current_city)

            if st.button("Generate Itinerary", type="primary"):
                itinerary = render_itinerary_generation(
                    st.session_state.current_city["city"],
                    st.session_state.current_city["country"],
                    itinerary_options["duration"],
                    st.session_state.current_user_input,
                    st.session_state.current_city,
                )

                if itinerary:
                    # Translate if needed
                    if itinerary_options["translate_to"] != "English":
                        with st.spinner(f"Translating to {itinerary_options['translate_to']}..."):
                            from modules.gemini_utils import gemini_translate
                            itinerary = gemini_translate(itinerary, itinerary_options["translate_to"])

                    st.session_state.current_itinerary = itinerary
                    st.rerun()

        else:
            # Display generated itinerary
            st.header("📋 Your Personalized Itinerary")
            render_itinerary_content(st.session_state.current_itinerary)

            # Action buttons
            render_itinerary_actions(
                st.session_state.current_city["city"],
                st.session_state.current_city["country"],
                st.session_state.current_city.get("climate", "Pleasant"),
                st.session_state.current_user_input["season"],
                st.session_state.current_itinerary,
                st.session_state.current_city,
                st.session_state.current_user_input,
            )

            # Translator
            render_itinerary_translator(st.session_state.current_itinerary)

            # Feedback form
            feedback_result = render_feedback_form(st.session_state.current_city["city"])

            if feedback_result["submitted"] and feedback_result["feedback"]:
                save_feedback(
                    st.session_state.current_city["city"],
                    feedback_result["feedback"],
                    st.session_state.session_id,
                    db
                )
                render_success_message(
                    "✅ Thank you for your feedback! It helps us improve recommendations."
                )


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
