"""
Modules package for Tourism Engine
Imports utilities for easy access
"""

from modules.data_utils import (
    load_data,
    get_age_group,
    get_user_pattern,
    get_dynamic_weights,
    filter_cities,
    rank_cities,
    get_city_image,
    save_feedback,
)

from modules.firebase_utils import (
    initialize_firebase,
    save_to_firebase,
    get_session_recommendations,
)

from modules.gemini_utils import (
    initialize_gemini,
    gemini_weather_advice,
    gemini_translate,
    generate_itinerary,
    is_gemini_available,
    get_gemini_error,
)

__all__ = [
    # Data utilities
    "load_data",
    "get_age_group",
    "get_user_pattern",
    "get_dynamic_weights",
    "filter_cities",
    "rank_cities",
    "get_city_image",
    "save_feedback",
    # Firebase utilities
    "initialize_firebase",
    "save_to_firebase",
    "get_session_recommendations",
    # Gemini utilities
    "initialize_gemini",
    "gemini_weather_advice",
    "gemini_translate",
    "generate_itinerary",
    "is_gemini_available",
    "get_gemini_error",
]
