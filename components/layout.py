"""
EmoSense AI - Global Design System
Glassmorphism, gradients, and emotional dark-mode optimized UI
"""
import streamlit as st
from pathlib import Path
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
    """Inject premium global CSS styles"""
    try:
        css = Path("styles/main.css").read_text(encoding="utf-8")
    except Exception:
        css = ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_container():
    """Return a centered container with max-width"""
    inject_global_styles()
    return st.container()

def render_header():
    """Render top navigation header"""
    st.markdown("""
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
        margin-top: 40px;
    }
    </style>
    
    <div class="header-container">
        <div class="header-content">
            <div class="header-logo">
                <span class="header-logo-icon">?</span>
                <span class="header-logo-text">EmoSense AI</span>
            </div>
            <div class="header-nav">
                <a href="/" class="header-nav-link">Home</a>
                <a href="/about" class="header-nav-link">About</a>
                <a href="/business_chatbot" class="header-nav-link">Business Chatbot</a>
                <a href="/personal_chatbot" class="header-nav-link">Personal Chatbot</a>
                <a href="/Terms_and_Conditions" class="header-nav-link">Terms</a>
            </div>
        </div>
    </div>
    <div class="main-content-with-header"></div>
    """, unsafe_allow_html=True)


def gradient_hero(title: str, subtitle: str):
    """Render gradient hero section"""
    st.markdown(f"""
    <div class="gradient-hero fade-in">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, primary_cta: tuple = None, secondary_cta: tuple = None):
    """Render full-width hero with optional CTAs"""
    primary_html = ""
    secondary_html = ""
    if primary_cta:
        primary_label, primary_href = primary_cta
        primary_html = f'<a class="btn-gradient" href="{primary_href}">{primary_label}</a>'
    if secondary_cta:
        secondary_label, secondary_href = secondary_cta
        secondary_html = f'<a class="btn-ghost" href="{secondary_href}">{secondary_label}</a>'
    
    st.markdown(f"""
    <div class="hero fade-in">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
        <div class="hero-ctas">
            {primary_html}
            {secondary_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def gradient_button(label: str, href: str = "#"):
    """Return a gradient button HTML string"""
    return f'<a class="btn-gradient" href="{href}">{label}</a>'


def card(content_html: str):
    """Render a reusable premium card"""
    st.markdown(f'<div class="premium-card fade-in">{content_html}</div>', unsafe_allow_html=True)


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
