import streamlit as st
import pandas as pd
import random
import time
import hashlib
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="🎮 TechPlay Pro - Elite Gaming Hub",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for professional gaming theme
st.markdown("""
<style>
    /* Import gaming fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Gaming Background with animated particles effect */
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 199, 255, 0.3) 0%, transparent 50%),
            linear-gradient(135deg, #0c0c1d 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0e2a5b 100%);
        color: white;
        font-family: 'Rajdhani', sans-serif;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated background elements */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 136, 0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(0, 204, 255, 0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255, 107, 107, 0.3), transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.3), transparent);
        background-repeat: repeat;
        background-size: 150px 150px;
        animation: particle-animation 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particle-animation {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-150px, -150px); }
    }
    
    /* Main header with enhanced styling */
    .main-header {
        background: linear-gradient(45deg, #00ff88, #00ccff, #ff6b6b, #ffd700);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        text-align: center;
        font-weight: 900;
        margin-bottom: 2rem;
        text-shadow: 0 0 50px rgba(0, 255, 136, 0.8);
        animation: gradient-shift 4s ease-in-out infinite, glow-pulse 2s ease-in-out infinite alternate;
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes glow-pulse {
        from { filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.7)); }
        to { filter: drop-shadow(0 0 40px rgba(0, 255, 136, 1)); }
    }
    
    /* Enhanced game card styling */
    .game-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.9) 0%, rgba(26, 26, 46, 0.8) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid transparent;
        background-clip: padding-box;
        backdrop-filter: blur(20px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .game-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 2px;
        background: linear-gradient(45deg, #00ff88, #00ccff, #ff6b6b);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: subtract;
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .game-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(0, 255, 136, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1);
    }
    
    .game-card:hover::before {
        opacity: 1;
    }
    
    /* Platform badges with glow effects */
    .ps3-badge, .ps4-badge, .ps5-badge, .pc-badge, .xbox-badge, .nintendo-badge { 
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .ps3-badge { 
        background: linear-gradient(45deg, #ff9a56, #ff6b6b);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    .ps4-badge { 
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
    }
    
    .ps5-badge { 
        background: linear-gradient(45deg, #667eea, #764ba2);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .pc-badge {
        background: linear-gradient(45deg, #ffd700, #ff8c00);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
    }
    
    .xbox-badge {
        background: linear-gradient(45deg, #107c10, #5cb85c);
        box-shadow: 0 4px 15px rgba(16, 124, 16, 0.4);
    }
    
    .nintendo-badge {
        background: linear-gradient(45deg, #e60012, #ff6b6b);
        box-shadow: 0 4px 15px rgba(230, 0, 18, 0.4);
    }
    
    /* Enhanced success/error messages */
    .success-msg {
        background: linear-gradient(45deg, #00ff88, #4ecdc4);
        color: black;
        padding: 1.5rem;
        border-radius: 15px;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        animation: success-pulse 0.6s ease-out;
    }
    
    .error-msg {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        animation: error-shake 0.6s ease-out;
    }
    
    @keyframes success-pulse {
        0% { transform: scale(0.95); opacity: 0; }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes error-shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00ff88, #00ccff) !important;
        color: black !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Orbitron', monospace !important;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(0, 255, 136, 0.5) !important;
        background: linear-gradient(45deg, #00ccff, #00ff88) !important;
    }
    
    /* Professional sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(0, 0, 0, 0.9) 0%, rgba(26, 26, 46, 0.8) 100%);
        backdrop-filter: blur(20px);
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(145deg, rgba(0, 0, 0, 0.8) 0%, rgba(26, 26, 46, 0.6) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0, 255, 136, 0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stat-card:hover {
        border-color: #00ff88;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 255, 136, 0.2);
    }
    
    /* Floating animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .floating {
        animation: float 4s ease-in-out infinite;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00ff88, #00ccff);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #00ccff, #ff6b6b);
    }
    
    /* Professional welcome card */
    .welcome-card {
        background: linear-gradient(135deg, 
            rgba(0, 255, 136, 0.1) 0%, 
            rgba(0, 204, 255, 0.1) 50%, 
            rgba(255, 107, 107, 0.1) 100%);
        border: 2px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 3s ease-in-out infinite;
        transform: rotate(45deg);
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        50% { transform: translateX(0%) translateY(0%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'users' not in st.session_state:
    st.session_state.users = []
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'pending_verification' not in st.session_state:
    st.session_state.pending_verification = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'verification_code' not in st.session_state:
    st.session_state.verification_code = None
if 'show_verification' not in st.session_state:
    st.session_state.show_verification = False
if 'download_history' not in st.session_state:
    st.session_state.download_history = []
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {}

# Enhanced Game data with more variety
GAMES_DATA = [
    {
        "title": "The Last of Us Part II",
        "platform": "PS4",
        "genre": "Action-Adventure",
        "rating": 5,
        "description": "A gripping post-apocalyptic sequel with unmatched storytelling and emotional depth.",
        "file_size": "78 GB",
        "price": "$59.99",
        "release_year": 2020,
        "developer": "Naughty Dog",
        "multiplayer": False,
        "download_url": "https://example.com/tlou2"
    },
    {
        "title": "God of War Ragnarök",
        "platform": "PS5", 
        "genre": "Action-Adventure",
        "rating": 5,
        "description": "Kratos and Atreus embark on a mythic journey for answers and allies in Norse realms.",
        "file_size": "84 GB",
        "price": "$69.99",
        "release_year": 2022,
        "developer": "Santa Monica Studio",
        "multiplayer": False,
        "download_url": "https://example.com/gow-ragnarok"
    },
    {
        "title": "Spider-Man: Miles Morales",
        "platform": "PS5",
        "genre": "Action-Adventure", 
        "rating": 4,
        "description": "Experience the rise of Miles Morales with incredible ray tracing and haptic feedback.",
        "file_size": "52 GB",
        "price": "$49.99",
        "release_year": 2020,
        "developer": "Insomniac Games",
        "multiplayer": False,
        "download_url": "https://example.com/miles-morales"
    },
    {
        "title": "Cyberpunk 2077",
        "platform": "PC",
        "genre": "Action RPG",
        "rating": 4,
        "description": "An open-world action-adventure story set in Night City, a megalopolis obsessed with power.",
        "file_size": "62 GB",
        "price": "$29.99",
        "release_year": 2020,
        "developer": "CD Projekt RED",
        "multiplayer": False,
        "download_url": "https://example.com/cyberpunk"
    },
    {
        "title": "Halo Infinite",
        "platform": "Xbox",
        "genre": "FPS",
        "rating": 4,
        "description": "Master Chief returns in the most expansive Master Chief campaign yet.",
        "file_size": "48 GB",
        "price": "Free",
        "release_year": 2021,
        "developer": "343 Industries",
        "multiplayer": True,
        "download_url": "https://example.com/halo-infinite"
    },
    {
        "title": "The Legend of Zelda: Breath of the Wild",
        "platform": "Nintendo",
        "genre": "Action-Adventure",
        "rating": 5,
        "description": "Step into a world of discovery, exploration, and adventure in Hyrule.",
        "file_size": "13 GB",
        "price": "$59.99",
        "release_year": 2017,
        "developer": "Nintendo EPD",
        "multiplayer": False,
        "download_url": "https://example.com/zelda-botw"
    },
    {
        "title": "Horizon Forbidden West",
        "platform": "PS5",
        "genre": "Action RPG",
        "rating": 5,
        "description": "Join Aloy as she braves the Forbidden West to find the source of a mysterious plague.",
        "file_size": "87 GB",
        "price": "$69.99",
        "release_year": 2022,
        "developer": "Guerrilla Games",
        "multiplayer": False,
        "download_url": "https://example.com/horizon-fw"
    },
    {
        "title": "Elden Ring",
        "platform": "PC",
        "genre": "Action RPG",
        "rating": 5,
        "description": "A fantasy action-RPG adventure set within a world created by Hidetaka Miyazaki and George R.R. Martin.",
        "file_size": "60 GB",
        "price": "$59.99",
        "release_year": 2022,
        "developer": "FromSoftware",
        "multiplayer": True,
        "download_url": "https://example.com/elden-ring"
    },
    {
        "title": "Forza Horizon 5",
        "platform": "Xbox",
        "genre": "Racing",
        "rating": 5,
        "description": "Explore the vibrant and ever-evolving open world landscapes of Mexico.",
        "file_size": "104 GB",
        "price": "$59.99",
        "release_year": 2021,
        "developer": "Playground Games",
        "multiplayer": True,
        "download_url": "https://example.com/forza-h5"
    },
    {
        "title": "Ratchet & Clank: Rift Apart",
        "platform": "PS5",
        "genre": "Platform",
        "rating": 4,
        "description": "Dimension-hopping adventure showcasing the PS5's incredible SSD speed and DualSense features.",
        "file_size": "42 GB", 
        "price": "$69.99",
        "release_year": 2021,
        "developer": "Insomniac Games",
        "multiplayer": False,
        "download_url": "https://example.com/ratchet"
    }
]

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    """Simulate sending verification email with better UI"""
    st.markdown(f"""
    <div style="background: linear-gradient(45deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 255, 0.2)); 
                border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
        <h4 style="color: #00ff88; margin-bottom: 1rem;">📧 Verification Email Sent!</h4>
        <p style="margin-bottom: 0.5rem;"><strong>To:</strong> {email}</p>
        <p style="margin-bottom: 0.5rem;"><strong>Verification Code:</strong> <span style="color: #ffd700; font-weight: bold; font-size: 1.2rem;">{code}</span></p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Please enter this code to verify your account.</p>
    </div>
    """, unsafe_allow_html=True)
    return True

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """Verify user credentials"""
    for user in st.session_state.users:
        if user['username'] == username and user['password'] == hash_password(password):
            return user
    return None

def register_user(username, email, password):
    """Register new user with enhanced validation"""
    # Enhanced validation
    if len(username) < 3:
        return False, "Username must be at least 3 characters long!"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address!"
    
    # Check if user already exists
    for user in st.session_state.users:
        if user['username'].lower() == username.lower():
            return False, "Username already exists!"
        if user['email'].lower() == email.lower():
            return False, "Email already registered!"
    
    # Generate verification code
    code = generate_verification_code()
    st.session_state.verification_code = code
    st.session_state.pending_verification = {
        'username': username,
        'email': email,
        'password': hash_password(password),
        'code': code,
        'timestamp': datetime.now()
    }
    
    # Send verification email
    send_verification_email(email, code)
    return True, "Registration successful! Please check your email for verification code."

def verify_email_code(entered_code):
    """Verify the email verification code"""
    if (st.session_state.pending_verification and 
        entered_code == st.session_state.pending_verification['code']):
        
        # Add user to registered users
        new_user = {
            'username': st.session_state.pending_verification['username'],
            'email': st.session_state.pending_verification['email'], 
            'password': st.session_state.pending_verification['password'],
            'join_date': datetime.now().strftime("%Y-%m-%d"),
            'verified': True,
            'downloads': 0,
            'favorite_genre': 'Action',
            'last_login': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.users.append(new_user)
        
        # Clear pending verification
        st.session_state.pending_verification = {}
        st.session_state.verification_code = None
        st.session_state.show_verification = False
        
        return True
    return False

def display_game_card(game, col_key):
    """Display enhanced game card with more information"""
    platform_class = f"{game['platform'].lower()}-badge"
    stars = "⭐" * game['rating'] + "☆" * (5 - game['rating'])
    
    # Determine platform icon
    platform_icons = {
        "PS3": "🎮", "PS4": "🎮", "PS5": "🎮",
        "PC": "🖥️", "Xbox": "🎯", "Nintendo": "🎲"
    }
    platform_icon = platform_icons.get(game['platform'], "🎮")
    
    # Price color based on value
    price_color = "#00ff88" if game['price'] == "Free" else "#ffd700"
    
    with st.container():
        st.markdown(f"""
        <div class="game-card floating">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="color: #00ff88; margin: 0; font-family: 'Orbitron', monospace;">{platform_icon} {game['title']}</h3>
                <span class="{platform_class}">{game['platform']}</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <p style="color: #00ccff; margin-bottom: 0.5rem;"><strong>🎯 Genre:</strong> {game['genre']}</p>
                    <p style="margin-bottom: 0.5rem;"><strong>⭐ Rating:</strong> {stars} ({game['rating']}/5)</p>
                    <p style="color: #ff6b6b; margin-bottom: 0.5rem;"><strong>📅 Year:</strong> {game['release_year']}</p>
                </div>
                <div>
                    <p style="color: {price_color}; font-weight: bold; margin-bottom: 0.5rem;">💰 Price: {game['price']}</p>
                    <p style="color: #ffd700; font-weight: bold; margin-bottom: 0.5rem;">📁 Size: {game['file_size']}</p>
                    <p style="color: #a8edea; margin-bottom: 0.5rem;"><strong>🏢 Dev:</strong> {game['developer']}</p>
                </div>
            </div>
            
            <p style="margin-bottom: 1rem; color: rgba(255,255,255,0.8); line-height: 1.4;">{game['description']}</p>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {'#00ff88' if game['multiplayer'] else '#ff6b6b'}; font-weight: bold;">
                    {'🌐 Multiplayer' if game['multiplayer'] else '👤 Single Player'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"⬇️ Download {game['title']}", key=f"download_{game['title']}_{col_key}", type="primary"):
                # Add to download history
                download_entry = {
                    'game': game['title'],
                    'platform': game['platform'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'size': game['file_size']
                }
                st.session_state.download_history.append(download_entry)
                
                # Update user download count
                if st.session_state.current_user:
                    for user in st.session_state.users:
                        if user['username'] == st.session_state.current_user['username']:
                            user['downloads'] = user.get('downloads', 0) + 1
                            break
                
                st.success(f"🎉 {game['title']} download started! Check your downloads folder.")
                st.balloons()
        
        with col2:
            if st.button("❤️", key=f"fav_{game['title']}_{col_key}", help="Add to favorites"):
                st.info("Added to favorites! ❤️")

def display_user_stats():
    """Display user statistics with charts"""
    if not st.session_state.current_user:
        return
    
    st.markdown("## 📊 Your Gaming Dashboard")
    
    # User stats metrics
    col1, col2, col3, col4 = st.columns(4)
    
    user_downloads = st.session_state.current_user.get('downloads', 0)
    total_games = len(GAMES_DATA)
    avg_rating = sum(g['rating'] for g in GAMES_DATA) / len(GAMES_DATA)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #00ff88; margin-bottom: 0.5rem;">🎮</h3>
            <h2 style="color: white; margin-bottom: 0.5rem;">{user_downloads}</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 0;">Downloads</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #00ccff; margin-bottom: 0.5rem;">📚</h3>
            <h2 style="color: white; margin-bottom: 0.5rem;">{total_games}</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 0;">Available Games</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #ffd700; margin-bottom: 0.5rem;">⭐</h3>
            <h2 style="color: white; margin-bottom: 0.5rem;">{avg_rating:.1f}</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 0;">Avg Rating</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        days_since_join = (datetime.now() - datetime.strptime(st.session_state.current_user.get('join_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")).days
        st.markdown(f"""
        <div class="stat-card">
            <h3 style="color: #ff6b6b; margin-bottom: 0.5rem;">📅</h3>
            <h2 style="color: white; margin-bottom: 0.5rem;">{days_since_join}</h2>
            <p style="color: rgba(255,255,255,0.7); margin: 0;">Days Member</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Download history chart
    if st.session_state.download_history:
        st.markdown("### 📈 Download Activity")
        
        # Create download history dataframe
        df_downloads = pd.DataFrame(st.session_state.download_history)
        df_downloads['date'] = pd.to_datetime(df_downloads['timestamp']).dt.date
        daily_downloads = df_downloads.groupby('date').size().reset_index(name='downloads')
        
        # Create interactive chart
        fig = px.line(daily_downloads, x='date', y='downloads', 
                     title='Daily Download Activity',
                     color_discrete_sequence=['#00ff88'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#00ff88'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Platform distribution
        platform_counts = df_downloads['platform'].value_counts()
        fig_pie = px.pie(values=platform_counts.values, names=platform_counts.index,
                        title='Downloads by Platform',
                        color_discrete_sequence=['#00ff88', '#00ccff', '#ff6b6b', '#ffd700', '#a8edea'])
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#00ccff'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

def display_sidebar():
    """Enhanced sidebar with user preferences and quick actions"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, rgba(0,255,136,0.2), rgba(0,204,255,0.2)); 
                    border-radius: 15px; margin-bottom: 2rem;">
            <h2 style="color: #00ff88; margin-bottom: 0.5rem;">🎮 TechPlay Pro</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Elite Gaming Hub</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.logged_in and st.session_state.current_user:
            st.markdown(f"### 👋 Welcome, {st.session_state.current_user['username']}!")
            
            # Quick stats
            st.markdown("#### 📊 Quick Stats")
            st.metric("Downloads", st.session_state.current_user.get('downloads', 0))
            st.metric("Member Since", st.session_state.current_user.get('join_date', 'Recently'))
            
            st.markdown("---")
            
            # User preferences
            st.markdown("#### ⚙️ Preferences")
            preferred_platform = st.selectbox(
                "Favorite Platform:",
                ["All", "PS3", "PS4", "PS5", "PC", "Xbox", "Nintendo"],
                key="user_platform_pref"
            )
            
            preferred_genre = st.selectbox(
                "Favorite Genre:",
                ["All", "Action", "Action-Adventure", "Action RPG", "FPS", "Racing", "Platform"],
                key="user_genre_pref"
            )
            
            # Save preferences
            if st.button("💾 Save Preferences", type="secondary"):
                st.session_state.user_preferences = {
                    'platform': preferred_platform,
                    'genre': preferred_genre
                }
                st.success("Preferences saved!")
            
            st.markdown("---")
            
            # Recent downloads
            if st.session_state.download_history:
                st.markdown("#### 📥 Recent Downloads")
                recent_downloads = st.session_state.download_history[-3:]  # Last 3 downloads
                for download in reversed(recent_downloads):
                    st.markdown(f"• **{download['game']}** ({download['platform']})")
            
            st.markdown("---")
            
            # Quick actions
            st.markdown("#### ⚡ Quick Actions")
            if st.button("🔄 Refresh Games", type="secondary"):
                st.rerun()
            
            if st.button("📊 View Full Stats", type="secondary"):
                st.session_state.show_full_stats = True
            
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.success("👋 Logged out successfully!")
                time.sleep(1)
                st.rerun()
        
        else:
            st.markdown("### 🔐 Authentication Required")
            st.info("Please login or register to access the gaming hub.")
            
            # Quick registration form in sidebar
            st.markdown("#### 📝 Quick Register")
            with st.form("sidebar_register"):
                sidebar_username = st.text_input("Username", key="sidebar_username")
                sidebar_email = st.text_input("Email", key="sidebar_email")
                sidebar_password = st.text_input("Password", type="password", key="sidebar_password")
                
                if st.form_submit_button("🚀 Join Now", type="primary"):
                    if sidebar_username and sidebar_email and sidebar_password:
                        success, message = register_user(sidebar_username, sidebar_email, sidebar_password)
                        if success:
                            st.success(message)
                            st.session_state.show_verification = True
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill all fields!")

def main():
    # Display sidebar
    display_sidebar()
    
    # Header with enhanced animation
    st.markdown('<h1 class="main-header">🎮 TECHPLAY PRO 🎮</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.4rem; color: #00ccff; margin-bottom: 0.5rem; font-family: 'Orbitron', monospace;">
            ✨ Elite Gaming Hub - Premium Console Games ✨
        </p>
        <p style="color: rgba(255,255,255,0.7); font-size: 1.1rem;">
            Download the latest and greatest games across all platforms
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication Section
    if not st.session_state.logged_in:
        # Show verification modal if needed
        if st.session_state.show_verification:
            st.markdown("## 📧 Email Verification Required")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div class="welcome-card">
                    <h3 style="color: #00ff88; margin-bottom: 1rem;">🔐 Verify Your Account</h3>
                    <p style="margin-bottom: 1.5rem;">We've sent a 6-digit verification code to:</p>
                    <p style="color: #ffd700; font-weight: bold; font-size: 1.1rem; margin-bottom: 1.5rem;">
                        {st.session_state.pending_verification.get('email', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                verification_code = st.text_input(
                    "Enter 6-digit verification code:", 
                    max_chars=6, 
                    key="verification_input",
                    help="Check your email for the verification code",
                    placeholder="123456"
                )
                
                col_verify, col_resend = st.columns(2)
                with col_verify:
                    if st.button("✅ Verify Account", type="primary", use_container_width=True):
                        if len(verification_code) == 6 and verification_code.isdigit():
                            if verify_email_code(verification_code):
                                st.markdown('<div class="success-msg">🎉 Account verified successfully! You can now login.</div>', unsafe_allow_html=True)
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.markdown('<div class="error-msg">❌ Invalid verification code! Please try again.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-msg">❌ Please enter a valid 6-digit code!</div>', unsafe_allow_html=True)
                
                with col_resend:
                    if st.button("📧 Resend Code", type="secondary", use_container_width=True):
                        new_code = generate_verification_code()
                        st.session_state.verification_code = new_code
                        st.session_state.pending_verification['code'] = new_code
                        send_verification_email(st.session_state.pending_verification['email'], new_code)
        else:
            # Enhanced Login/Register interface
            st.markdown("## 🚀 Join the Ultimate Gaming Experience")
            
            tab1, tab2 = st.tabs(["🔐 **Login**", "📝 **Create Account**"])
            
            with tab1:
                st.markdown("### 🎮 Welcome Back, Gamer!")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("""
                    <div class="welcome-card">
                        <h4 style="color: #00ff88; margin-bottom: 1rem;">Login to Your Gaming Hub</h4>
                        <p style="color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">
                            Access your personal gaming library and download history
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    username = st.text_input("👤 Username or Email", key="login_username", placeholder="Enter your username")
                    password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
                    
                    col_login, col_demo = st.columns(2)
                    with col_login:
                        if st.button("🚀 Login to TechPlay", type="primary", use_container_width=True):
                            if username and password:
                                user = verify_user(username, password)
                                if user:
                                    st.session_state.current_user = user
                                    st.session_state.logged_in = True
                                    user['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                    st.markdown('<div class="success-msg">🎉 Welcome back! Loading your gaming hub...</div>', unsafe_allow_html=True)
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.markdown('<div class="error-msg">❌ Invalid credentials! Please check your username and password.</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="error-msg">⚠️ Please fill in all fields!</div>', unsafe_allow_html=True)
                    
                    with col_demo:
                        if st.button("🎯 Demo Login", type="secondary", use_container_width=True):
                            # Auto-fill demo credentials
                            st.info("Demo credentials: **gamer1** / **password123**")
            
            with tab2:
                st.markdown("### 🌟 Join the Elite Gaming Community!")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("""
                    <div class="welcome-card">
                        <h4 style="color: #00ccff; margin-bottom: 1rem;">Create Your Gaming Account</h4>
                        <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">
                            Join thousands of gamers and get instant access to:
                        </p>
                        <ul style="color: rgba(255,255,255,0.7); text-align: left; margin-bottom: 1.5rem;">
                            <li>🎮 Unlimited game downloads</li>
                            <li>📊 Personal gaming statistics</li>
                            <li>❤️ Favorites and wishlist</li>
                            <li>🔔 New game notifications</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    reg_username = st.text_input("👤 Choose Username", key="reg_username", placeholder="Enter a unique username (min 3 chars)")
                    reg_email = st.text_input("📧 Email Address", key="reg_email", placeholder="your.email@example.com") 
                    reg_password = st.text_input("🔒 Create Password", type="password", key="reg_password", placeholder="Enter a secure password (min 6 chars)")
                    
                    # Password strength indicator
                    if reg_password:
                        strength = "Weak" if len(reg_password) < 8 else "Strong"
                        color = "#ff6b6b" if strength == "Weak" else "#00ff88"
                        st.markdown(f"<p style='color: {color}; font-size: 0.9rem;'>Password strength: **{strength}**</p>", unsafe_allow_html=True)
                    
                    agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="agree_terms")
                    
                    if st.button("🎯 Create Gaming Account", type="primary", use_container_width=True, disabled=not agree_terms):
                        if reg_username and reg_email and reg_password:
                            if agree_terms:
                                success, message = register_user(reg_username, reg_email, reg_password)
                                if success:
                                    st.markdown('<div class="success-msg">🎉 Registration successful! Check your email for verification.</div>', unsafe_allow_html=True)
                                    st.session_state.show_verification = True
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="error-msg">⚠️ Please agree to the terms to continue!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-msg">⚠️ Please fill in all fields!</div>', unsafe_allow_html=True)
    
    else:
        # Main Application - User is logged in
        # Enhanced Welcome Section
        st.markdown(f"""
        <div class="welcome-card">
            <h2 style="color: #00ff88; margin-bottom: 1rem;">🎉 Welcome back, {st.session_state.current_user['username']}! 🎉</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 0.5rem;">
                Ready to explore and download the ultimate gaming collection?
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <span style="color: rgba(255,255,255,0.7);">📅 Member since: <strong>{st.session_state.current_user.get('join_date', 'Recently')}</strong></span>
                <span style="color: rgba(255,255,255,0.7);">⬇️ Downloads: <strong>{st.session_state.current_user.get('downloads', 0)}</strong></span>
                <span style="color: rgba(255,255,255,0.7);">🕒 Last login: <strong>{st.session_state.current_user.get('last_login', 'Now')}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display user statistics
        display_user_stats()
        
        st.markdown("---")
        
        # Enhanced Games Section
        st.markdown("## 🎮 Premium Game Collection")
        
        # Advanced filter options
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            platform_filter = st.selectbox("🎯 Platform:", 
                                ["All", "PS3", "PS4", "PS5", "PC", "Xbox", "Nintendo"])
        with col2:
            genre_filter = st.selectbox("🎪 Genre:", 
                                ["All", "Action", "Action-Adventure", "Action RPG", "FPS", "Racing", "Platform"])
        with col3:
            sort_by = st.selectbox("📊 Sort by:", 
                                ["Title", "Rating", "Platform", "Release Year", "File Size"])
        with col4:
            view_mode = st.selectbox("👁️ View:", 
                                ["Grid", "List", "Detailed"])
        
        # Search functionality
        search_term = st.text_input("🔍 Search games...", placeholder="Enter game title, developer, or keyword")
        
        # Filter and sort games
        filtered_games = GAMES_DATA
        
        # Apply search filter
        if search_term:
            search_term = search_term.lower()
            filtered_games = [g for g in filtered_games if 
                            search_term in g['title'].lower() or 
                            search_term in g['developer'].lower() or 
                            search_term in g['genre'].lower()]
        
        # Apply platform filter
        if platform_filter != "All":
            filtered_games = [g for g in filtered_games if g['platform'] == platform_filter]
        
        # Apply genre filter
        if genre_filter != "All":
            filtered_games = [g for g in filtered_games if g['genre'] == genre_filter]
        
        # Apply sorting
        if sort_by == "Rating":
            filtered_games = sorted(filtered_games, key=lambda x: x['rating'], reverse=True)
        elif sort_by == "Platform":
            filtered_games = sorted(filtered_games, key=lambda x: x['platform'])
        elif sort_by == "Release Year":
            filtered_games = sorted(filtered_games, key=lambda x: x['release_year'], reverse=True)
        elif sort_by == "File Size":
            filtered_games = sorted(filtered_games, key=lambda x: int(x['file_size'].split()[0]), reverse=True)
        else:
            filtered_games = sorted(filtered_games, key=lambda x: x['title'])
        
        # Display games count and filters summary
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.5); padding: 1rem; border-radius: 10px; margin: 1rem 0; 
                    border-left: 4px solid #00ff88;">
            <strong>📚 Found {len(filtered_games)} games</strong>
            {f" • 🎯 Platform: {platform_filter}" if platform_filter != "All" else ""}
            {f" • 🎪 Genre: {genre_filter}" if genre_filter != "All" else ""}
            {f" • 🔍 Search: '{search_term}'" if search_term else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # Display games based on view mode
        if view_mode == "Grid":
            # Grid view - 3 columns
            num_cols = 3
            cols = st.columns(num_cols)
            
            for idx, game in enumerate(filtered_games):
                with cols[idx % num_cols]:
                    display_game_card(game, f"grid_{idx}")
        
        elif view_mode == "List":
            # List view - 2 columns
            num_cols = 2
            cols = st.columns(num_cols)
            
            for idx, game in enumerate(filtered_games):
                with cols[idx % num_cols]:
                    display_game_card(game, f"list_{idx}")
        
        else:  # Detailed view
            # Single column detailed view
            for idx, game in enumerate(filtered_games):
                display_game_card(game, f"detailed_{idx}")
                if idx < len(filtered_games) - 1:
                    st.markdown("---")
        
        # No games found message
        if not filtered_games:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: rgba(255,107,107,0.1); 
                        border: 2px dashed rgba(255,107,107,0.3); border-radius: 15px; margin: 2rem 0;">
                <h3 style="color: #ff6b6b; margin-bottom: 1rem;">🔍 No Games Found</h3>
                <p style="color: rgba(255,255,255,0.7);">
                    Try adjusting your filters or search terms to find games.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Featured section
        st.markdown("---")
        st.markdown("## 🌟 Featured & Trending")
        
        # Get top-rated games
        featured_games = sorted(GAMES_DATA, key=lambda x: x['rating'], reverse=True)[:3]
        
        cols = st.columns(3)
        for idx, game in enumerate(featured_games):
            with cols[idx]:
                st.markdown(f"""
                <div style="background: linear-gradient(45deg, rgba(255,215,0,0.2), rgba(255,107,107,0.2)); 
                            border: 2px solid rgba(255,215,0,0.3); border-radius: 15px; padding: 1.5rem; text-align: center;">
                    <h4 style="color: #ffd700; margin-bottom: 0.5rem;">🏆 {game['title']}</h4>
                    <p style="color: white; margin-bottom: 0.5rem;">{'⭐' * game['rating']} ({game['rating']}/5)</p>
                    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{game['platform']} • {game['genre']}</p>
                </div>
                """, unsafe_allow_html=True)

# Initialize demo users if none exist
if not st.session_state.users:
    demo_users = [
        {
            'username': 'gamer1',
            'email': 'gamer1@techplay.com',
            'password': hash_password('password123'),
            'join_date': '2024-01-15',
            'verified': True,
            'downloads': 15,
            'favorite_genre': 'Action-Adventure',
            'last_login': '2024-12-10 14:30'
        },
        {
            'username': 'player2', 
            'email': 'player2@techplay.com',
            'password': hash_password('gaming456'),
            'join_date': '2024-02-20',
            'verified': True,
            'downloads': 8,
            'favorite_genre': 'RPG',
            'last_login': '2024-12-09 18:45'
        },
        {
            'username': 'progamer',
            'email': 'pro@techplay.com', 
            'password': hash_password('elite999'),
            'join_date': '2023-12-01',
            'verified': True,
            'downloads': 42,
            'favorite_genre': 'FPS',
            'last_login': '2024-12-10 12:15'
        }
    ]
    st.session_state.users = demo_users

if __name__ == "__main__":
    main()