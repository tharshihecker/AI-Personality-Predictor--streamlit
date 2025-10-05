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
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
        color: #0f172a; /* darker text (not white) */
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    /* Center content and reduce max width for better centering */
    .main .block-container .stMarkdown, .main .block-container .stTitle {
        margin-left: auto !important;
        margin-right: auto !important;
        max-width: 900px !important;
    }
    
    /* Titles & headings */
    :root{
        --primary:#0f172a;
        --accent-1:#0ea5a4; /* teal */
        --accent-2:#7c3aed; /* violet */
        --muted:#64748b;
        --card:#ffffff;
    }

    h1 {
        color: var(--primary) !important;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-align: center;
        background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        color: var(--accent-1) !important; /* colored headings */
        font-weight: 700;
    }

    h3 {
        color: var(--accent-2) !important;
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
    
    /* Input fields (softer, warmer and lower visual intensity) */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: #fcfbf9 !important; /* warm light */
        color: #0f172a !important; /* dark text for visibility */
        border: 1px solid rgba(15,23,42,0.06) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        height: 40px !important;
        line-height: 1.2 !important;
        font-size: 14px !important;
        transition: all 0.12s ease !important;
        box-shadow: none !important;
    }

    /* Placeholder color so placeholders are visible */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder,
    .stTextInput input::-webkit-input-placeholder, .stTextArea textarea::-webkit-input-placeholder,
    .stTextInput input:-ms-input-placeholder, .stTextArea textarea:-ms-input-placeholder {
        color: #475569 !important;
        opacity: 1 !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }
    
    /* Form containers */
    .stForm {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(6px);
        padding: 1rem !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        margin: 0.75rem 0 !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #34d399, #10b981) !important; /* green */
        color: #000000 !important; /* black text */
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.18) !important;
    }

    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.22) !important;
    }

    /* Ensure metrics/cards use subtle colored accents */
    .stMetric {
        color: var(--primary) !important;
    }
    
    /* Success messages - multiple selectors to ensure coverage */
    .stSuccess, .stAlert[kind="success"], [data-testid="stAlert"][kind="success"] {
        background: linear-gradient(135deg, #bbf7d0 0%, #86efac 100%) !important;
        color: #065f46 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 2px solid #22c55e !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
        font-weight: 600 !important;
    }
    
    .stSuccess *, .stAlert[kind="success"] *, [data-testid="stAlert"][kind="success"] * {
        color: #065f46 !important;
    }
    
    /* Error messages - multiple selectors to ensure coverage */
    .stError, .stAlert[kind="error"], [data-testid="stAlert"][kind="error"] {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%) !important;
        color: #7f1d1d !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 2px solid #ef4444 !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
        font-weight: 600 !important;
    }
    
    .stError *, .stAlert[kind="error"] *, [data-testid="stAlert"][kind="error"] * {
        color: #7f1d1d !important;
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
        background: var(--card) !important;
        backdrop-filter: blur(6px) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid rgba(15, 23, 42, 0.04) !important;
    }
    .personality-card h1, .personality-card h2 {
        text-align: center;
    }

    /* Ensure buttons are visible and clickable */
    .stButton button {
        background: linear-gradient(135deg, #34d399, #10b981) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        z-index: 5 !important;
        box-shadow: 0 4px 10px rgba(16,185,129,0.12) !important;
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

    /* Strong overrides for auth forms and inputs to ensure visibility */
    .stForm, .stForm * {
        color: #000000 !important;
        background-color: transparent !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        color: #000000 !important;
        background: #ffffff !important;
        border: 1px solid rgba(15,23,42,0.08) !important;
    }

    .stTextInput input::placeholder, .stTextArea textarea::placeholder,
    .stTextInput input::-webkit-input-placeholder, .stTextArea textarea::-webkit-input-placeholder,
    .stTextInput input:-ms-input-placeholder, .stTextArea textarea:-ms-input-placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    
    /* Fix tab visibility - make all tab text permanently visible */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        border: 2px solid #e5e7eb !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #000000 !important;
        background-color: #f3f4f6 !important;
        border-color: #9ca3af !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #000000 !important;
        background-color: #ffffff !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Personality Test Slider Styling */
    .stSlider {
        padding: 10px 0 !important;
    }
    
    .stSlider > div > div > div > div {
        text-align: center !important;
    }
    
    /* Make slider track thicker and more visible */
    .stSlider > div > div > div > div > div {
        height: 8px !important;
        background: linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #22c55e 100%) !important;
        border-radius: 4px !important;
    }
    
    /* Make slider thumb bigger */
    .stSlider > div > div > div > div > div > div {
        width: 24px !important;
        height: 24px !important;
        background: #3b82f6 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Mobile Navigation Buttons */
    [data-testid="column"] .stButton button[key^="nav_"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s !important;
    }
    
    [data-testid="column"] .stButton button[key^="nav_"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Logout button special styling */
    [data-testid="column"] .stButton button[key="nav_logout"] {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    }
    
    [data-testid="column"] .stButton button[key="nav_logout"]:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
    }
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {
        [data-testid="column"] .stButton button[key^="nav_"] {
            font-size: 12px !important;
            padding: 6px 8px !important;
        }
    }

    /* FORCE ALL BUTTONS TO BE VISIBLE AND CLICKABLE */
    .stButton button, .stButton > button, button[kind="primary"], button[kind="secondary"] {
        pointer-events: auto !important;
        z-index: 99999 !important;
        background-color: #ff4444 !important;
        color: white !important;
        border: 3px solid #cc0000 !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        cursor: pointer !important;
        position: relative !important;
        display: block !important;
        width: 100% !important;
        min-height: 50px !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover, .stButton > button:hover, button[kind="primary"]:hover, button[kind="secondary"]:hover {
        background-color: #ff0000 !important;
        transform: scale(1.05) !important;
        box-shadow: 0 8px 16px rgba(255, 68, 68, 0.5) !important;
    }
    
    .stButton button:active, .stButton > button:active {
        background-color: #990000 !important;
        transform: scale(0.95) !important;
    }

    /* Warm light card backgrounds for sections */
    .warm-card {
        background: linear-gradient(180deg, #fff7ed 0%, #fffbf7 100%) !important;
        border: 1px solid rgba(249, 115, 22, 0.06) !important;
    }

    .muted-card {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border: 1px solid rgba(15, 23, 42, 0.03) !important;
    }

    /* Animated icon helper */
    .icon-spin {
        display:inline-block;
        animation: spin 4s linear infinite;
        transform-origin: center;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Multi-color heading banner */
    .multi-heading {
        display:block;
        text-align:center;
        font-weight:800;
        font-size:2.2rem;
        margin: 6px 0 14px 0;
        background: linear-gradient(90deg,#06b6d4,#7c3aed,#f97316,#ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
        color: #0f172a !important; /* always dark text */
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


def render_heading(text: str, icon: str = ""):
    """Render a stylized multi-color heading with optional animated icon"""
    if icon:
        st.markdown(f"<div class='multi-heading'>{icon} <span style='font-weight:800'>{text}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='multi-heading'>{text}</div>", unsafe_allow_html=True)

# Authentication UI
def show_auth_page():
    """Show login/signup page"""
    render_heading("Personality Test App", "🧠")
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
    # Mobile-friendly navigation bar at top
    st.markdown("### 🧭 Navigation")
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 1, 1, 1])
    
    with nav_col1:
        if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.nav_override = 'Dashboard'
            st.rerun()
    with nav_col2:
        if st.button("🧠 Take Test", key="nav_take_test", use_container_width=True):
            st.session_state.nav_override = 'Take Test'
            st.rerun()
    with nav_col3:
        if st.button("📊 History", key="nav_history", use_container_width=True):
            st.session_state.nav_override = 'Test History'
            st.rerun()
    with nav_col4:
        if st.button("👤 Profile", key="nav_profile", use_container_width=True):
            st.session_state.nav_override = 'Profile'
            st.rerun()
    with nav_col5:
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown("---")
    
    render_heading(f"Welcome, {st.session_state.user['name']}!", "👋")
    
    # Sidebar navigation (still keep for desktop users)
    st.sidebar.title("Navigation")
    # Use nav_override when set by buttons elsewhere (results/history)
    options = ["Dashboard", "Take Test", "Test History", "Profile"]
    default = st.session_state.get('nav_override', None)
    if default and default in options:
        page = st.sidebar.selectbox("Go to:", options, index=options.index(default), key="nav_select")
        # clear override after use - but after page navigation
        if st.session_state.get('nav_override') == page:
            st.session_state.pop('nav_override', None)
    else:
        page = st.sidebar.selectbox("Go to:", options, key="nav_select")
    
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
    
    # Get user stats - force fresh database connection
    db = init_connection()
    if db is not None:
        # Clear any cached results and get fresh data
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
                    # Display created_at with +5:30 offset
                    try:
                        display_time = (test['created_at'] + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M')
                    except Exception:
                        display_time = str(test.get('created_at'))

                    with st.expander(f"{advice.get('icon', '❓')} {test['prediction']} - {display_time} (+05:30)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Confidence:** {test['confidence']:.1%}")
                        with col2:
                            details_key = f"view_{str(test['_id'])}"
                            if st.button(f"👁️ View Details", key=details_key, use_container_width=True):
                                st.balloons()
                                st.success("✅ VIEW DETAILS CLICKED!")
                                
                                # Show details immediately here
                                st.write("---")
                                st.subheader(f"🔍 Details for {test['prediction']}")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Type", test['prediction'])
                                    st.metric("Confidence", f"{test['confidence']:.1%}")
                                    
                                with col2:
                                    st.write("**Probabilities:**")
                                    for personality, prob in test['probabilities'].items():
                                        st.write(f"• {personality}: {prob:.1%}")
                                
                                # Show charts
                                st.write("**📊 Charts:**")
                                chart_col1, chart_col2 = st.columns(2)
                                
                                with chart_col1:
                                    # Pie chart
                                    import plotly.express as px
                                    prob_data = pd.DataFrame(
                                        list(test['probabilities'].items()),
                                        columns=['Personality', 'Probability']
                                    )
                                    fig_pie = px.pie(prob_data, values='Probability', names='Personality',
                                                   title="Distribution")
                                    fig_pie.update_traces(textfont_color='black')
                                    fig_pie.update_layout(font_color='black')
                                    st.plotly_chart(fig_pie, use_container_width=True)
                                
                                with chart_col2:
                                    # Bar chart
                                    fig_bar = px.bar(prob_data, x='Personality', y='Probability',
                                                   title="Scores")
                                    fig_bar.update_traces(textfont_color='black')
                                    fig_bar.update_layout(font_color='black',
                                                        xaxis_title="Type",
                                                        yaxis_title="Probability")
                                    st.plotly_chart(fig_bar, use_container_width=True)
                                
                                st.write("---")
            else:
                st.info("📝 **Instructions:** Please use the sidebar navigation and select **'Take Test'** to complete your first personality assessment!")

def show_personality_test():
    """Show personality test interface"""
    render_heading("Personality Test", "🧠")
    st.markdown("<div style='text-align: center; font-size: 18px; margin-bottom: 30px;'>Rate each aspect of your personality on a scale from 0 to 10</div>", unsafe_allow_html=True)
    
    # Load models and features
    model, le = load_models()
    feature_names = load_features()
    
    if model is None or le is None:
        st.error("Failed to load prediction models")
        return
    
    # If we have a result saved in session state and flagged, show it (outside form)
    if st.session_state.get('show_results') and st.session_state.get('latest_result'):
        res = st.session_state.latest_result
        show_test_results(res['prediction'], res['confidence'], res['probabilities'])
        return

    # Create form for personality test
    with st.form("personality_test"):
        responses = {}
        
        # Create sliders for each feature (centered)
        for i, feature in enumerate(feature_names):
            feature_display = feature.replace('_', ' ').title()
            description = FEATURE_DESCRIPTIONS.get(feature, f"Rate your {feature.replace('_', ' ')}")

            # Center each question and slider with larger text
            with st.container():
                c1, c2, c3 = st.columns([1, 8, 1])
                with c2:
                    # Larger, centered question title
                    st.markdown(f"<div style='text-align: center; font-size: 22px; font-weight: bold; color: #1f2937; margin-bottom: 10px;'>{feature_display}</div>", unsafe_allow_html=True)
                    
                    # Centered description with larger text
                    st.markdown(f"<div style='text-align: center; font-size: 16px; color: #4b5563; margin-bottom: 15px; font-style: italic;'>{description}</div>", unsafe_allow_html=True)
                    
                    responses[feature] = st.slider(
                        label=f"slider_{feature}",
                        min_value=0.0,
                        max_value=10.0,
                        value=5.0,
                        step=0.1,
                        help=description,
                        key=f"slider_{feature}",
                        label_visibility='collapsed'
                    )
                    
                    # Add some spacing
                    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
        
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
                    # Do not call show_test_results() here while inside form.
                    # Instead, set a flag and rerun so results render outside the form context.
                    st.session_state.show_results = True
                    st.rerun()
                else:
                    st.error("Failed to save test results")
            else:
                st.error("Database connection failed")

def show_test_results(prediction, confidence, probabilities):
    """Show test results"""
    advice = PERSONALITY_ADVICE.get(prediction, {})
    
    # Main result card
    st.success("✅ Test completed successfully!")
    
    # Result display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Personality result card
        card_class = f"{prediction.lower()}-card"
        st.markdown(f"""
        <div class="personality-card {card_class}">
            <h1 style="text-align: center; font-size: 3rem; margin: 0;">{advice.get('icon', '❓')}</h1>
            <h2 style="text-align: center; color: #333; margin: 10px 0;">{prediction}</h2>
            <h3 style="text-align: center; color: #1f2937;">{confidence:.1%} Confidence</h3>
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
            textfont=dict(size=14, color='#0f172a'),
            marker=dict(line=dict(color='#0f172a', width=1))
        )
        fig.update_layout(
            font=dict(size=14, color='#0f172a'),
            title_font=dict(size=18, color='#0b1220'),
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
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    # Action buttons with immediate navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Take Another Test", key="take_another_test_btn", use_container_width=True):
            st.balloons()
            st.success("✅ TAKE ANOTHER TEST CLICKED!")
            st.session_state.pop('latest_result', None)
            st.session_state.pop('show_results', None)
            st.session_state.nav_override = 'Take Test'
            st.rerun()
    
    # Hidden buttons - commented out
    # with col2:
    #     if st.button("📊 View History", key="result_view_history", use_container_width=True):
    #         st.balloons()
    #         st.success("✅ VIEW HISTORY CLICKED!")
    #         st.session_state.pop('latest_result', None)
    #         st.session_state.pop('show_results', None)
    #         st.session_state.nav_override = 'Test History'
    #         st.rerun()
    # 
    # with col3:
    #     if st.button("🏠 Go to Dashboard", key="result_go_dashboard", use_container_width=True):
    #         st.balloons()
    #         st.success("✅ GO TO DASHBOARD CLICKED!")
    #         st.session_state.pop('latest_result', None)
    #         st.session_state.pop('show_results', None)
    #         st.session_state.nav_override = 'Dashboard'
    #         st.rerun()

def show_test_history():
    """Show test history"""
    render_heading("Test History", "📊")
    
    db = init_connection()
    if db is not None:
        history_result = get_user_history(db, st.session_state.user["_id"])
        
        if history_result["success"]:
            tests = history_result["tests"]
            
            if tests:
                st.write(f"Total tests completed: **{len(tests)}**")
                if st.button("Remove All History"):
                    st.session_state.confirm_delete_history = True

                if st.session_state.get('confirm_delete_history'):
                    st.warning("This action will permanently delete all your test history. This cannot be undone.")
                    c1, c2 = st.columns([1,1])
                    with c1:
                        if st.button("Yes, delete all history", key="delete_history_yes"):
                            db = init_connection()
                            if db is not None:
                                try:
                                    db.personality_tests.delete_many({"user_id": ObjectId(st.session_state.user['_id'])})
                                    st.success("All history removed")
                                    # Clear session and reload
                                    st.session_state.pop('confirm_delete_history', None)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to delete history: {e}")
                            else:
                                st.error("Database connection failed")
                    with c2:
                        if st.button("Cancel", key="delete_history_cancel"):
                            st.session_state.pop('confirm_delete_history', None)
                            st.info("Deletion cancelled")
                
                # History table
                for test in tests:
                    advice = PERSONALITY_ADVICE.get(test["prediction"], {})
                    # Format created_at with +5:30 offset
                    try:
                        display_time = (test['created_at'] + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M')
                    except Exception:
                        display_time = str(test.get('created_at'))

                    with st.expander(f"{advice.get('icon', '❓')} {test['prediction']} - {display_time} — {test['confidence']:.1%} confidence"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Prediction Details:**")
                            st.write(f"• Type: {test['prediction']}")
                            st.write(f"• Confidence: {test['confidence']:.1%}")
                            try:
                                date_display = (test['created_at'] + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M')
                            except Exception:
                                date_display = str(test.get('created_at'))
                            st.write(f"• Date: {date_display} (+05:30)")
                        
                        with col2:
                            st.write("**Probabilities:**")
                            for personality, prob in test['probabilities'].items():
                                st.write(f"• {personality}: {prob:.1%}")
                        
                        view_full_key = f"view_full_{str(test['_id'])}"
                        if st.button(f"📋 View Full Results", key=view_full_key, use_container_width=True):
                            st.balloons()
                            st.success("✅ VIEW FULL RESULTS CLICKED!")
                            
                            # Immediately show the result here in this page
                            st.write("---")
                            st.subheader(f"🎯 Full Results for {test['prediction']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Personality Type", test['prediction'])
                                st.metric("Confidence", f"{test['confidence']:.1%}")
                            
                            with col2:
                                st.write("**All Probabilities:**")
                                for personality, prob in test['probabilities'].items():
                                    st.write(f"• **{personality}**: {prob:.1%}")
                            
                            # Show charts
                            st.write("**📊 Visual Analysis:**")
                            chart_col1, chart_col2 = st.columns(2)
                            
                            with chart_col1:
                                # Pie chart
                                import plotly.express as px
                                prob_data = pd.DataFrame(
                                    list(test['probabilities'].items()),
                                    columns=['Personality', 'Probability']
                                )
                                fig_pie = px.pie(prob_data, values='Probability', names='Personality',
                                               title="Personality Distribution")
                                fig_pie.update_traces(textfont_color='black')
                                fig_pie.update_layout(font_color='black')
                                st.plotly_chart(fig_pie, use_container_width=True)
                            
                            with chart_col2:
                                # Bar chart
                                fig_bar = px.bar(prob_data, x='Personality', y='Probability',
                                               title="Probability Scores")
                                fig_bar.update_traces(textfont_color='black')
                                fig_bar.update_layout(font_color='black', 
                                                    xaxis_title="Personality Type",
                                                    yaxis_title="Probability")
                                st.plotly_chart(fig_bar, use_container_width=True)
                            
                            # Show advice if available
                            advice = PERSONALITY_ADVICE.get(test['prediction'], {})
                            if advice:
                                st.write("**💡 Advice:**")
                                for tip in advice.get('advice', []):
                                    st.write(f"• {tip}")
                            
                            st.write("---")
            else:
                st.info("📝 **Instructions:** Please use the sidebar navigation and select **'Take Test'** to complete your first personality assessment!")
        else:
            st.error("Failed to load test history")
    else:
        st.error("Database connection failed")

def show_profile():
    """Show user profile"""
    render_heading("Profile", "👤")
    
    user = st.session_state.user
    
    # User info (no profile picture)
    st.write("**Name:**", user["name"])
    st.write("**Email:**", user["email"])
    try:
        member_since = (user['created_at'] + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d')
    except Exception:
        member_since = str(user.get('created_at'))
    st.write("**Member Since:**", member_since + " (+05:30)")
    
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
                    # Show breakdown counts and percentages in compact table
                    total = sum(personality_counts.values())
                    pct_table = pd.DataFrame([
                        {"Type": k, "Count": v, "Percent": f"{v/total:.1%}"}
                        for k, v in personality_counts.items()
                    ])
                    
                    # Display table in smaller columns
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        st.dataframe(pct_table, use_container_width=True, hide_index=True)

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
                        font=dict(size=14, color='#000000'),
                        title_font=dict(size=18, color='#000000'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            gridcolor='rgba(0,0,0,0.2)',
                            linecolor='#000000',
                            tickfont=dict(color='#000000'),
                            title=dict(font=dict(color='#000000'))
                        ),
                        yaxis=dict(
                            gridcolor='rgba(0,0,0,0.2)',
                            linecolor='#000000',
                            tickfont=dict(color='#000000'),
                            title=dict(font=dict(color='#000000'))
                        )
                    )
                    fig.update_traces(
                        marker=dict(line=dict(color='#000000', width=1)),
                        text=[f"{v}" for v in list(personality_counts.values())],
                        textposition='outside',
                        textfont=dict(color='#000000')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Confidence over time
                st.subheader("📈 Confidence Over Time")

                confidence_data = [(test["created_at"], test["confidence"]) for test in reversed(tests)]
                if confidence_data:
                    # Apply timezone offset for display
                    dates, confidences = zip(*confidence_data)
                    try:
                        dates_display = [(d + timedelta(hours=5, minutes=30)) for d in dates]
                    except Exception:
                        dates_display = dates

                    fig = px.line(
                        x=dates_display,
                        y=confidences,
                        title="Test Confidence Over Time",
                        color_discrete_sequence=['#4299e1']
                    )
                    fig.update_layout(
                        xaxis_title="Date (+05:30)",
                        yaxis_title="Confidence",
                        font=dict(size=14, color='#000000'),
                        title_font=dict(size=18, color='#000000'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            gridcolor='rgba(0,0,0,0.2)',
                            linecolor='#000000',
                            tickfont=dict(color='#000000'),
                            title=dict(font=dict(color='#000000'))
                        ),
                        yaxis=dict(
                            gridcolor='rgba(0,0,0,0.2)',
                            linecolor='#000000',
                            tickfont=dict(color='#000000'),
                            title=dict(font=dict(color='#000000'))
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