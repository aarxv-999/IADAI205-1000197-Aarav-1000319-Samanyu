"""
Sidebar UI component for user input preferences
"""

import streamlit as st


def render_sidebar():
    """Render sidebar for user input"""
    with st.sidebar:
        st.title("🌍 Your Preferences")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=25,
                step=1
            )

            season = st.selectbox(
                "Travel Season",
                ["Spring", "Summer", "Fall", "Winter"]
            )

        with col2:
            interest = st.selectbox(
                "Primary Interest",
                ["Culture", "Adventure", "Nature", "Beach"]
            )

            budget = st.selectbox(
                "Budget Level",
                ["Budget", "Mid-Range", "Luxury"]
            )

        duration = st.slider(
            "Trip Duration (days)",
            min_value=1,
            max_value=30,
            value=7,
            step=1
        )

        weather = st.selectbox(
            "Weather Preference",
            ["Cold", "Pleasant", "Warm"]
        )

        # Submit button
        submit = st.button("🚀 Find Destinations", use_container_width=True)

        return {
            "age": age,
            "interest": interest,
            "duration": duration,
            "weather": weather,
            "season": season,
            "budget": budget,
            "submit": submit
        }


def render_error_message(error_msg):
    """Display error message in sidebar"""
    with st.sidebar:
        st.error(error_msg)


def render_info_message(msg):
    """Display info message in sidebar"""
    with st.sidebar:
        st.info(msg)


def render_success_message(msg):
    """Display success message in sidebar"""
    with st.sidebar:
        st.success(msg)
