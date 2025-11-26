"""
EmoSense AI - Global Design System
Glassmorphism, gradients, and emotional dark-mode optimized UI
"""
import streamlit as st
from typing import Callable


def set_page_config():
    """Set unified Streamlit page configuration"""
    st.set_page_config(
        page_title="EmoSense AI",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def inject_global_styles():
    """Inject comprehensive global CSS styles"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* === GLOBAL RESETS === */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background: #0E0F14;
    }
    
    /* === GLASSMORPHISM CARDS === */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(138, 92, 246, 0.3);
        border-color: rgba(138, 92, 246, 0.2);
    }
    
    /* === GRADIENT HERO === */
    .gradient-hero {
        background: linear-gradient(135deg, #8A5CF6, #C06CFF);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(138, 92, 246, 0.4);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .gradient-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 1rem;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* === TYPOGRAPHY === */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    h1 { font-size: 2.5rem; margin-bottom: 1rem; }
    h2 { font-size: 2rem; margin-bottom: 0.875rem; }
    h3 { font-size: 1.5rem; margin-bottom: 0.75rem; }
    
    p, li, span {
        color: #A8A9B3;
        line-height: 1.7;
    }
    
    /* === BUTTONS === */
    .stButton > button {
        background: linear-gradient(135deg, #8A5CF6, #C06CFF);
        color: #FFFFFF !important;
        border: none;
        border-radius: 50px;
        padding: 0.875rem 2rem;
        font-weight: 800;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(138, 92, 246, 0.3);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(138, 92, 246, 0.5);
        background: linear-gradient(135deg, #9B6DF7, #D17DFF);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button variant */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(138, 92, 246, 0.4);
    }
    
    /* === EMOTION CHIPS === */
    .emotion-chip {
        display: inline-block;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.875rem;
        font-weight: 600;
        color: #FFFFFF;
        backdrop-filter: blur(10px);
        transition: all 0.2s ease;
    }
    
    .emotion-chip:hover {
        background: rgba(138, 92, 246, 0.2);
        border-color: rgba(138, 92, 246, 0.4);
        transform: translateY(-2px);
    }
    
    .emotion-chip-joy { border-color: rgba(255, 209, 102, 0.5); color: #FFD166; }
    .emotion-chip-sadness { border-color: rgba(0, 196, 204, 0.5); color: #00C4CC; }
    .emotion-chip-anger { border-color: rgba(251, 113, 133, 0.5); color: #FB7185; }
    
    /* === CHAT BUBBLES === */
    .message-user {
        background: linear-gradient(135deg, #8A5CF6, #C06CFF);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.75rem 0;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 4px 12px rgba(138, 92, 246, 0.3);
    }
    
    .message-ai {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.75rem 0;
        max-width: 75%;
        float: left;
        clear: both;
        backdrop-filter: blur(10px);
    }
    
    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: #FFFFFF;
        padding: 0.75rem;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #8A5CF6;
        box-shadow: 0 0 0 2px rgba(138, 92, 246, 0.2);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* === CONTAINER === */
    .main-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* === SECTION CARD === */
    .section-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .section-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .section-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    
    /* === FEATURE BULLETS === */
    .feature-list {
        list-style: none;
        padding-left: 0;
    }
    
    .feature-list li {
        padding: 0.75rem 0;
        color: #A8A9B3;
        font-size: 1rem;
        line-height: 1.6;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .feature-list li:last-child {
        border-bottom: none;
    }
    
    .feature-list li::before {
        content: "✓";
        color: #8A5CF6;
        font-weight: bold;
        margin-right: 0.75rem;
        font-size: 1.2rem;
    }
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(138, 92, 246, 0.4);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(138, 92, 246, 0.6);
    }
    
    /* === METRICS === */
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 1rem;
    }
    
    .stMetric label {
        color: #A8A9B3 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        color: #FFFFFF;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(138, 92, 246, 0.3);
    }
    
    /* === DATAFRAME === */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* === ANIMATIONS === */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* === SPACING === */
    .spacer-sm { height: 1rem; }
    .spacer-md { height: 2rem; }
    .spacer-lg { height: 3rem; }
    .spacer-xl { height: 4rem; }
    
    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: rgba(14, 15, 20, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #FFFFFF;
    }
    
    /* === ACCENT COLORS === */
    .accent-teal { color: #00C4CC; }
    .accent-pink { color: #FB7185; }
    .accent-yellow { color: #FFD166; }
    
    /* === DIVIDER === */
    hr {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin: 2rem 0;
    }
    
    /* === INFO/WARNING/SUCCESS BOXES === */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    </style>
    """, unsafe_allow_html=True)


def page_container():
    """Return a centered container with max-width"""
    inject_global_styles()
    return st.container()



def render_header(active_page: str = "home"):
    """Render top navigation header with active state highlighting"""
    nav_items = [
        {"key": "home", "label": "Home", "href": "/app"},
        {"key": "business", "label": "Business Chatbot", "href": "/business_chatbot"},
        {"key": "personal", "label": "Personal Chatbot", "href": "/personal_chatbot"},
        {"key": "about", "label": "About", "href": "/about"},
    ]

    nav_links = []
    for item in nav_items:
        active_class = " active" if item["key"] == active_page else ""
        nav_links.append(f'<a href="{item["href"]}" class="header-nav-link{active_class}">{item["label"]}</a>')
    nav_links_html = "".join(nav_links)

    header_html = """
    <style>
    .header-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(17, 24, 39, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-logo-icon {
        font-size: 1.75rem;
    }
    
    .header-logo-text {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-nav {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .header-nav-link {
        padding: 0.5rem 1rem;
        color: #A8A9B3;
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .header-nav-link:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #FFFFFF;
    }
    
    .header-nav-link.active {
        background: rgba(102, 126, 234, 0.2);
        color: #667EEA;
    }
    
    .main-content-with-header {
        margin-top: 80px;
    }
    </style>
    
    <div class="header-container">
        <div class="header-content">
            <div class="header-logo">
                <span class="header-logo-icon">dYZ-</span>
                <span class="header-logo-text">EmoSense AI</span>
            </div>
            <div class="header-nav">{NAV_LINKS}</div>
        </div>
    </div>
    <div class="main-content-with-header"></div>
    """

    st.markdown(header_html.replace('{NAV_LINKS}', nav_links_html), unsafe_allow_html=True)


def gradient_hero(title: str, subtitle: str):
    """Render gradient hero section"""
    st.markdown(f"""
    <div class="gradient-hero fade-in">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def section_card(title: str, icon: str, body_fn: Callable):
    """Render a glassmorphic section card with icon and title"""
    st.markdown(f"""
    <div class="section-card fade-in">
        <div class="section-header">
            <span class="section-icon">{icon}</span>
            <h2 class="section-title">{title}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call the body function to render content
    body_fn()


def spacer(size: str = "md"):
    """Add vertical spacing"""
    st.markdown(f'<div class="spacer-{size}"></div>', unsafe_allow_html=True)


def emotion_chip(emotion: str, score: float = None, emoji: str = ""):
    """Render an emotion chip"""
    score_text = f" • {score:.2f}" if score else ""
    emoji_text = f"{emoji} " if emoji else ""
    
    emotion_class = f"emotion-chip-{emotion.lower()}" if emotion.lower() in ['joy', 'sadness', 'anger'] else ""
    
    return f'<span class="emotion-chip {emotion_class}">{emoji_text}{emotion.capitalize()}{score_text}</span>'
