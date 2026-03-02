"""
Gemini API utilities for generating travel advice, translations, and itineraries
"""

import streamlit as st
import google.generativeai as genai
from config import (
    GEMINI_MODEL,
    GEMINI_WEATHER_TEMP,
    GEMINI_WEATHER_TOKENS,
    GEMINI_TRANSLATE_TEMP,
    GEMINI_TRANSLATE_TOKENS,
    GEMINI_ITINERARY_TEMP,
    GEMINI_ITINERARY_TOKENS,
)

# Global state
GEMINI_AVAILABLE = False
GEMINI_ERROR_MESSAGE = ""


# =========================
# GEMINI INITIALIZATION
# =========================
def initialize_gemini():
    """Initialize Gemini with proper error handling"""
    global GEMINI_AVAILABLE, GEMINI_ERROR_MESSAGE

    try:
        if "GEMINI_API_KEY" not in st.secrets:
            GEMINI_ERROR_MESSAGE = "GEMINI_API_KEY not found in secrets"
            return False

        api_key = st.secrets["GEMINI_API_KEY"]

        if not api_key or len(api_key) < 10:
            GEMINI_ERROR_MESSAGE = "Invalid API key format"
            return False

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content("Say 'OK' if you can read this.")

        if response and response.text:
            GEMINI_AVAILABLE = True
            return True
        else:
            GEMINI_ERROR_MESSAGE = "Gemini responded but with empty text"
            return False

    except Exception as e:
        GEMINI_ERROR_MESSAGE = f"Gemini initialization error: {str(e)}"
        return False


# =========================
# WEATHER ADVICE
# =========================
def gemini_weather_advice(city, climate, season, interest):
    """Generate weather-based travel advice using Gemini"""
    fallback = f"{city} offers a {climate.lower()} climate during {season}, suitable for {interest.lower()} activities and cultural exploration."

    if not GEMINI_AVAILABLE:
        return fallback

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        prompt = f"""You are a helpful travel assistant. 

City: {city}
Climate: {climate}
Season: {season}
Traveler Interest: {interest}

Provide 2-3 sentences with:
1. What the weather is typically like
2. 2-3 specific activities or attractions suitable for this weather
3. One practical travel tip

Keep it concise, friendly, and actionable."""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_WEATHER_TEMP,
                max_output_tokens=GEMINI_WEATHER_TOKENS,
            )
        )

        if response and response.text:
            return response.text.strip()
        else:
            return fallback

    except Exception as e:
        st.warning(f"AI advice generation failed: {str(e)}")
        return fallback


# =========================
# TRANSLATION
# =========================
def gemini_translate(text, language):
    """Translate text using Gemini"""
    if language == "English" or not GEMINI_AVAILABLE:
        return text

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        prompt = f"""Translate the following text to {language}. 
Only provide the translation, nothing else.

Text to translate:
{text}"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TRANSLATE_TEMP,
                max_output_tokens=GEMINI_TRANSLATE_TOKENS,
            )
        )

        if response and response.text:
            return response.text.strip()
        else:
            return text

    except Exception as e:
        st.warning(f"Translation failed: {str(e)}")
        return text


# =========================
# ITINERARY GENERATION
# =========================
def generate_itinerary(city, country, duration, user_input, city_row):
    """
    Generate detailed itinerary using Gemini
    Uses multi-call approach to avoid truncation
    """
    if not GEMINI_AVAILABLE:
        return "Itinerary generation requires Gemini API"

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        # First call: Generate introduction and context
        intro_prompt = f"""You are a travel itinerary expert. Write a 3-4 sentence introduction for a {duration}-day trip to {city}, {country}.

Explain how this destination matches the traveler's profile:
- Interest: {user_input['interest']}
- Budget Level: {user_input['budget']}
- Season: {user_input['season']}
- Weather Preference: {user_input['weather']}
- Age: {user_input['age']}

Make it engaging and personalized. Only write the introduction, nothing else."""

        intro_response = model.generate_content(
            intro_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_ITINERARY_TEMP,
                max_output_tokens=300,
            )
        )

        introduction = intro_response.text.strip() if intro_response and intro_response.text else ""
        print(f"[v0] DEBUG: Introduction length: {len(introduction)} chars")

        # Second call: Generate each day separately to avoid truncation
        full_itinerary = introduction + "\n\n"

        for day_num in range(1, duration + 1):
            day_prompt = f"""Generate a complete and full itinerary for Day {day_num} of a {duration}-day trip to {city}, {country}.

Traveler Profile:
- Interest: {user_input['interest']}
- Budget: {user_input['budget']}
- Season: {user_input['season']}

You MUST write the COMPLETE itinerary for this day with ALL sections filled out. Do not truncate or cut off any content.

Format exactly as:
**Day {day_num} - [Unique, compelling title about the main activity]**

Morning: [Start time] - Write 80-120 words describing the specific morning activity, exact location names, what to see/do, and why it's perfect for this traveler.

Lunch: [Time] - Specify exact restaurant name, cuisine type, signature dishes to order, estimated cost, and why it matches the traveler's budget/interests.

Afternoon: [Time] - Write 80-120 words with specific activity, exact location, duration, what to expect, photos/sights.

Evening: [Time] - Describe dinner experience, restaurant name, cuisine, ambiance, and evening activity (show, walk, etc).

Tips: Write practical advice including: best transportation method, estimated daily budget, what to bring, booking recommendations, avoid/crowds, local customs.

IMPORTANT: You must complete this entire itinerary. Do not stop mid-sentence or leave any section incomplete. Every word must be included."""

            day_response = model.generate_content(
                day_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=GEMINI_ITINERARY_TEMP,
                    max_output_tokens=min(2000, GEMINI_ITINERARY_TOKENS),
                )
            )

            if day_response and day_response.text:
                day_content = day_response.text.strip()
                full_itinerary += day_content + "\n\n"
                print(f"[v0] DEBUG: Day {day_num} length: {len(day_content)} chars")
            else:
                print(f"[v0] DEBUG: Failed to generate Day {day_num}")

        print(f"[v0] DEBUG: FINAL itinerary total length: {len(full_itinerary)} characters")

        if len(full_itinerary) > 500:
            return full_itinerary
        else:
            return "Failed to generate complete itinerary. Please try again."

    except Exception as e:
        print(f"[v0] DEBUG: Itinerary generation error: {str(e)}")
        st.error(f"Itinerary generation failed: {str(e)}")
        return "Error generating itinerary"


# =========================
# HELPER FUNCTIONS
# =========================
def is_gemini_available():
    """Check if Gemini is available"""
    return GEMINI_AVAILABLE


def get_gemini_error():
    """Get Gemini initialization error message"""
    return GEMINI_ERROR_MESSAGE
