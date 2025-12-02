"""
EmoSense AI - Single Flow App
State-machine architecture for seamless guided user journey

Stages:
0 - Welcome Screen
1 - Select Mode (Business Buddy / Personal Companion)
2 - Age + Goal Input
3 - COPE Questionnaire (28 items)
4 - Persona Assignment Summary
5 - Persona-Based Chatbot (Personal)
6 - Business Buddy Dashboard
"""
import sys
import os
import re
import hashlib
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# Fix import path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

# Core imports
from utils.predict import predict_emotions
from utils.labels import EMOTIONS, EMOJI_MAP

# Services
from services.cope_assessment_service import (
    COPE_QUESTIONS,
    RESPONSE_OPTIONS,
    SUBSCALE_INFO,
    PERSONA_INFO,
    compute_cope_scores,
    assign_persona,
    get_coping_profile_summary
)
from services.persona_engine import (
    get_persona_engine,
    get_persona_prompt,
    get_persona_metadata,
    PERSONA_METADATA
)

# Optional services with fallbacks
try:
    from services.voice_chat_service import get_voice_chat_service
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

try:
    from services.personal_llm_service import get_personal_llm_service
    PERSONAL_LLM_AVAILABLE = True
except:
    PERSONAL_LLM_AVAILABLE = False

try:
    from services.summary_service_local import summarize_text_local
    SUMMARY_AVAILABLE = True
except:
    SUMMARY_AVAILABLE = False

try:
    from services.answer_comparison_service import get_comparison_service
    COMPARISON_AVAILABLE = True
except:
    COMPARISON_AVAILABLE = False

# Try plotly for charts
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except:
    PLOTLY_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EmoSense AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL STYLES
# ============================================================

