import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Cultural Tourism Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

dummy_destinations = [
    {
        "name": "Kyoto",
        "country": "Japan",
        "description": "Experience the timeless beauty of ancient temples, traditional gardens, and geisha culture. Kyoto seamlessly blends centuries of history with modern charm."
    },
    {
        "name": "Paris",
        "country": "France",
        "description": "The City of Light offers iconic landmarks, world-class museums, and exquisite cuisine. Wander along the Seine, visit the Eiffel Tower, and immerse yourself in Parisian elegance."
    },
    {
        "name": "Bali",
        "country": "Indonesia",
        "description": "Discover tropical paradise with stunning beaches, terraced rice paddies, and spiritual temples. Bali offers perfect harmony between adventure and relaxation."
    },
    {
        "name": "Barcelona",
        "country": "Spain",
        "description": "Marvel at Gaudí's architectural masterpieces, enjoy vibrant beaches, and experience the rich cultural heritage. Barcelona pulses with energy and creativity."
    },
    {
        "name": "Bangkok",
        "country": "Thailand",
        "description": "Navigate bustling markets, visit ornate temples, and savor street food delights. Bangkok is a sensory explosion of colors, sounds, and flavors."
    }
]

def home_page():
    st.title("🌍 AI Cultural Tourism Platform")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to Your AI Travel Companion
        
        Discover the world in a personalized way. Our AI-powered platform helps you:
        
        - **Find Perfect Destinations** - Get AI-recommended destinations tailored to your preferences
        - **Generate Itineraries** - Receive day-wise travel plans crafted just for you
        - **Get Smart Recommendations** - Discover hidden gems similar to your interests
        - **Create PDF Guides** - Download your complete travel itinerary as a PDF
        - **Generate Travel Videos** - Get AI-created recap videos of your journey
        - **Chat Multilingually** - Ask our AI chatbot in your preferred language
        
        **Ready to explore?** Use the sidebar to navigate through different features.
        """)
    
    with col2:
        st.info("""
        ### 🚀 Quick Start
        
        1. Go to **Personalization** to tell us about yourself
        2. Get **Recommendations** based on your profile
        3. Generate your personalized **Itinerary**
        4. Download as **PDF** or get a video recap
        5. Chat with our **Chatbot** for more help
        """)

def personalization_page():
    st.title("📝 Personalization")
    st.markdown("Tell us about yourself so we can recommend the perfect destinations!")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        age = st.slider("Your Age", min_value=18, max_value=80, value=30)
        
        interests = st.multiselect(
            "Your Interests (select all that apply)",
            ["Culture", "Adventure", "Nature", "Food", "History", "Beaches"],
            default=["Culture", "Nature"]
        )
        
        trip_duration = st.selectbox(
            "Trip Duration",
            ["3 days", "5 days", "7 days", "10 days"],
            index=1
        )
        
        preferred_month = st.selectbox(
            "Preferred Travel Month",
            ["January", "February", "March", "April", "May", "June", 
             "July", "August", "September", "October", "November", "December"],
            index=0
        )
        
        budget = st.slider(
            "Your Budget (USD per person)",
            min_value=500,
            max_value=10000,
            value=3000,
            step=100
        )
    
    with col2:
        weather_pref = st.selectbox(
            "Weather Preference",
            ["Cold", "Moderate", "Hot"],
            index=1
        )
        
        accessibility = st.checkbox("Do you have accessibility needs?", value=False)
        
        language = st.selectbox(
            "Preferred Language",
            ["English", "Hindi", "French", "Japanese"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### Budget Summary")
        st.info(f"💰 Your trip budget: **${budget:,}** for {trip_duration}")
        estimated_cost_per_day = budget / int(trip_duration.split()[0])
        st.markdown(f"📊 Estimated daily budget: **${estimated_cost_per_day:,.0f}** per day")
    
    st.markdown("---")
    
    if st.button("🎯 Generate Suggestions", use_container_width=True, type="primary"):
        st.session_state.personalization_complete = True
        st.success("✅ Profile created successfully!")
        st.info("Personalized destinations will appear below based on your preferences...")
        
        st.markdown("## 🌟 Recommended Destinations")
        
        for dest in dummy_destinations:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"### {dest['name']}, {dest['country']}")
                    st.markdown(dest['description'])
                
                with col2:
                    if st.button("👍 Like", key=f"like_{dest['name']}"):
                        st.success(f"You liked {dest['name']}!")
                
                with col3:
                    if st.button("👎 Dislike", key=f"dislike_{dest['name']}"):
                        st.warning(f"You disliked {dest['name']}")

def recommendations_page():
    st.title("⭐ Smart Recommendations")
    st.markdown("---")
    
    st.info("""
    Based on your preferences, here are destinations similar to those you've liked.
    These recommendations are powered by our AI recommendation engine that analyzes:
    - Your interests and preferences
    - Weather and seasonal factors
    - Accessibility requirements
    - Travel duration constraints
    
    **Similar destinations will appear here once you complete personalization.**
    """)
    
    st.markdown("### Why These Destinations?")
    st.markdown("""
    - **Curated by AI** - Machine learning algorithms analyze millions of travel data points
    - **Personalized** - Every recommendation is tailored to your unique profile
    - **Quality Assured** - Destinations are vetted for safety, accessibility, and authenticity
    """)

def itinerary_page():
    st.title("📅 Itinerary Generator")
    st.markdown("---")
    
    st.info("""
    Your personalized day-wise itinerary will appear here once you've selected a destination.
    
    The AI will generate a detailed itinerary including:
    - Morning, afternoon, and evening activities
    - Restaurant recommendations
    - Transportation details
    - Local tips and cultural insights
    - Accessibility accommodations
    """)
    
    st.markdown("### Sample Itinerary Format")
    
    with st.expander("View Sample Format"):
        st.markdown("""
        **Day 1 - Arrival**
        - Arrive at airport
        - Check into hotel
        - Evening walk through city center
        - Dinner at local restaurant
        
        **Day 2 - Cultural Exploration**
        - Morning: Visit museum (wheelchair accessible)
        - Lunch: Traditional cuisine at nearby cafe
        - Afternoon: Walking tour of historic district
        - Evening: Cultural performance
        
        **Day 3 - Departure**
        - Breakfast at hotel
        - Last-minute shopping
        - Departure
        """)

def pdf_generator_page():
    st.title("📄 PDF Generator")
    st.markdown("---")
    
    st.info("""
    Download your complete travel itinerary as a professional PDF document.
    
    The PDF will include:
    - Your personalized itinerary
    - Destination information
    - Restaurant recommendations
    - Transportation guide
    - Emergency contacts
    - Weather forecast
    - Packing checklist
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Generate PDF")
        if st.button("📥 Download Itinerary PDF", use_container_width=True):
            st.success("✅ PDF generated successfully!")
            st.markdown("**Your itinerary is ready to download.**")
    
    with col2:
        st.markdown("### Features")
        st.markdown("""
        - High-quality formatting
        - Easy to share
        - Print-friendly
        - Includes maps
        - Offline accessible
        """)

