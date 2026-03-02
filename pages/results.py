"""
Results display component for showing ranked destinations
"""

import streamlit as st
from modules.data_utils import get_city_image
from modules.gemini_utils import gemini_weather_advice


def render_results_header(total_results):
    """Render header for results section"""
    st.header("🎯 Top Recommendations")
    st.subheader(f"Found {total_results} matching destinations")
    st.divider()


def render_destination_card(index, row, user_input):
    """Render individual destination card"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            image_url = get_city_image(row["city"])
            st.image(image_url, use_container_width=True)

        with col2:
            st.subheader(f"{row['city']}, {row['country']}")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Rating", f"{row['avg_rating']}/5")
            with col_b:
                st.metric("Match Score", f"{row['final_score']:.2%}")
            with col_c:
                st.metric("Duration", f"{row['ideal_duration_days']} days")

            st.caption(f"📍 {row['continent']} | 💰 {row['budget_level']}")

            # Description
            st.write(row["description"])

            # Weather advice
            weather_advice = gemini_weather_advice(
                row["city"],
                row["climate"],
                user_input["season"],
                user_input["interest"]
            )
            st.info(f"✈️ **Travel Tip:** {weather_advice}")

            # Scores breakdown
            st.caption("📊 Interest Match:")
            col_scores = st.columns(4)
            with col_scores[0]:
                st.metric("Culture", f"{row.get('culture_score', 0):.1f}")
            with col_scores[1]:
                st.metric("Adventure", f"{row.get('adventure_score', 0):.1f}")
            with col_scores[2]:
                st.metric("Nature", f"{row.get('nature_score', 0):.1f}")
            with col_scores[3]:
                st.metric("Beach", f"{row.get('beach_score', 0):.1f}")

            return True


def render_results_tabs(ranked_results, user_input, on_select_callback):
    """Render results with tabs for different views"""
    # Limit to top 5 recommendations
    top_results = ranked_results.head(5)
    
    tab1, tab2 = st.tabs(["Card View", "Comparison Table"])

    with tab1:
        for idx, (_, row) in enumerate(top_results.iterrows(), 1):
            col_left, col_right = st.columns([5, 1])

            with col_left:
                render_destination_card(idx, row, user_input)

            with col_right:
                if st.button("📋 Create Itinerary", key=f"btn_{idx}"):
                    on_select_callback(row, user_input)

    with tab2:
        # Table view
        display_df = top_results[[
            "city",
            "country",
            "avg_rating",
            "final_score",
            "ideal_duration_days",
            "budget_level"
        ]].copy()

        display_df.columns = [
            "City",
            "Country",
            "Rating",
            "Match Score",
            "Duration",
            "Budget"
        ]

        st.dataframe(display_df, use_container_width=True)


def render_no_results():
    """Render message when no results found"""
    st.warning("❌ No destinations found matching your criteria. Try adjusting your preferences!")