st.markdown("""
<style>
/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Global dark theme */
.stApp {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
    min-height: 100vh;
}

/* Progress bar */
.progress-container {
    background: rgba(17, 24, 39, 0.6);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(138, 92, 246, 0.2);
}

.progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.progress-step {
    color: #C4B5FD;
    font-weight: 600;
    font-size: 0.9rem;
}

.progress-title {
    color: #9CA3AF;
    font-size: 0.85rem;
}

.progress-bar-bg {
    background: rgba(138, 92, 246, 0.2);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
}

.progress-bar-fill {
    background: linear-gradient(90deg, #667EEA 0%, #8B5CF6 50%, #EC4899 100%);
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}

/* Stage container */
.stage-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}

/* Hero section */
.hero-section {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(236, 72, 153, 0.1) 100%);
    border-radius: 24px;
    border: 1px solid rgba(138, 92, 246, 0.2);
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667EEA 0%, #8B5CF6 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.hero-subtitle {
    color: #9CA3AF;
    font-size: 1.25rem;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
}

/* Cards */
.glass-card {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(138, 92, 246, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(138, 92, 246, 0.4);
    transform: translateY(-2px);
}

/* Mode selection cards */
.mode-card {
    background: rgba(17, 24, 39, 0.6);
    border: 2px solid rgba(138, 92, 246, 0.3);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.mode-card:hover {
    border-color: #8B5CF6;
    transform: translateY(-4px);
    box-shadow: 0 10px 40px rgba(138, 92, 246, 0.2);
}

.mode-card.selected {
    border-color: #8B5CF6;
    background: rgba(138, 92, 246, 0.15);
}

.mode-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.mode-title {
    color: #FFFFFF;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.mode-desc {
    color: #9CA3AF;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* Question cards */
.question-card {
    background: rgba(17, 24, 39, 0.5);
    border: 1px solid rgba(138, 92, 246, 0.15);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.question-number {
    color: #8B5CF6;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

.question-text {
    color: #E5E7EB;
    font-size: 1rem;
    line-height: 1.5;
    margin-bottom: 1rem;
}

/* Persona card */
.persona-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
    border: 2px solid rgba(138, 92, 246, 0.4);
    border-radius: 24px;
    padding: 2.5rem;
    text-align: center;
}

.persona-emoji {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.persona-name {
    color: #FFFFFF;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.persona-therapy {
    color: #C4B5FD;
    font-size: 1rem;
    margin-bottom: 1rem;
}

.persona-description {
    color: #D1D5DB;
    font-size: 1.1rem;
    line-height: 1.7;
    max-width: 500px;
    margin: 0 auto 1.5rem;
}

/* Chat interface */
.chat-container {
    max-height: 450px;
    overflow-y: auto;
    padding: 1rem;
    background: rgba(17, 24, 39, 0.3);
    border-radius: 16px;
    margin-bottom: 1rem;
    border: 1px solid rgba(138, 92, 246, 0.2);
}

.message-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.875rem 1.25rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0 0.5rem auto;
    max-width: 75%;
    width: fit-content;
    float: right;
    clear: both;
}

.message-bot {
    background: rgba(138, 92, 246, 0.15);
    border: 1px solid rgba(138, 92, 246, 0.3);
    color: #E5E7EB;
    padding: 0.875rem 1.25rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.5rem auto 0.5rem 0;
    max-width: 75%;
    width: fit-content;
    float: left;
    clear: both;
}

.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

/* Emotion chip */
.emotion-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(138, 92, 246, 0.2);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #C4B5FD;
    margin-top: 0.5rem;
}

/* Business section */
.analysis-card {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(138, 92, 246, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: #8B5CF6;
}

.stat-label {
    color: #9CA3AF;
    font-size: 0.9rem;
}

/* Buttons */
.primary-btn {
    background: linear-gradient(135deg, #667EEA 0%, #8B5CF6 100%);
    color: white;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 12px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(138, 92, 246, 0.4);
}

.secondary-btn {
    background: transparent;
    color: #C4B5FD;
    border: 2px solid rgba(138, 92, 246, 0.4);
    padding: 0.75rem 1.5rem;
    border-radius: 10px;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.secondary-btn:hover {
    background: rgba(138, 92, 246, 0.1);
    border-color: #8B5CF6;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem;
    color: #6B7280;
    font-size: 0.85rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(138, 92, 246, 0.1);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        # Flow control
        "stage": 0,
        "mode": None,  # "personal" or "business"
        
        # User profile
        "user_age": 25,
        "user_goal": None,
        
        # COPE assessment
        "cope_answers": {},
        "cope_scores": {},
        "persona": None,
        "persona_info": None,
        
        # Chat state (Personal)
        "chat_history": [],
        "emotion_history": [],
        "last_audio_hash": None,
        "pending_tts_audio": None,
        
        # Business analysis state
        "business_comments": [],
        "business_emotions": {},
        "business_summary": "",
        "business_chat_history": [],
        "analysis_complete": False,
        
        # UI state
        "clear_input": False,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_markdown_to_html(text: str) -> str:
    """Convert markdown to HTML for rendering"""
    if not text:
        return text
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Numbered lists
    text = re.sub(r'^(\d+)\.\s+', r'<strong>\1.</strong> ', text, flags=re.MULTILINE)
    # Bullet points
    text = re.sub(r'^-\s+', r'• ', text, flags=re.MULTILINE)
    # Line breaks
    text = text.replace('\n', '<br>')
    
    return text


def get_dominant_emotion(text: str) -> Tuple[str, float]:
    """Get dominant emotion from text"""
    try:
        emotions, probs = predict_emotions(text, threshold=0.1)
        if probs:
            dominant = max(probs.items(), key=lambda x: x[1])
            return dominant[0], dominant[1]
    except:
        pass
    return "neutral", 0.5


def render_progress_bar(stage: int, stage_names: Dict[int, str]):
    """Render progress indicator"""
    total_stages = 6
    progress = (stage / total_stages) * 100
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-header">
            <span class="progress-step">Step {stage + 1} of {total_stages + 1}</span>
            <span class="progress-title">{stage_names.get(stage, '')}</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def reset_journey():
    """Reset all session state to start fresh"""
    keys_to_reset = [
        "stage", "mode", "user_age", "user_goal",
        "cope_answers", "cope_scores", "persona", "persona_info",
        "chat_history", "emotion_history", "last_audio_hash", "pending_tts_audio",
        "business_comments", "business_emotions", "business_summary",
        "business_chat_history", "analysis_complete"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    init_session_state()
    st.rerun()


# ============================================================
# STAGE 0: WELCOME SCREEN
# ============================================================

def render_welcome():
    """Render welcome screen"""
    st.markdown('<div class="stage-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🎭 EmoSense AI</div>
        <div class="hero-subtitle">
            Your emotion-aware AI companion for personal wellbeing and business insights.
            Discover your unique coping style and get personalized support.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">💜</div>
            <div style="color: #FFFFFF; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Personal Companion</div>
            <div style="color: #9CA3AF; font-size: 0.95rem; line-height: 1.5;">
                A caring AI friend that adapts to your emotional style.
                Voice & text chat with 28-emotion detection.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">💼</div>
            <div style="color: #FFFFFF; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">Business Buddy</div>
            <div style="color: #9CA3AF; font-size: 0.95rem; line-height: 1.5;">
                Deep sentiment analysis for customer feedback.
                Viral detection, root cause analysis, smart summaries.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Start Your Journey", type="primary", use_container_width=True):
            st.session_state.stage = 1
            st.rerun()
    
    # Quick access for returning users
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.85rem;">
        Already completed onboarding? 
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        skip_col1, skip_col2 = st.columns(2)
        with skip_col1:
            if st.button("Skip to Personal Chat", use_container_width=True):
                st.session_state.stage = 5
                st.session_state.mode = "personal"
                st.session_state.persona = "Gentle Sensitive"
                st.session_state.persona_info = PERSONA_INFO.get("Gentle Sensitive", {})
                st.rerun()
        with skip_col2:
            if st.button("Skip to Business Buddy", use_container_width=True):
                st.session_state.stage = 6
                st.session_state.mode = "business"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# STAGE 1: SELECT MODE
# ============================================================

def render_mode_select():
    """Render mode selection screen"""
    render_progress_bar(1, STAGE_NAMES)
    
    st.markdown('<div class="stage-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFFFFF; font-size: 2rem; margin-bottom: 0.5rem;">How would you like to use EmoSense?</h1>
        <p style="color: #9CA3AF; font-size: 1.1rem;">Choose your path and we'll personalize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        personal_selected = st.session_state.mode == "personal"
        st.markdown(f"""
        <div class="mode-card {'selected' if personal_selected else ''}">
            <div class="mode-icon">💜</div>
            <div class="mode-title">Personal Companion</div>
            <div class="mode-desc">
                An emotionally intelligent AI friend that adapts to your unique coping style.
                Voice & text chat, emotion detection, and personalized support.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Personal Companion", key="select_personal", use_container_width=True):
            st.session_state.mode = "personal"
            st.rerun()
    
    with col2:
        business_selected = st.session_state.mode == "business"
        st.markdown(f"""
        <div class="mode-card {'selected' if business_selected else ''}">
            <div class="mode-icon">💼</div>
            <div class="mode-title">Business Buddy</div>
            <div class="mode-desc">
                Deep sentiment analysis for customer feedback, reviews, and social media.
                Viral detection, crisis radar, and actionable insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Business Buddy", key="select_business", use_container_width=True):
            st.session_state.mode = "business"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Continue button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True, 
                     disabled=st.session_state.mode is None):
            st.session_state.stage = 2
            st.rerun()
    
    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.stage = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# STAGE 2: AGE + GOAL INPUT
# ============================================================

def render_age_goal_input():
    """Render age and goal input screen"""
    render_progress_bar(2, STAGE_NAMES)
    
    st.markdown('<div class="stage-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFFFFF; font-size: 2rem; margin-bottom: 0.5rem;">Tell us about yourself</h1>
        <p style="color: #9CA3AF; font-size: 1.1rem;">This helps us personalize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Age input
    st.markdown("""
    <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.5rem;">Your Age</div>
    """, unsafe_allow_html=True)
    
    age = st.slider(
        "Age",
        min_value=13,
        max_value=100,
        value=st.session_state.user_age,
        label_visibility="collapsed"
    )
    st.session_state.user_age = age
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Goal selection based on mode
    st.markdown("""
    <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.5rem;">Primary Goal</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.mode == "personal":
        goals = [
            "Manage stress and anxiety",
            "Process difficult emotions",
            "Build emotional awareness",
            "Find daily encouragement",
            "Work through life transitions",
            "General emotional support"
        ]
    else:
        goals = [
            "Understand customer sentiment",
            "Identify product issues",
            "Monitor brand perception",
            "Detect crisis signals early",
            "Improve customer experience",
            "Track competitor sentiment"
        ]
    
    goal = st.selectbox(
        "Goal",
        options=goals,
        index=goals.index(st.session_state.user_goal) if st.session_state.user_goal in goals else 0,
        label_visibility="collapsed"
    )
    st.session_state.user_goal = goal
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →", type="primary", use_container_width=True):
            st.session_state.stage = 3
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.stage = 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# STAGE 3: COPE QUESTIONNAIRE
# ============================================================

def render_cope_questionnaire():
    """Render Brief COPE questionnaire"""
    render_progress_bar(3, STAGE_NAMES)
    
    st.markdown('<div class="stage-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="color: #FFFFFF; font-size: 2rem; margin-bottom: 0.5rem;">Coping Style Assessment</h1>
        <p style="color: #9CA3AF; font-size: 1rem; max-width: 600px; margin: 0 auto;">
            These questions help us understand how you typically handle stress and challenges.
            Think about what you generally do when facing difficulties.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress through questions
    questions_answered = len(st.session_state.cope_answers)
    total_questions = len(COPE_QUESTIONS)
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span style="color: #8B5CF6; font-weight: 600;">{questions_answered}</span>
        <span style="color: #6B7280;"> / {total_questions} questions answered</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Response options as short labels
    option_labels = {
        1: "Not at all",
        2: "A little",
        3: "Medium amount",
        4: "A lot"
    }
    
    # Render questions in groups
    questions_per_page = 7
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    
    if "cope_page" not in st.session_state:
        st.session_state.cope_page = 0
    
    current_page = st.session_state.cope_page
    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_questions)
    
    # Page indicator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem; color: #6B7280; font-size: 0.85rem;">
        Page {current_page + 1} of {total_pages}
    </div>
    """, unsafe_allow_html=True)
    
    # Render current page questions
    for i in range(start_idx, end_idx):
        q = COPE_QUESTIONS[i]
        qid = q["id"]
        
        st.markdown(f"""
        <div class="question-card">
            <div class="question-number">Question {i + 1}</div>
            <div class="question-text">{q['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current answer
        current_answer = st.session_state.cope_answers.get(qid, None)
        options = list(option_labels.values())
        
        answer = st.radio(
            f"q_{qid}",
            options=options,
            index=options.index(option_labels[current_answer]) if current_answer else None,
            horizontal=True,
            label_visibility="collapsed",
            key=f"cope_q_{qid}"
        )
        
        # Store answer
        if answer:
            # Convert label back to score
            score = [k for k, v in option_labels.items() if v == answer][0]
            st.session_state.cope_answers[qid] = score
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if current_page > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.cope_page -= 1
                st.rerun()
    
    with col2:
        # Check if all questions on current page are answered
        current_page_questions = [COPE_QUESTIONS[i]["id"] for i in range(start_idx, end_idx)]
        all_current_answered = all(qid in st.session_state.cope_answers for qid in current_page_questions)
        
        if current_page < total_pages - 1:
            if st.button("Next →", type="primary", use_container_width=True, disabled=not all_current_answered):
                st.session_state.cope_page += 1
                st.rerun()
        else:
            # Final page - submit button
            all_answered = len(st.session_state.cope_answers) == total_questions
            if st.button("Complete Assessment ✓", type="primary", use_container_width=True, disabled=not all_answered):
                # Compute scores and assign persona
                scores = compute_cope_scores(st.session_state.cope_answers, COPE_QUESTIONS)
                st.session_state.cope_scores = scores
                
                persona_name, persona_info = assign_persona(scores)
                st.session_state.persona = persona_name
                st.session_state.persona_info = persona_info
                
                st.session_state.stage = 4
                st.rerun()
    
    with col3:
        if st.button("← Back to Start", use_container_width=True):
            st.session_state.stage = 2
            st.session_state.cope_page = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# STAGE 4: PERSONA SUMMARY
# ============================================================

def render_persona_summary():
    """Render persona assignment summary"""
    render_progress_bar(4, STAGE_NAMES)
    
    st.markdown('<div class="stage-container">', unsafe_allow_html=True)
    
    persona = st.session_state.persona
    persona_info = st.session_state.persona_info or {}
    persona_meta = get_persona_metadata(persona)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFFFFF; font-size: 2rem; margin-bottom: 0.5rem;">Your EmoSense Persona</h1>
        <p style="color: #9CA3AF; font-size: 1rem;">Based on your coping style assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Persona card
    st.markdown(f"""
    <div class="persona-card">
        <div class="persona-emoji">{persona_meta.get('emoji', '💜')}</div>
        <div class="persona-name">{persona}</div>
        <div class="persona-therapy">{persona_meta.get('therapy_style', 'Supportive Therapy')}</div>
        <div class="persona-description">
            {persona_info.get('description', persona_meta.get('short_desc', 'A personalized emotional support companion'))}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Traits
    traits = persona_info.get('traits', [])
    if traits:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.75rem;">Your Coping Traits</div>
        </div>
        """, unsafe_allow_html=True)
        
        trait_cols = st.columns(len(traits))
        for col, trait in zip(trait_cols, traits):
            with col:
                st.markdown(f"""
                <div style="background: rgba(138, 92, 246, 0.15); border: 1px solid rgba(138, 92, 246, 0.3);
                            border-radius: 8px; padding: 0.75rem; text-align: center;">
                    <span style="color: #C4B5FD; font-size: 0.9rem;">{trait}</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Continue button based on mode
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.mode == "personal":
            if st.button("💬 Start Personal Chat", type="primary", use_container_width=True):
                st.session_state.stage = 5
                st.rerun()
        else:
            if st.button("📊 Go to Business Buddy", type="primary", use_container_width=True):
                st.session_state.stage = 6
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Retake Assessment", use_container_width=True):
            st.session_state.cope_answers = {}
            st.session_state.cope_page = 0
            st.session_state.stage = 3
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# STAGE 5: PERSONAL CHATBOT
# ============================================================

def render_chat_interface():
    """Render personal companion chat interface"""
    persona = st.session_state.persona or "Gentle Sensitive"
    persona_meta = get_persona_metadata(persona)
    
    # Header
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; 
                padding: 1rem 1.5rem; background: rgba(17, 24, 39, 0.6); 
                border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid rgba(138, 92, 246, 0.2);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">{persona_meta.get('emoji', '💜')}</span>
            <div>
                <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">{persona}</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">{persona_meta.get('therapy_style', 'Your companion')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    if not st.session_state.chat_history:
        # Welcome message
        st.markdown(f"""
        <div class="message-bot">
            Hi there! I'm your {persona} companion. {persona_meta.get('short_desc', '')} 
            How are you feeling today?
        </div>
        <div class="clearfix"></div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="message-user">{format_markdown_to_html(msg['content'])}</div>
                <div class="clearfix"></div>
                """, unsafe_allow_html=True)
                if msg.get("emotion"):
                    emoji = EMOJI_MAP.get(msg["emotion"], "🎭")
                    st.markdown(f"""
                    <div style="text-align: right; margin-bottom: 0.5rem;">
                        <span class="emotion-chip">{emoji} {msg['emotion'].capitalize()}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-bot">{format_markdown_to_html(msg['content'])}</div>
                <div class="clearfix"></div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-play TTS if pending
    if st.session_state.pending_tts_audio:
        st.audio(st.session_state.pending_tts_audio, format="audio/mp3", autoplay=True)
        st.session_state.pending_tts_audio = None
    
    # Input area
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="personal_chat_input"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    # Voice input
    if VOICE_AVAILABLE:
        st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
        audio_bytes = st.audio_input("🎤 Or record a voice message", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        audio_bytes = None
    
    # Process text input
    if send_button and user_input.strip():
        process_chat_message(user_input.strip())
        st.rerun()
    
    # Process voice input
    if audio_bytes and VOICE_AVAILABLE:
        audio_hash = hashlib.md5(audio_bytes.getvalue()).hexdigest()
        
        if audio_hash != st.session_state.last_audio_hash:
            st.session_state.last_audio_hash = audio_hash
            
            voice_service = get_voice_chat_service()
            if voice_service:
                with st.spinner("Processing voice..."):
                    try:
                        # Transcribe
                        user_text = voice_service.speech_to_text(audio_bytes.getvalue())
                        
                        if user_text:
                            # Process message and get TTS
                            bot_response = process_chat_message(user_text, return_response=True)
                            
                            # Generate TTS
                            tts_audio = voice_service.text_to_speech(bot_response)
                            st.session_state.pending_tts_audio = tts_audio
                            
                            st.rerun()
                    except Exception as e:
                        st.error(f"Voice processing error: {str(e)}")
    
    # Restart button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Restart Journey", use_container_width=True):
            reset_journey()


def process_chat_message(user_text: str, return_response: bool = False) -> Optional[str]:
    """Process a chat message and generate response"""
    # Detect emotion
    emotion, confidence = get_dominant_emotion(user_text)
    
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_text,
        "emotion": emotion,
        "confidence": confidence
    })
    
    # Generate persona-based response
    engine = get_persona_engine()
    
    if engine:
        bot_response = engine.generate_persona_response(
            user_message=user_text,
            persona=st.session_state.persona,
            chat_history=st.session_state.chat_history[:-1],  # Exclude current message
            emotion_context=emotion
        )
    else:
        # Fallback response
        bot_response = f"I hear you. It sounds like you're feeling {emotion}. I'm here to support you. Tell me more about what's on your mind."
    
    # Add bot response to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_response
    })
    
    # Keep only last 20 messages
    if len(st.session_state.chat_history) > 20:
        st.session_state.chat_history = st.session_state.chat_history[-20:]
    
    if return_response:
        return bot_response
    return None


# ============================================================
# STAGE 6: BUSINESS BUDDY
# ============================================================

def render_business_buddy():
    """Render Business Buddy dashboard"""
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; 
                padding: 1rem 1.5rem; background: rgba(17, 24, 39, 0.6); 
                border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid rgba(138, 92, 246, 0.2);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">💼</span>
            <div>
                <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Business Buddy</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">Your brand therapist</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    tab1, tab2 = st.tabs(["📝 Text Input", "📄 CSV Upload"])
    
    with tab1:
        st.markdown("""
        <div style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 0.5rem;">
            Paste customer comments, reviews, or feedback (one per line)
        </div>
        """, unsafe_allow_html=True)
        
        text_input = st.text_area(
            "Comments",
            height=150,
            placeholder="Enter customer comments here, one per line...\n\nExample:\nI love this product, it works great!\nTerrible customer service, waited 2 hours\nThe new feature is confusing",
            label_visibility="collapsed"
        )
        
        if st.button("Analyze Comments", type="primary"):
            if text_input.strip():
                comments = [c.strip() for c in text_input.strip().split('\n') if c.strip()]
                if comments:
                    st.session_state.business_comments = comments
                    run_business_analysis(comments)
    
    with tab2:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head(), use_container_width=True)
                
                # Auto-detect comment column
                text_cols = [col for col in df.columns if df[col].dtype == 'object']
                
                if text_cols:
                    selected_col = st.selectbox("Select comment column", text_cols)
                    
                    if st.button("Analyze CSV", type="primary"):
                        comments = df[selected_col].dropna().astype(str).tolist()
                        if comments:
                            st.session_state.business_comments = comments[:500]  # Limit to 500
                            run_business_analysis(comments[:500])
            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")
    
    # Display analysis results
    if st.session_state.analysis_complete:
        render_business_results()
    
    # Business chat section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;">
        💬 Ask About Your Analysis
    </div>
    """, unsafe_allow_html=True)
    
    business_input = st.text_input(
        "Question",
        placeholder="Ask a question about the analysis...",
        label_visibility="collapsed",
        key="business_chat_input"
    )
    
    if st.button("Ask", key="business_ask"):
        if business_input.strip():
            process_business_question(business_input.strip())
            st.rerun()
    
    # Display business chat
    if st.session_state.business_chat_history:
        st.markdown('<div class="chat-container" style="max-height: 300px;">', unsafe_allow_html=True)
        for msg in st.session_state.business_chat_history[-10:]:
            if msg["role"] == "user":
                st.markdown(f'<div class="message-user">{msg["content"]}</div><div class="clearfix"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-bot">{format_markdown_to_html(msg["content"])}</div><div class="clearfix"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Restart button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Restart Journey", use_container_width=True, key="business_restart"):
            reset_journey()


def run_business_analysis(comments: List[str]):
    """Run emotion analysis on business comments"""
    with st.spinner("Analyzing emotions..."):
        all_emotions = {}
        emotion_counts = {e: 0 for e in EMOTIONS}
        
        for comment in comments:
            try:
                emotions, probs = predict_emotions(comment, threshold=0.3)
                for emotion, prob in probs.items():
                    all_emotions[emotion] = all_emotions.get(emotion, 0) + prob
                    if prob >= 0.3:
                        emotion_counts[emotion] += 1
            except:
                pass
        
        # Average emotions
        n = len(comments)
        avg_emotions = {e: all_emotions.get(e, 0) / n for e in EMOTIONS}
        
        st.session_state.business_emotions = avg_emotions
        
        # Simple summary
        dominant = max(avg_emotions.items(), key=lambda x: x[1])
        st.session_state.business_summary = f"Analyzed {n} comments. Dominant emotion: {dominant[0].capitalize()} ({dominant[1]*100:.1f}%)"
        
        st.session_state.analysis_complete = True


def render_business_results():
    """Render business analysis results"""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;">
        📊 Analysis Results
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    st.info(st.session_state.business_summary)
    
    # Emotion chart
    emotions = st.session_state.business_emotions
    if emotions:
        # Sort by score
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[e[0].capitalize() for e in sorted_emotions],
                y=[e[1] * 100 for e in sorted_emotions],
                marker_color='#8B5CF6'
            ))
            fig.update_layout(
                title="Top Emotions Detected",
                xaxis_title="Emotion",
                yaxis_title="Average Score (%)",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback display
            for emotion, score in sorted_emotions:
                emoji = EMOJI_MAP.get(emotion, "🎭")
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px;
                            background: rgba(138, 92, 246, 0.1); margin: 4px 0; border-radius: 8px;">
                    <span style="color: #FFFFFF;">{emoji} {emotion.capitalize()}</span>
                    <span style="color: #8B5CF6; font-weight: bold;">{score*100:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)


def process_business_question(question: str):
    """Process a business question"""
    # Add to history
    st.session_state.business_chat_history.append({
        "role": "user",
        "content": question
    })
    
    # Generate response based on analysis
    context = f"""
    Analysis summary: {st.session_state.business_summary}
    Number of comments analyzed: {len(st.session_state.business_comments)}
    """
    
    if st.session_state.business_emotions:
        top_emotions = sorted(st.session_state.business_emotions.items(), key=lambda x: x[1], reverse=True)[:5]
        context += f"\nTop emotions: {', '.join([f'{e[0]} ({e[1]*100:.1f}%)' for e in top_emotions])}"
    
    engine = get_persona_engine()
    
    if engine:
        # Use persona engine for business response
        response = engine.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are Business Buddy, an AI analyst for customer feedback.
                
Context from analysis:
{context}

Provide helpful, actionable insights based on the analysis. Be concise and professional."""},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=300
        ).choices[0].message.content
    else:
        response = f"Based on the analysis: {st.session_state.business_summary}. Please ensure OpenAI API key is configured for detailed insights."
    
    st.session_state.business_chat_history.append({
        "role": "assistant",
        "content": response
    })


# ============================================================
# STAGE NAMES FOR PROGRESS BAR
# ============================================================

STAGE_NAMES = {
    0: "Welcome",
    1: "Choose Your Path",
    2: "About You",
    3: "Coping Style Assessment",
    4: "Your Persona",
    5: "Personal Companion",
    6: "Business Buddy"
}


# ============================================================
# MAIN APP ROUTER
# ============================================================

def main():
    """Main app router based on stage"""
    stage = st.session_state.stage
    
    if stage == 0:
        render_welcome()
    elif stage == 1:
        render_mode_select()
    elif stage == 2:
        render_age_goal_input()
    elif stage == 3:
        render_cope_questionnaire()
    elif stage == 4:
        render_persona_summary()
    elif stage == 5:
        render_chat_interface()
    elif stage == 6:
        render_business_buddy()
    else:
        # Default to welcome
        st.session_state.stage = 0
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>EmoSense AI © 2024 | UFV University Project</p>
        <p style="font-size: 0.75rem; margin-top: 0.5rem;">
            Powered by BERT, GPT-4, and the Brief COPE assessment
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