def video_generator_page():
    st.title("🎬 Travel Recap Video")
    st.markdown("---")
    
    st.info("""
    Get an AI-generated travel recap video summarizing your journey.
    
    The video will include:
    - Destination highlights
    - Your itinerary summary
    - Local cultural insights
    - Travel tips and recommendations
    - Motivational travel music
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Create Your Video")
        if st.button("🎥 Generate Recap Video", use_container_width=True):
            st.success("✅ Video generation started!")
            st.markdown("**Your travel recap video is being created. Check back soon!**")
            st.progress(0.7)
    
    with col2:
        st.markdown("### Video Details")
        st.markdown("""
        - Duration: 5-10 minutes
        - Format: HD Quality
        - Music: Licensed tracks
        - Language: Your preferred language
        - Sharable format
        """)

def chatbot_page():
    st.title("💬 Multilingual Chatbot")
    st.markdown("---")
    
    st.info("""
    Chat with our AI travel assistant powered by advanced language models.
    
    Ask about:
    - Destination recommendations
    - Travel tips and advice
    - Cultural information
    - Logistics and planning
    - Emergency assistance
    """)
    
    language = st.selectbox(
        "Select Chat Language",
        ["English", "Hindi", "French", "Japanese", "Spanish", "German"],
        index=0
    )
    
    st.markdown("### Chat Interface")
    
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        st.markdown("**Bot:** Hello! I'm your AI travel assistant. How can I help you plan your perfect cultural tour?")
        st.markdown("")
        st.markdown("**You:** What destinations do you recommend for culture lovers?")
        st.markdown("")
        st.markdown("**Bot:** Based on cultural interests, I recommend exploring Kyoto, Rome, or Istanbul. Each offers rich historical and cultural experiences...")
    
    user_input = st.text_input("Type your message...", placeholder="Ask me anything about travel!")
    
    if st.button("Send", use_container_width=True):
        if user_input:
            st.success(f"✅ Your message was received: '{user_input}'")
            st.info("**Bot Response:** Thank you for your question! In the full version, I'll provide detailed responses in your preferred language.")

pages = {
    "🏠 Home": home_page,
    "📝 Personalization": personalization_page,
    "⭐ Recommendations": recommendations_page,
    "📅 Itinerary": itinerary_page,
    "📄 PDF Generator": pdf_generator_page,
    "🎬 Video Generator": video_generator_page,
    "💬 Chatbot": chatbot_page,
}

st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to:", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
**AI Cultural Tourism Platform**

*Phase 1 - UI & Structure*

This platform demonstrates the complete user interface and flow for an AI-powered cultural tourism recommendation system.
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

pages[selected_page]()
