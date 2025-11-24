"""
Shared Layout Components for EmoSense AI
Provides consistent styling, page configuration, and reusable UI components
"""
import streamlit as st
from typing import Callable


def set_page_config():
    """Configure the Streamlit page with consistent settings"""
    st.set_page_config(
        page_title="EmoSense AI",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_global_styles():
    """Apply global CSS styles for consistent design"""
    st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Page Container */
    .main-container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* Rounded Cards */
    .card {
        background: linear-gradient(145deg, #1e1e1e 0%, #2d2d2d 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.2);
    }
    
    /* Gradient Hero */
    .hero-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 20px #fff, 0 0 30px #667eea;
        }
        to {
            text-shadow: 0 0 30px #fff, 0 0 40px #764ba2;
        }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .hero-detail {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
    }
    
    /* Section Cards */
    .section-card {
        background: linear-gradient(145deg, #1e1e1e 0%, #2d2d2d 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .section-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    /* Headings */
    h1 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #a5b4fc;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #cbd5e1;
        font-weight: 600;
    }
    
    /* Links */
    a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Feature Bullets */
    .feature-list {
        list-style: none;
        padding-left: 0;
    }
    
    .feature-list li {
        padding: 0.75rem 0;
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .feature-list li:last-child {
        border-bottom: none;
    }
    
    .feature-list li::before {
        content: "✓";
        color: #667eea;
        font-weight: bold;
        margin-right: 0.75rem;
        font-size: 1.2rem;
    }
    
    /* Emotion Chips */
    .emotion-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
        background: rgba(102, 126, 234, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Message Bubbles */
    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.75rem 0;
        max-width: 80%;
    }
    
    .message-ai {
        background: linear-gradient(145deg, #2d2d2d 0%, #3d3d3d 100%);
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.75rem 0;
        max-width: 80%;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Spacing */
    .spacer-sm {
        height: 1rem;
    }
    
    .spacer-md {
        height: 2rem;
    }
    
    .spacer-lg {
        height: 3rem;
    }
    
    /* Dark Theme Enhancements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #1e1e1e;
        color: #e2e8f0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #1e1e1e 0%, #2d2d2d 100%);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #a5b4fc;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(145deg, #2d2d2d 0%, #3d3d3d 100%);
        border-color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)


def page_container():
    """Return a container with centered content and max-width"""
    apply_global_styles()
    return st.container()


def section_card(title: str, icon: str, body_fn: Callable):
    """
    Render a beautiful section card with icon, title, and custom body content
    
    Args:
        title: Section title text
        icon: Emoji icon
        body_fn: Function to call that renders the body content
    """
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header">
            <span class="section-icon">{icon}</span>
            <h2 class="section-title">{title}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call the body function to render content
    body_fn()
    
    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)


def hero_section(title: str, subtitle: str, detail: str = ""):
    """Render a gradient hero section"""
    detail_html = f"<p class='hero-detail'>{detail}</p>" if detail else ""
    
    st.markdown(f"""
    <div class="hero-gradient">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        {detail_html}
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, features: list):
    """Render a feature card with bullet points"""
    features_html = "\n".join([f"<li>{feature}</li>" for feature in features])
    
    st.markdown(f"""
    <div class="card">
        <h3 style="font-size: 1.5rem; color: #a5b4fc; margin-bottom: 1rem;">
            {icon} {title}
        </h3>
        <ul class="feature-list">
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)


def emotion_chip(emotion: str, score: float, emoji: str = ""):
    """Render an emotion chip"""
    emoji_text = f"{emoji} " if emoji else ""
    return f'<span class="emotion-chip">{emoji_text}{emotion} • {score:.2f}</span>'


def spacer(size: str = "md"):
    """Add vertical spacing"""
    st.markdown(f"<div class='spacer-{size}'></div>", unsafe_allow_html=True)
