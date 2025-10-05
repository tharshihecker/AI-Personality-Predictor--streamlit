import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pymongo
from pymongo import MongoClient
import bcrypt
from datetime import datetime, timedelta
import json
import plotly.express as px
import plotly.graph_objects as go
from bson.objectid import ObjectId
import os

# Page configuration
st.set_page_config(
    page_title="Personality Test App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS Design with Better Visibility
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* App container */
    .stApp {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        font-family: 'Inter', sans-serif;
        color: #1f2937;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Titles & headings */
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin: 1rem;
        padding: 1.5rem;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }
    
    /* Form containers */
    .stForm {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        padding: 2rem !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: 1rem 0 !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3) !important;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3) !important;
    }
    
    /* Slider styling */
    .stSlider {
        padding: 1rem 0 !important;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #e5e7eb, #6366f1) !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Cards & results */
    .personality-card {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .introvert-card {
        border-left: 5px solid #3b82f6 !important;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 197, 253, 0.05)) !important;
    }
    
    .extrovert-card {
        border-left: 5px solid #ef4444 !important;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(252, 165, 165, 0.05)) !important;
    }
    
    .ambivert-card {
        border-left: 5px solid #8b5cf6 !important;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), rgba(196, 181, 253, 0.05)) !important;
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.8) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Alert styling */ 
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Text elements */
    .stMarkdown, .stText {
        color: #374151 !important;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        text-align: center !important;
    }
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# MongoDB Atlas connection
@st.cache_resource
def init_connection():
    """Initialize MongoDB connection"""
    try:
        client = MongoClient("mongodb+srv://streamlit_user:ULnY2laU64LKScPH@fdm.hd64spw.mongodb.net/?retryWrites=true&w=majority&appName=fdm")
        db = client.personality_app
        return db
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Load ML models
@st.cache_resource
def load_models():
    """Load personality prediction models"""
    try:
        import os
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "joblib", "final_gnb_personality_model.joblib")
        le_path = os.path.join(current_dir, "joblib", "personality_label_encoder.joblib")
        
        model = joblib.load(model_path)
        le = joblib.load(le_path)
        return model, le
    except Exception as e:
        st.error(f"Failed to load models: {e}")
        st.error(f"Current working directory: {os.getcwd()}")
        st.error(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        return None, None

# Load features
@st.cache_data
def load_features():
    """Load feature names"""
    try:
        with open("features.json") as f:
            feature_names = json.load(f)["features"]
        return feature_names
    except:
        # Fallback features
        return [
            'party_liking', 'public_speaking_comfort', 'excitement_seeking', 
            'alone_time_preference', 'talkativeness', 'social_energy', 
            'leadership', 'reading_habit', 'adventurousness', 'group_comfort'
        ]

# Feature descriptions
FEATURE_DESCRIPTIONS = {
    'party_liking': 'How much do you enjoy parties and large social gatherings?',
    'public_speaking_comfort': 'How comfortable are you with public speaking?',
    'excitement_seeking': 'How much do you seek exciting and thrilling experiences?',
    'alone_time_preference': 'How much do you prefer spending time alone?',
    'talkativeness': 'How talkative are you in social situations?',
    'social_energy': 'How energized do you feel around other people?',
    'leadership': 'How much do you enjoy taking leadership roles?',
    'reading_habit': 'How much do you enjoy reading books?',
    'adventurousness': 'How adventurous are you in trying new things?',
    'group_comfort': 'How comfortable do you feel in group settings?'
}

# Personality advice system
PERSONALITY_ADVICE = {
    "Introvert": {
        "description": "You tend to be more reserved and prefer smaller social circles. You recharge through solitude and often think before you speak.",
        "strengths": ["Deep thinking", "Good listening skills", "Strong focus", "Meaningful relationships"],
        "advice": [
            "Schedule regular alone time to recharge your energy",
            "Practice speaking up in small groups before larger ones",
            "Use your listening skills to build deeper connections",
            "Find quiet spaces for focused work and creativity"
        ],
        "career_suggestions": ["Writer", "Researcher", "Programmer", "Counselor", "Artist"],
        "color": "#3b82f6",
        "icon": "🔍"
    },
    "Extrovert": {
        "description": "You are energized by social interaction and tend to be outgoing and talkative. You often think out loud and enjoy being around people.",
        "strengths": ["Strong communication", "Natural leadership", "Networking ability", "High energy"],
        "advice": [
            "Channel your energy into leadership opportunities",
            "Use your networking skills to build professional relationships",
            "Practice active listening to balance your communication style",
            "Find roles that involve teamwork and collaboration"
        ],
        "career_suggestions": ["Sales", "Teaching", "Marketing", "Event Planning", "Management"],
        "color": "#f97316",
        "icon": "🌟"
    },
    "Ambivert": {
        "description": "You exhibit both introverted and extroverted tendencies, adapting your behavior based on the situation and your energy levels.",
        "strengths": ["Adaptability", "Balanced perspective", "Situational awareness", "Versatile communication"],
        "advice": [
            "Learn to recognize when you need social time vs. alone time",
            "Use your adaptability as a strength in various situations",
            "Practice balancing your energy between social and solitary activities",
            "Leverage your ability to understand both introverts and extroverts"
        ],
        "career_suggestions": ["Project Manager", "Consultant", "Human Resources", "Therapist", "Entrepreneur"],
        "color": "#8b5cf6",
        "icon": "⚖️"
    }
}

# Authentication functions
def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def create_user(db, name, email, password):
    """Create new user in MongoDB"""
    try:
        # Check if user exists
        if db.users.find_one({"email": email.lower()}):
            return {"success": False, "message": "Email already registered"}
        
        # Create user
        user_data = {
            "name": name,
            "email": email.lower(),
            "password_hash": hash_password(password),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        
        return {"success": True, "user": user_data}
    except Exception as e:
        return {"success": False, "message": str(e)}

def authenticate_user(db, email, password):
    """Authenticate user"""
    try:
        user = db.users.find_one({"email": email.lower()})
        if user and verify_password(password, user["password_hash"]):
            return {"success": True, "user": user}
        return {"success": False, "message": "Invalid email or password"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def save_test_result(db, user_id, features, prediction, confidence, probabilities):
    """Save personality test result to MongoDB"""
    try:
        test_data = {
            "user_id": ObjectId(user_id),
            "features": features,
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "created_at": datetime.utcnow()
        }
        
        result = db.personality_tests.insert_one(test_data)
        test_data["_id"] = result.inserted_id
        
        return {"success": True, "test": test_data}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_user_history(db, user_id):
    """Get user's test history from MongoDB"""
    try:
        tests = list(db.personality_tests.find(
            {"user_id": ObjectId(user_id)}
        ).sort("created_at", -1))
        
        return {"success": True, "tests": tests}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

# Authentication UI
def show_auth_page():
    """Show login/signup page"""
    st.title("🧠 Personality Test App")
    st.markdown("### Discover your personality type")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to your account")
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if email and password:
                    db = init_connection()
                    if db is not None:
                        result = authenticate_user(db, email, password)
                        if result["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user = result["user"]
                            st.session_state.page = 'dashboard'
                            st.rerun()
                        else:
                            st.error(result["message"])
                    else:
                        st.error("Database connection failed")
                else:
                    st.error("Please fill all fields")
    
    with tab2:
        st.subheader("Create new account")
        with st.form("signup_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            signup_btn = st.form_submit_button("Sign Up", use_container_width=True)
            
            if signup_btn:
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        db = init_connection()
                        if db is not None:
                            result = create_user(db, name, email, password)
                            if result["success"]:
                                st.success("Account created successfully! Please login.")
                            else:
                                st.error(result["message"])
                        else:
                            st.error("Database connection failed")
                else:
                    st.error("Please fill all fields")

# Dashboard
def show_dashboard():
    """Show main dashboard"""
    st.title(f"Welcome, {st.session_state.user['name']}! 👋")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Go to:",
        ["Dashboard", "Take Test", "Test History", "Profile"],
        key="nav_select"
    )
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.page = 'login'
        st.rerun()
    
    # Route to selected page
    if page == "Dashboard":
        show_dashboard_content()
    elif page == "Take Test":
        show_personality_test()
    elif page == "Test History":
        show_test_history()
    elif page == "Profile":
        show_profile()

def show_dashboard_content():
    """Show dashboard content"""
    col1, col2, col3 = st.columns(3)
    
    # Get user stats
    db = init_connection()
    if db is not None:
        history_result = get_user_history(db, st.session_state.user["_id"])
        if history_result["success"]:
            tests = history_result["tests"]
            
            with col1:
                st.metric("Total Tests", len(tests))
            
            with col2:
                if tests:
                    avg_confidence = np.mean([test["confidence"] for test in tests])
                    st.metric("Average Confidence", f"{avg_confidence:.1%}")
                else:
                    st.metric("Average Confidence", "N/A")
            
            with col3:
                if tests:
                    most_common = max(set([test["prediction"] for test in tests]), 
                                    key=[test["prediction"] for test in tests].count)
                    st.metric("Most Common Type", most_common)
                else:
                    st.metric("Most Common Type", "N/A")
            
            # Recent tests
            st.subheader("Recent Tests")
            if tests:
                recent_tests = tests[:5]  # Show last 5 tests
                for test in recent_tests:
                    advice = PERSONALITY_ADVICE.get(test["prediction"], {})
                    with st.expander(f"{advice.get('icon', '❓')} {test['prediction']} - {test['created_at'].strftime('%Y-%m-%d %H:%M')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Confidence:** {test['confidence']:.1%}")
                        with col2:
                            if st.button(f"View Details", key=f"view_{test['_id']}"):
                                st.session_state.selected_test = test
                                st.session_state.page = 'test_details'
                                st.rerun()
            else:
                st.info("No tests taken yet. Take your first personality test!")
                if st.button("Take Your First Test"):
                    st.session_state.page = 'test'
                    st.rerun()

def show_personality_test():
    """Show personality test interface"""
    st.title("🧠 Personality Test")
    st.markdown("Rate each aspect of your personality on a scale from 0 to 10")
    
    # Load models and features
    model, le = load_models()
    feature_names = load_features()
    
    if model is None or le is None:
        st.error("Failed to load prediction models")
        return
    
    # Create form for personality test
    with st.form("personality_test"):
        responses = {}
        
        # Create sliders for each feature
        for i, feature in enumerate(feature_names):
            feature_display = feature.replace('_', ' ').title()
            description = FEATURE_DESCRIPTIONS.get(feature, f"Rate your {feature.replace('_', ' ')}")
            
            responses[feature] = st.slider(
                f"**{feature_display}**",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.1,
                help=description,
                key=f"slider_{feature}"
            )
            
            st.caption(description)
            st.markdown("---")
        
        # Submit button
        submit_btn = st.form_submit_button("🎯 Get My Personality Result", use_container_width=True)
        
        if submit_btn:
            # Make prediction
            features = [responses[f] for f in feature_names]
            features_array = np.array(features).reshape(1, -1)
            
            pred_encoded = model.predict(features_array)[0]
            probabilities = model.predict_proba(features_array)[0]
            
            prediction = le.inverse_transform([pred_encoded])[0]
            confidence = float(max(probabilities))
            
            # Get all class probabilities
            all_classes = le.classes_
            prob_dict = {}
            for i, prob in enumerate(probabilities):
                prob_dict[all_classes[i]] = float(prob)
            
            # Save to database
            db = init_connection()
            if db is not None:
                save_result = save_test_result(
                    db, 
                    st.session_state.user["_id"], 
                    responses, 
                    prediction, 
                    confidence, 
                    prob_dict
                )
                
                if save_result["success"]:
                    # Store result in session state
                    st.session_state.latest_result = {
                        "prediction": prediction,
                        "confidence": confidence,
                        "probabilities": prob_dict,
                        "features": responses
                    }
                    
                    # Show results
                    show_test_results(prediction, confidence, prob_dict)
                else:
                    st.error("Failed to save test results")
            else:
                st.error("Database connection failed")

def show_test_results(prediction, confidence, probabilities):
    """Show test results"""
    advice = PERSONALITY_ADVICE.get(prediction, {})
    
    # Main result card
    st.success("Test completed successfully!")
    
    # Result display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Personality result card
        card_class = f"{prediction.lower()}-card"
        st.markdown(f"""
        <div class="personality-card {card_class}">
            <h1 style="text-align: center; font-size: 3rem; margin: 0;">{advice.get('icon', '❓')}</h1>
            <h2 style="text-align: center; color: #333; margin: 10px 0;">{prediction}</h2>
            <h3 style="text-align: center; color: #666;">{confidence:.1%} Confidence</h3>
            <p style="text-align: center; color: #555; margin: 15px 0;">{advice.get('description', '')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Probability chart
        st.subheader("📊 Probabilities")
        prob_df = pd.DataFrame(
            list(probabilities.items()),
            columns=['Personality', 'Probability']
        )
        
        fig = px.pie(
            prob_df, 
            values='Probability', 
            names='Personality',
            color_discrete_map={
                'Extrovert': '#ed8936',
                'Introvert': '#4299e1', 
                'Ambivert': '#9f7aea'
            },
            title="Personality Type Probabilities"
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=14, color='white'),
            marker=dict(line=dict(color='white', width=2))
        )
        fig.update_layout(
            font=dict(size=14, color='#2d3748'),
            title_font=dict(size=18, color='#1a202c'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.01
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Your Strengths")
        for strength in advice.get('strengths', []):
            st.write(f"• {strength}")
        
        st.subheader("🎯 Career Suggestions")
        for career in advice.get('career_suggestions', []):
            st.write(f"• {career}")
    
    with col2:
        st.subheader("💡 Personal Development Advice")
        for tip in advice.get('advice', []):
            st.write(f"• {tip}")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Take Another Test"):
            st.rerun()
    with col2:
        if st.button("📊 View History"):
            st.session_state.page = 'history'
            st.rerun()
    with col3:
        if st.button("🏠 Go to Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()

def show_test_history():
    """Show test history"""
    st.title("📊 Test History")
    
    db = init_connection()
    if db is not None:
        history_result = get_user_history(db, st.session_state.user["_id"])
        
        if history_result["success"]:
            tests = history_result["tests"]
            
            if tests:
                st.write(f"Total tests completed: **{len(tests)}**")
                
                # History table
                for test in tests:
                    advice = PERSONALITY_ADVICE.get(test["prediction"], {})
                    
                    with st.expander(f"{advice.get('icon', '❓')} {test['prediction']} - {test['created_at'].strftime('%Y-%m-%d %H:%M')} - {test['confidence']:.1%} confidence"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Prediction Details:**")
                            st.write(f"• Type: {test['prediction']}")
                            st.write(f"• Confidence: {test['confidence']:.1%}")
                            st.write(f"• Date: {test['created_at'].strftime('%Y-%m-%d %H:%M')}")
                        
                        with col2:
                            st.write("**Probabilities:**")
                            for personality, prob in test['probabilities'].items():
                                st.write(f"• {personality}: {prob:.1%}")
                        
                        if st.button(f"View Full Results", key=f"view_full_{test['_id']}"):
                            show_test_results(test['prediction'], test['confidence'], test['probabilities'])
            else:
                st.info("No tests completed yet.")
                if st.button("Take Your First Test"):
                    st.session_state.page = 'test'
                    st.rerun()
        else:
            st.error("Failed to load test history")
    else:
        st.error("Database connection failed")

def show_profile():
    """Show user profile"""
    st.title("👤 Profile")
    
    user = st.session_state.user
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/150", caption="Profile Picture", width=150)
    
    with col2:
        st.write("**Name:**", user["name"])
        st.write("**Email:**", user["email"])
        st.write("**Member Since:**", user["created_at"].strftime("%Y-%m-%d"))
    
    # User statistics
    st.subheader("📈 Your Statistics")
    
    db = init_connection()
    if db is not None:
        history_result = get_user_history(db, user["_id"])
        
        if history_result["success"]:
            tests = history_result["tests"]
            
            if tests:
                # Statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Tests", len(tests))
                
                with col2:
                    avg_confidence = np.mean([test["confidence"] for test in tests])
                    st.metric("Average Confidence", f"{avg_confidence:.1%}")
                
                with col3:
                    personality_counts = {}
                    for test in tests:
                        personality_counts[test["prediction"]] = personality_counts.get(test["prediction"], 0) + 1
                    most_common = max(personality_counts.items(), key=lambda x: x[1])
                    st.metric("Most Common Type", f"{most_common[0]} ({most_common[1]}x)")
                
                # Personality distribution chart
                st.subheader("🎭 Personality Type Distribution")
                
                if personality_counts:
                    fig = px.bar(
                        x=list(personality_counts.keys()),
                        y=list(personality_counts.values()),
                        color=list(personality_counts.keys()),
                        color_discrete_map={
                            'Extrovert': '#ed8936',
                            'Introvert': '#4299e1',
                            'Ambivert': '#9f7aea'
                        },
                        title="Personality Type Distribution"
                    )
                    fig.update_layout(
                        xaxis_title="Personality Type",
                        yaxis_title="Number of Tests",
                        showlegend=False,
                        font=dict(size=14, color='#2d3748'),
                        title_font=dict(size=18, color='#1a202c'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            gridcolor='rgba(128,128,128,0.2)',
                            linecolor='rgba(128,128,128,0.3)'
                        ),
                        yaxis=dict(
                            gridcolor='rgba(128,128,128,0.2)',
                            linecolor='rgba(128,128,128,0.3)'
                        )
                    )
                    fig.update_traces(
                        marker=dict(line=dict(color='white', width=1))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Confidence over time
                st.subheader("📈 Confidence Over Time")
                
                confidence_data = [(test["created_at"], test["confidence"]) for test in reversed(tests)]
                if confidence_data:
                    dates, confidences = zip(*confidence_data)
                    
                    fig = px.line(
                        x=dates,
                        y=confidences,
                        title="Test Confidence Over Time",
                        color_discrete_sequence=['#4299e1']
                    )
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Confidence",
                        font=dict(size=14, color='#2d3748'),
                        title_font=dict(size=18, color='#1a202c'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            gridcolor='rgba(128,128,128,0.2)',
                            linecolor='rgba(128,128,128,0.3)'
                        ),
                        yaxis=dict(
                            gridcolor='rgba(128,128,128,0.2)',
                            linecolor='rgba(128,128,128,0.3)'
                        )
                    )
                    fig.update_traces(
                        line=dict(width=3),
                        marker=dict(size=8, color='#4299e1')
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No test data available for statistics.")

# Main app logic
def main():
    """Main application logic"""
    init_session_state()
    

    
    # Route based on authentication status
    if not st.session_state.authenticated:
        show_auth_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()