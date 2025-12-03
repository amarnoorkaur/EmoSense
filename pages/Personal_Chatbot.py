"""
Personal Emotion Companion - EmoSense AI
Continuous, context-aware, emotionally intelligent conversational agent
with Voice Chat support and optional COPE-based persona customization
Enhanced with Big Five personality adaptation (Mini-IPIP-20)
"""
import sys
import os
import hashlib

# Fix import path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, emotion_chip, spacer, page_header, card
from components.footer import render_footer
from services.personal_llm_service import get_personal_llm_service
from services.voice_chat_service import get_voice_chat_service
from services.cope_assessment_service import (
    COPE_QUESTIONS,
    RESPONSE_OPTIONS,
    PERSONA_INFO,
    compute_cope_scores,
    assign_persona
)
from services.persona_engine import get_persona_engine, get_persona_metadata
from services.big_five_service import (
    MINI_IPIP_QUESTIONS,
    RESPONSE_OPTIONS as BIG_FIVE_OPTIONS,
    TRAIT_INFO,
    score_mini_ipip,
    get_personality_summary,
    map_big_five_to_persona,
    get_recommended_personality
)
import datetime
from typing import Optional, Dict, List, Tuple

# Configure page
set_page_config()
inject_global_styles()

# Initialize LLM service
llm_service = get_personal_llm_service()

# Initialize Voice Chat service
voice_service = get_voice_chat_service()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

# Companion mode: "choice" -> "onboarding" -> "chat" OR "choice" -> "chat"
if "companion_mode" not in st.session_state:
    st.session_state.companion_mode = "choice"  # "choice", "onboarding", "big_five", "chat"

# Customization choice: None, "customized", "big_five", "general"
if "customization_choice" not in st.session_state:
    st.session_state.customization_choice = None

# Onboarding state (COPE)
if "onboarding_page" not in st.session_state:
    st.session_state.onboarding_page = 0

if "cope_answers" not in st.session_state:
    st.session_state.cope_answers = {}

if "cope_scores" not in st.session_state:
    st.session_state.cope_scores = {}

if "persona" not in st.session_state:
    st.session_state.persona = None

if "persona_info" not in st.session_state:
    st.session_state.persona_info = None

# Big Five personality state
if "big_five_page" not in st.session_state:
    st.session_state.big_five_page = 0

if "big_five_answers" not in st.session_state:
    st.session_state.big_five_answers = {}

if "big_five_scores" not in st.session_state:
    st.session_state.big_five_scores = None

if "big_five_summary" not in st.session_state:
    st.session_state.big_five_summary = None

# Initialize session state for conversation memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Last 10 messages

if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []  # Emotion analyses over time

if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "Casual Chat"

if "bot_personality" not in st.session_state:
    st.session_state.bot_personality = "Friendly"

if "last_emotion_data" not in st.session_state:
    st.session_state.last_emotion_data = None

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Voice chat session state
if "voice_chat_history" not in st.session_state:
    st.session_state.voice_chat_history = []

if "show_voice_emotion" not in st.session_state:
    st.session_state.show_voice_emotion = True

if "last_voice_audio" not in st.session_state:
    st.session_state.last_voice_audio = None

if "voice_processing" not in st.session_state:
    st.session_state.voice_processing = False

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

if "pending_tts_audio" not in st.session_state:
    st.session_state.pending_tts_audio = None

# Map persona to bot personality (from onboarding)
PERSONA_TO_PERSONALITY = {
    "Direct Professional": "Calm",
    "Gentle Sensitive": "Big Sister",
    "Reflective Companion": "Deep Thinker",
    "Energetic Companion": "Funny",
    "Motivational Guide": "Friendly"
}

# Apply persona if customization was completed
if st.session_state.persona and st.session_state.customization_choice == "customized":
    mapped_personality = PERSONA_TO_PERSONALITY.get(
        st.session_state.persona, 
        st.session_state.bot_personality
    )
    if st.session_state.bot_personality != mapped_personality:
        st.session_state.bot_personality = mapped_personality

# Custom CSS for chat interface
st.markdown("""
<style>
/* Remove top spacing */
.page-wrapper {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.gradient-hero {
    margin-top: 0 !important;
}

.header-container {
    margin-bottom: 0 !important;
}

/* Chat container */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    background: rgba(17, 24, 39, 0.3);
    border-radius: 12px;
    margin-bottom: 1rem;
}

/* User message (right side) */
.message-user-chat {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.875rem 1.25rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.5rem 0 0.5rem auto;
    max-width: 75%;
    width: fit-content;
    float: right;
    clear: both;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    animation: slideInRight 0.3s ease-out;
}

/* Bot message (left side) */
.message-bot-chat {
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
    animation: slideInLeft 0.3s ease-out;
}

/* Emotion chips in chat */
.emotion-chip-inline {
    display: inline-block;
    background: rgba(138, 92, 246, 0.2);
    border: 1px solid rgba(138, 92, 246, 0.4);
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    margin: 0.25rem;
    color: #C4B5FD;
}

/* Timestamp */
.timestamp {
    font-size: 0.7rem;
    color: #9CA3AF;
    margin: 0.25rem 0 1rem 0;
    clear: both;
}

.timestamp-user {
    text-align: right;
}

.timestamp-bot {
    text-align: left;
}

/* Mode badges */
.mode-badge {
    display: inline-block;
    background: rgba(138, 92, 246, 0.2);
    border: 1px solid rgba(138, 92, 246, 0.4);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    color: #C4B5FD;
    margin-right: 0.5rem;
}

/* Animations */
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Scrollbar styling */
.chat-container::-webkit-scrollbar {
    width: 6px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(17, 24, 39, 0.3);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: rgba(138, 92, 246, 0.5);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: rgba(138, 92, 246, 0.7);
}

/* Voice Chat Styles */
.voice-chat-container {
    background: rgba(17, 24, 39, 0.4);
    border: 1px solid rgba(138, 92, 246, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.voice-message {
    padding: 1rem;
    border-radius: 12px;
    margin: 0.75rem 0;
    animation: fadeIn 0.3s ease-out;
}

.voice-message-user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 15%;
    border-bottom-right-radius: 4px;
}

.voice-message-bot {
    background: rgba(138, 92, 246, 0.15);
    border: 1px solid rgba(138, 92, 246, 0.3);
    color: #E5E7EB;
    margin-right: 15%;
    border-bottom-left-radius: 4px;
}

.voice-emotion-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #6EE7B7;
    margin: 0.5rem 0;
}

.voice-role-label {
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    opacity: 0.8;
}

.voice-content {
    font-size: 0.95rem;
    line-height: 1.5;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.voice-recording-hint {
    background: rgba(234, 179, 8, 0.1);
    border: 1px solid rgba(234, 179, 8, 0.3);
    color: #FCD34D;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


def detect_emotion_for_voice(text: str) -> Tuple[str, float]:
    """
    Detect dominant emotion from text for voice chat pipeline
    
    Args:
        text: User's transcribed text
        
    Returns:
        Tuple of (dominant_emotion, confidence_score)
    """
    try:
        predicted_emotions, probabilities = predict_emotions(text, threshold=0.3)
        
        if predicted_emotions and probabilities:
            # Get the dominant emotion (highest probability)
            dominant = predicted_emotions[0]
            confidence = probabilities.get(dominant, 0.5)
            return dominant, confidence
        else:
            return "neutral", 0.5
    except Exception as e:
        return "neutral", 0.5


def render_voice_chat_history():
    """Render voice conversation history as a clean timeline"""
    if not st.session_state.voice_chat_history:
        st.markdown("""
        <div class="premium-card fade-in" style="text-align: center; padding: 2.5rem;">
            <div style="font-size: 2.4rem; margin-bottom: 0.5rem;">🎙️</div>
            <h3 style="color: #E5E7EB; margin: 0 0 0.5rem;">Start a voice conversation</h3>
            <p style="margin: 0; color: #A8A9B3;">Record your voice below and I'll respond with speech.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown('<div class="voice-chat-container">', unsafe_allow_html=True)
    
    for i, msg in enumerate(st.session_state.voice_chat_history):
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            emotion_html = ""
            if st.session_state.show_voice_emotion and "emotion" in msg:
                emotion = msg.get("emotion", "")
                confidence = msg.get("confidence", 0)
                emoji = EMOJI_MAP.get(emotion.lower(), "💬")
                emotion_html = f'<div class="voice-emotion-badge">{emoji} {emotion.capitalize()} ({confidence:.0%})</div>'
            
            st.markdown(f"""
            <div class="voice-message voice-message-user">
                <div class="voice-role-label">🗣️ You said:</div>
                <div class="voice-content">{content}</div>
                {emotion_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="voice-message voice-message-bot">
                <div class="voice-role-label">💜 EmoSense:</div>
                <div class="voice-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show audio player for bot responses
            if "audio" in msg and msg["audio"]:
                st.audio(msg["audio"], format="audio/mp3")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_chat_history():
    """Render the conversation history as chat bubbles"""
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="premium-card fade-in" style="text-align: center; padding: 2.5rem;">
            <div style="font-size: 2.4rem; margin-bottom: 0.5rem;">??</div>
            <h3 style="color: #E5E7EB; margin: 0 0 0.5rem;">Start a conversation</h3>
            <p style="margin: 0; color: #A8A9B3;">Type anything below and I will respond with empathy.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown('<div class="premium-card"><div class="chat-shell">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg.get("timestamp", "")
        bubble_class = "chat-bubble chat-user" if role == "user" else "chat-bubble chat-ai"
        st.markdown(f'<div class="{bubble_class}">{content}</div><div class="chat-meta">{timestamp}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


def should_analyze_emotions(user_message: str, mode: str) -> bool:
    """
    Determine if emotion analysis should run
    Only runs when:
    - User is in "Help Me Reflect" mode
    - Distress keywords are detected
    - User explicitly requests analysis
    """
    if mode == "Help Me Reflect":
        return True
    
    if llm_service and llm_service.detect_distress(user_message):
        return True
    
    # Check for explicit analysis requests
    message_lower = user_message.lower()
    analysis_triggers = ["how am i feeling", "what emotions", "analyze", "what's my mood"]
    if any(trigger in message_lower for trigger in analysis_triggers):
        return True
    
    return False


def handle_user_message(user_message: str):
    """Process user message and generate response"""
    
    if not user_message.strip():
        return
    
    # Get current settings
    mode = st.session_state.conversation_mode
    personality = st.session_state.bot_personality
    
    # Check for crisis situation first
    if llm_service and llm_service.is_crisis_situation(user_message):
        # Immediate grounding response
        crisis_response = llm_service.get_crisis_response()
        
        # Add to chat history
        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": timestamp
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": crisis_response,
            "timestamp": timestamp
        })
        
        # Keep last 10 conversations
        st.session_state.chat_history = st.session_state.chat_history[-20:]
        
        return
    
    # Determine if emotion analysis needed
    run_emotion_analysis = should_analyze_emotions(user_message, mode)
    
    emotion_context = None
    if run_emotion_analysis:
        # Run BERT emotion detection
        predicted_emotions, probabilities = predict_emotions(user_message, threshold=0.3)
        
        emotion_context = {
            "emotions": predicted_emotions,
            "probabilities": probabilities
        }
        
        # Store in emotion history
        st.session_state.emotion_history.append({
            "timestamp": datetime.datetime.now(),
            "emotions": predicted_emotions,
            "probabilities": probabilities,
            "message": user_message
        })
        
        # Keep last 10 emotion analyses
        st.session_state.emotion_history = st.session_state.emotion_history[-10:]
        
        st.session_state.last_emotion_data = emotion_context
    
    # Detect emotional trend
    emotion_trend = None
    if llm_service and len(st.session_state.emotion_history) >= 3:
        emotion_trend = llm_service.detect_emotional_trend(st.session_state.emotion_history)
    
    # Generate LLM response
    timestamp = datetime.datetime.now().strftime("%I:%M %p")
    
    if not llm_service:
        response = "I need an OpenAI API key to chat with you. Please configure OPENAI_API_KEY in your environment or Streamlit secrets. 🔑"
    else:
        # Generate natural conversational response with all 4 adaptation layers
        response = llm_service.generate_response(
            user_message=user_message,
            chat_history=st.session_state.chat_history,
            mode=mode,
            personality=personality,
            emotion_context=emotion_context,
            emotion_trend=emotion_trend,
            persona=st.session_state.persona,
            big_five_scores=st.session_state.big_five_scores  # Pass Big Five if available
        )
    
    # Add to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message,
        "timestamp": timestamp,
        "emotion_data": emotion_context
    })
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": timestamp
    })
    
    # Keep last 20 messages (10 exchanges)
    st.session_state.chat_history = st.session_state.chat_history[-20:]


# ============================================================
# RENDER FUNCTIONS FOR EACH MODE
# ============================================================

def render_choice_screen():
    """Render the initial choice between full personalization or general bot"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFFFFF; font-size: 1.75rem; margin-bottom: 0.5rem;">Welcome to EmoSense Companion</h2>
        <p style="color: #9CA3AF; font-size: 1rem;">How would you like to experience your AI companion?</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
                    border: 2px solid rgba(139, 92, 246, 0.4); border-radius: 20px; padding: 2rem; text-align: center;
                    min-height: 320px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🧠 + 🎭</div>
            <div style="color: #FFFFFF; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem;">Full Personalization</div>
            <div style="color: #C4B5FD; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">
                Complete both assessments for the most personalized experience:
            </div>
            <div style="text-align: left; padding: 0 1rem;">
                <div style="color: #93C5FD; font-size: 0.85rem; margin-bottom: 0.5rem;">
                    <strong>Step 1:</strong> 🧠 Big Five Personality (20 questions)
                </div>
                <div style="color: #C4B5FD; font-size: 0.85rem; margin-bottom: 0.75rem;">
                    <strong>Step 2:</strong> 🎭 COPE Coping Style (28 questions)
                </div>
            </div>
            <div style="color: #6B7280; font-size: 0.8rem;">
                ⏱️ Total: 5-8 minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Start Full Personalization", type="primary", use_container_width=True, key="choose_full"):
            st.session_state.customization_choice = "full"
            st.session_state.companion_mode = "big_five"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: rgba(17, 24, 39, 0.6); border: 2px solid rgba(107, 114, 128, 0.4);
                    border-radius: 20px; padding: 2rem; text-align: center; min-height: 320px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">💬</div>
            <div style="color: #FFFFFF; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem;">General Chat</div>
            <div style="color: #9CA3AF; font-size: 0.9rem; line-height: 1.6; margin-bottom: 1rem;">
                Start chatting right away with our friendly AI companion. 
                You can manually choose personality and conversation mode.
            </div>
            <div style="color: #6B7280; font-size: 0.8rem; margin-top: 2rem;">
                ⚡ Start immediately
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 Skip to Chat", use_container_width=True, key="choose_general"):
            st.session_state.customization_choice = "general"
            st.session_state.companion_mode = "chat"
            st.rerun()


def render_big_five_assessment():
    """Render the Big Five (Mini-IPIP-20) personality assessment"""
    total_questions = len(MINI_IPIP_QUESTIONS)
    questions_answered = len(st.session_state.big_five_answers)
    
    # Progress bar
    progress = questions_answered / total_questions
    st.markdown(f"""
    <div style="background: rgba(17, 24, 39, 0.6); border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;
                border: 1px solid rgba(59, 130, 246, 0.3);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #93C5FD; font-weight: 600;">🧠 Personality Assessment (Big Five)</span>
            <span style="color: #9CA3AF;">{questions_answered} / {total_questions}</span>
        </div>
        <div style="background: rgba(59, 130, 246, 0.2); border-radius: 8px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
                        height: 100%; width: {progress * 100}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Response options for Big Five (1-5 Likert scale)
    option_labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    
    # Show 5 questions per page
    questions_per_page = 5
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.big_five_page
    
    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_questions)
    
    st.markdown(f"""
    <div style="color: #9CA3AF; font-size: 0.85rem; margin-bottom: 1rem; text-align: center;">
        Rate how well each statement describes you.
    </div>
    """, unsafe_allow_html=True)
    
    # Render current page questions
    for i in range(start_idx, end_idx):
        q = MINI_IPIP_QUESTIONS[i]
        qid = q["id"]
        trait = q["trait"]
        trait_info = TRAIT_INFO[trait]
        
        st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(59, 130, 246, 0.15);
                    border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1rem;">{trait_info['emoji']}</span>
                <span style="color: {trait_info['color']}; font-size: 0.75rem; font-weight: 600;">
                    {trait_info['name']}
                </span>
                <span style="color: #6B7280; font-size: 0.75rem;">• Q{i + 1}</span>
            </div>
            <div style="color: #E5E7EB; font-size: 0.95rem; line-height: 1.5;">
                {q['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        current_answer = st.session_state.big_five_answers.get(qid)
        current_index = current_answer - 1 if current_answer else None
        
        answer = st.radio(
            f"Answer for Q{i+1}",
            options=option_labels,
            index=current_index,
            horizontal=True,
            label_visibility="collapsed",
            key=f"big_five_{qid}"
        )
        
        if answer:
            score = option_labels.index(answer) + 1
            st.session_state.big_five_answers[qid] = score
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_page > 0:
            if st.button("← Previous", use_container_width=True, key="bf_prev"):
                st.session_state.big_five_page -= 1
                st.rerun()
    
    with col2:
        current_page_qids = [MINI_IPIP_QUESTIONS[i]["id"] for i in range(start_idx, end_idx)]
        all_current_answered = all(qid in st.session_state.big_five_answers for qid in current_page_qids)
        
        if current_page < total_pages - 1:
            if st.button("Next →", type="primary", use_container_width=True, disabled=not all_current_answered, key="bf_next"):
                st.session_state.big_five_page += 1
                st.rerun()
        else:
            # Final page - complete button (goes to COPE next)
            all_answered = len(st.session_state.big_five_answers) == total_questions
            if st.button("✓ Continue to Coping Style →", type="primary", use_container_width=True, disabled=not all_answered, key="bf_complete"):
                # Score the assessment
                scores = score_mini_ipip(st.session_state.big_five_answers)
                st.session_state.big_five_scores = scores
                st.session_state.big_five_summary = get_personality_summary(scores)
                
                # Map to persona and personality (will be refined by COPE)
                persona_name, _ = map_big_five_to_persona(scores)
                st.session_state.persona = persona_name
                
                recommended_personality = get_recommended_personality(scores)
                st.session_state.bot_personality = recommended_personality
                
                # Move to COPE assessment (Step 2)
                st.session_state.companion_mode = "onboarding"
                st.rerun()
    
    with col3:
        if st.button("Skip →", use_container_width=True, help="Skip to general chat", key="bf_skip"):
            st.session_state.customization_choice = "general"
            st.session_state.companion_mode = "chat"
            st.session_state.big_five_answers = {}
            st.session_state.big_five_page = 0
            st.rerun()


def render_big_five_results():
    """Show Big Five results before continuing to COPE"""
    scores = st.session_state.big_five_scores
    summary = st.session_state.big_five_summary
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h3 style="color: #FFFFFF; font-size: 1.5rem; margin-bottom: 0.5rem;">🧠 Your Personality Profile</h3>
        <p style="color: #9CA3AF; font-size: 0.9rem;">Step 1 Complete! Here's what we learned about you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display trait scores
    for trait_key in ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]:
        if trait_key in summary:
            info = summary[trait_key]
            score = info["score"]
            level = info["level"]
            emoji = info["emoji"]
            color = info["color"]
            desc = info["description"]
            
            # Calculate bar width (score 1-5 -> 20%-100%)
            bar_width = (score / 5) * 100
            
            st.markdown(f"""
            <div style="background: rgba(17, 24, 39, 0.5); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="color: #FFFFFF; font-weight: 600;">{emoji} {trait_key.capitalize()}</span>
                    <span style="color: {color}; font-weight: 600;">{score}/5 ({level.upper()})</span>
                </div>
                <div style="background: rgba(107, 114, 128, 0.3); border-radius: 8px; height: 8px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {bar_width}%;"></div>
                </div>
                <div style="color: #9CA3AF; font-size: 0.8rem; margin-top: 0.5rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Retake Assessment", use_container_width=True):
            st.session_state.big_five_answers = {}
            st.session_state.big_five_page = 0
            st.session_state.big_five_scores = None
            st.session_state.companion_mode = "big_five"
            st.rerun()
    
    with col2:
        if st.button("Continue to Coping Style →", type="primary", use_container_width=True):
            st.session_state.companion_mode = "onboarding"
            st.rerun()


def render_onboarding():
    """Render the COPE questionnaire onboarding flow"""
    total_questions = len(COPE_QUESTIONS)
    questions_answered = len(st.session_state.cope_answers)
    
    # Show step indicator if coming from Big Five
    if st.session_state.big_five_scores:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #10B981; color: white; width: 24px; height: 24px; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">✓</span>
                <span style="color: #10B981; font-size: 0.85rem;">Personality</span>
            </div>
            <div style="width: 40px; height: 2px; background: rgba(139, 92, 246, 0.5);"></div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: #8B5CF6; color: white; width: 24px; height: 24px; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">2</span>
                <span style="color: #C4B5FD; font-size: 0.85rem; font-weight: 600;">Coping Style</span>
            </div>
            <div style="width: 40px; height: 2px; background: rgba(107, 114, 128, 0.3);"></div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="background: rgba(107, 114, 128, 0.3); color: #6B7280; width: 24px; height: 24px; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; font-size: 0.75rem;">3</span>
                <span style="color: #6B7280; font-size: 0.85rem;">Chat</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    progress = questions_answered / total_questions
    st.markdown(f"""
    <div style="background: rgba(17, 24, 39, 0.6); border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;
                border: 1px solid rgba(138, 92, 246, 0.2);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #C4B5FD; font-weight: 600;">🎭 Coping Style Assessment (Step 2)</span>
            <span style="color: #9CA3AF;">{questions_answered} / {total_questions}</span>
        </div>
        <div style="background: rgba(138, 92, 246, 0.2); border-radius: 8px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #667EEA 0%, #8B5CF6 50%, #EC4899 100%);
                        height: 100%; width: {progress * 100}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Response options
    option_labels = ["Not at all", "A little bit", "Medium amount", "A lot"]
    
    # Show 4 questions per page
    questions_per_page = 4
    total_pages = (total_questions + questions_per_page - 1) // questions_per_page
    current_page = st.session_state.onboarding_page
    
    start_idx = current_page * questions_per_page
    end_idx = min(start_idx + questions_per_page, total_questions)
    
    st.markdown(f"""
    <div style="color: #9CA3AF; font-size: 0.85rem; margin-bottom: 1rem; text-align: center;">
        Think about how you typically handle stress and challenges.
    </div>
    """, unsafe_allow_html=True)
    
    # Render current page questions
    for i in range(start_idx, end_idx):
        q = COPE_QUESTIONS[i]
        qid = q["id"]
        
        st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.5); border: 1px solid rgba(138, 92, 246, 0.15);
                    border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
            <div style="color: #8B5CF6; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">
                Question {i + 1}
            </div>
            <div style="color: #E5E7EB; font-size: 0.95rem; line-height: 1.5;">
                {q['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        current_answer = st.session_state.cope_answers.get(qid)
        current_index = current_answer - 1 if current_answer else None
        
        answer = st.radio(
            f"Answer for Q{i+1}",
            options=option_labels,
            index=current_index,
            horizontal=True,
            label_visibility="collapsed",
            key=f"cope_{qid}"
        )
        
        if answer:
            score = option_labels.index(answer) + 1
            st.session_state.cope_answers[qid] = score
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_page > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.onboarding_page -= 1
                st.rerun()
    
    with col2:
        current_page_qids = [COPE_QUESTIONS[i]["id"] for i in range(start_idx, end_idx)]
        all_current_answered = all(qid in st.session_state.cope_answers for qid in current_page_qids)
        
        if current_page < total_pages - 1:
            if st.button("Next →", type="primary", use_container_width=True, disabled=not all_current_answered):
                st.session_state.onboarding_page += 1
                st.rerun()
        else:
            # Final page - complete button
            all_answered = len(st.session_state.cope_answers) == total_questions
            if st.button("✓ Complete & Start Chatting →", type="primary", use_container_width=True, disabled=not all_answered):
                # Compute scores and assign persona
                scores = compute_cope_scores(st.session_state.cope_answers, COPE_QUESTIONS)
                st.session_state.cope_scores = scores
                
                persona_name, persona_info = assign_persona(scores)
                st.session_state.persona = persona_name
                st.session_state.persona_info = persona_info
                
                # Apply personality mapping (COPE refines Big Five recommendation)
                mapped_personality = PERSONA_TO_PERSONALITY.get(persona_name, "Friendly")
                st.session_state.bot_personality = mapped_personality
                
                # Mark as fully customized
                st.session_state.customization_choice = "full"
                
                # Move to chat
                st.session_state.companion_mode = "chat"
                st.rerun()
    
    with col3:
        if st.button("Skip →", use_container_width=True, help="Skip to general chat"):
            st.session_state.customization_choice = "general"
            st.session_state.companion_mode = "chat"
            st.session_state.cope_answers = {}
            st.session_state.onboarding_page = 0
            st.rerun()


def render_persona_banner():
    """Show persona banner if customization was completed (Full, COPE, or Big Five only)"""
    
    # Full personalization banner (Big Five + COPE)
    if st.session_state.customization_choice == "full" and st.session_state.big_five_scores and st.session_state.cope_scores:
        scores = st.session_state.big_five_scores
        summary = st.session_state.big_five_summary or {}
        persona = st.session_state.persona
        persona_meta = get_persona_metadata(persona) if persona else {}
        
        # Create trait badges
        trait_badges = ""
        for trait_key in ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]:
            if trait_key in summary:
                info = summary[trait_key]
                level = info.get("level", "medium")
                emoji = info.get("emoji", "")
                level_label = "H" if level == "high" else ("L" if level == "low" else "M")
                color = info.get("color", "#8B5CF6")
                trait_badges += f'<span style="background: {color}22; color: {color}; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.65rem; margin-right: 0.2rem;">{emoji}{level_label}</span>'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(139, 92, 246, 0.15) 100%);
                    border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.75rem;">{persona_meta.get('emoji', '✨')}</span>
                <div style="flex: 1;">
                    <div style="color: #FFFFFF; font-weight: 600;">{persona or 'Fully Personalized Companion'}</div>
                    <div style="color: #9CA3AF; font-size: 0.8rem;">Based on your personality + coping style</div>
                </div>
                <div style="display: flex; gap: 0.25rem;">
                    <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 0.2rem 0.5rem;
                                border-radius: 8px; font-size: 0.7rem;">🧠</span>
                    <span style="background: rgba(139, 92, 246, 0.2); color: #C4B5FD; padding: 0.2rem 0.5rem;
                                border-radius: 8px; font-size: 0.7rem;">🎭</span>
                </div>
            </div>
            <div style="display: flex; gap: 0.2rem; flex-wrap: wrap;">
                {trait_badges}
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Big Five only personalization banner
    if st.session_state.customization_choice == "big_five" and st.session_state.big_five_scores:
        scores = st.session_state.big_five_scores
        summary = st.session_state.big_five_summary or {}
        persona = st.session_state.persona
        persona_meta = get_persona_metadata(persona) if persona else {}
        
        # Create trait badges
        trait_badges = ""
        for trait_key in ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]:
            if trait_key in summary:
                info = summary[trait_key]
                level = info.get("level", "medium")
                emoji = info.get("emoji", "")
                level_label = "H" if level == "high" else ("L" if level == "low" else "M")
                color = info.get("color", "#8B5CF6")
                trait_badges += f'<span style="background: {color}22; color: {color}; padding: 0.2rem 0.5rem; border-radius: 8px; font-size: 0.7rem; margin-right: 0.25rem;">{emoji} {level_label}</span>'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
                    border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.75rem;">{persona_meta.get('emoji', '🧠')}</span>
                <div>
                    <div style="color: #FFFFFF; font-weight: 600;">{persona or 'Adaptive Companion'}</div>
                    <div style="color: #9CA3AF; font-size: 0.8rem;">Based on your Big Five personality profile</div>
                </div>
                <div style="margin-left: auto;">
                    <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 0.25rem 0.75rem;
                                border-radius: 12px; font-size: 0.75rem;">🧠 Personality-Based</span>
                </div>
            </div>
            <div style="display: flex; gap: 0.25rem; flex-wrap: wrap;">
                {trait_badges}
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # COPE only personalization banner
    if st.session_state.customization_choice == "customized" and st.session_state.persona:
        persona = st.session_state.persona
        persona_meta = get_persona_metadata(persona)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
                    border: 1px solid rgba(138, 92, 246, 0.3); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;
                    display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 2rem;">{persona_meta.get('emoji', '💜')}</span>
            <div>
                <div style="color: #FFFFFF; font-weight: 600;">{persona}</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">{persona_meta.get('short_desc', '')}</div>
            </div>
            <div style="margin-left: auto;">
                <span style="background: rgba(16, 185, 129, 0.2); color: #6EE7B7; padding: 0.25rem 0.75rem;
                            border-radius: 12px; font-size: 0.75rem;">🎭 COPE-Based</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_chat_ui():
    """Render the main chat interface"""
    # Show persona banner if customized
    render_persona_banner()
    
    # Determine if personality is locked (Full, Big Five, or COPE customization)
    personality_locked = st.session_state.customization_choice in ["customized", "big_five", "full"]
    
    # Settings row - only show personality selector if NOT customized
    if not personality_locked:
        col_settings1, col_settings2 = st.columns(2)
        
        with col_settings1:
            mode = st.selectbox(
                "🎭 Conversation Mode",
                ["Casual Chat", "Comfort Me", "Help Me Reflect", "Hype Me Up", "Just Listen"],
                key="mode_selector"
            )
            st.session_state.conversation_mode = mode
        
        with col_settings2:
            personality = st.selectbox(
                "✨ Companion Personality",
                ["Friendly", "Calm", "Big Sister", "Funny", "Deep Thinker"],
                key="personality_selector"
            )
            st.session_state.bot_personality = personality
    else:
        # Just show mode selector for customized users
        mode = st.selectbox(
            "🎭 Conversation Mode",
            ["Casual Chat", "Comfort Me", "Help Me Reflect", "Hype Me Up", "Just Listen"],
            key="mode_selector"
        )
        st.session_state.conversation_mode = mode
    
    spacer("sm")
    
    # Display current mode
    mode_descriptions = {
        "Casual Chat": "💬 Natural, friendly conversation",
        "Comfort Me": "🤗 Gentle support and grounding",
        "Help Me Reflect": "🤔 Thoughtful exploration (auto emotion analysis)",
        "Hype Me Up": "🔥 Energizing cheerleader mode",
        "Just Listen": "👂 Minimal responses, maximum space"
    }
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 0.75rem 1.25rem; margin-bottom: 1rem;">
        <span class="mode-badge">{st.session_state.conversation_mode}</span>
        <span style="color: #9CA3AF; font-size: 0.875rem;">{mode_descriptions.get(st.session_state.conversation_mode, '')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Chat history display
    render_chat_history()
    
    spacer("md")
    
    # Input area with text and voice options
    col_input, col_mic, col_buttons = st.columns([3.5, 0.5, 1])
    
    with col_input:
        if "user_message_input" not in st.session_state:
            st.session_state.user_message_input = ""
        
        if st.session_state.clear_input:
            st.session_state.user_message_input = ""
            st.session_state.clear_input = False
        
        user_input = st.text_area(
            "Message",
            value=st.session_state.user_message_input,
            height=100,
            placeholder="Type or click 🎙️ to talk... I'm here to listen. 💜",
            label_visibility="collapsed",
            key="personal_chat_input_box"
        )
    
    with col_mic:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        audio_input = st.audio_input(
            "🎙️",
            key="inline_voice_input",
            label_visibility="collapsed"
        )
    
    with col_buttons:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        send_button = st.button("💬 Send", type="primary")
        
        if st.button("🔍 Analyze", help="Explicitly analyze emotions in your message"):
            if user_input.strip():
                with st.spinner("Understanding your emotions..."):
                    predicted_emotions, probabilities = predict_emotions(user_input, threshold=0.3)
                    
                    if llm_service:
                        reflection = llm_service.generate_emotion_reflection(
                            user_input,
                            predicted_emotions,
                            probabilities,
                            st.session_state.bot_personality
                        )
                    else:
                        if predicted_emotions:
                            emotion_list = ", ".join([f"{e.capitalize()}" for e in predicted_emotions[:3]])
                            reflection = f"I sense {emotion_list} in your words. These emotions are valid. 💜"
                        else:
                            reflection = "Your message feels emotionally balanced. 🌟"
                    
                    timestamp = datetime.datetime.now().strftime("%I:%M %p")
                    emotion_context = {"emotions": predicted_emotions, "probabilities": probabilities}
                    
                    st.session_state.chat_history.append({
                        "role": "user", "content": user_input, "timestamp": timestamp, "emotion_data": emotion_context
                    })
                    st.session_state.chat_history.append({
                        "role": "assistant", "content": reflection, "timestamp": timestamp
                    })
                    st.session_state.chat_history = st.session_state.chat_history[-20:]
                    
                    st.session_state.emotion_history.append({
                        "timestamp": datetime.datetime.now(), "emotions": predicted_emotions,
                        "probabilities": probabilities, "message": user_input
                    })
                    st.session_state.emotion_history = st.session_state.emotion_history[-10:]
                    
                    st.session_state.clear_input = True
                    st.rerun()
        
        if st.button("🗑️ Clear"):
            st.session_state.chat_history = []
            st.session_state.emotion_history = []
            st.session_state.last_emotion_data = None
            st.session_state.clear_input = True
            st.rerun()
    
    # Handle text send
    if send_button and user_input.strip():
        message_to_send = user_input
        st.session_state.user_message_input = ""
        st.session_state.clear_input = True
        
        with st.spinner("💭 Thinking..."):
            handle_user_message(message_to_send)
        st.rerun()
    
    # Handle voice input
    if audio_input is not None:
        audio_bytes = audio_input.read()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        if audio_hash != st.session_state.last_audio_hash and len(audio_bytes) > 0:
            st.session_state.last_audio_hash = audio_hash
            
            if voice_service:
                try:
                    with st.spinner("🎙️ Transcribing your voice..."):
                        user_text = voice_service.speech_to_text(audio_bytes)
                    
                    if user_text.strip():
                        st.success(f"📝 You said: \"{user_text}\"")
                        
                        with st.spinner("💭 Thinking..."):
                            handle_user_message(user_text)
                        
                        with st.spinner("🔊 Generating voice response..."):
                            if st.session_state.chat_history:
                                last_response = st.session_state.chat_history[-1]["content"]
                                tts_audio = voice_service.text_to_speech(last_response)
                                st.session_state.pending_tts_audio = tts_audio
                        
                        st.rerun()
                    else:
                        st.warning("🎙️ Couldn't understand the audio. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error processing voice: {str(e)}")
            else:
                st.error("🔑 Voice service unavailable. Please configure OPENAI_API_KEY.")
    
    # Auto-play TTS
    if st.session_state.pending_tts_audio is not None:
        st.audio(st.session_state.pending_tts_audio, format="audio/mp3", autoplay=True)
        st.session_state.pending_tts_audio = None
    
    spacer("md")
    
    # Reset option
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start Over (New Persona)", use_container_width=True):
            # Reset all onboarding state (COPE + Big Five)
            st.session_state.companion_mode = "choice"
            st.session_state.customization_choice = None
            # COPE reset
            st.session_state.cope_answers = {}
            st.session_state.cope_scores = {}
            st.session_state.persona = None
            st.session_state.persona_info = None
            st.session_state.onboarding_page = 0
            # Big Five reset
            st.session_state.big_five_answers = {}
            st.session_state.big_five_scores = None
            st.session_state.big_five_summary = None
            st.session_state.big_five_page = 0
            # Chat reset
            st.session_state.chat_history = []
            st.session_state.emotion_history = []
            st.session_state.bot_personality = "Friendly"
            st.rerun()
    
    # Safety reminder
    st.markdown("""
    <div style="background: rgba(138, 92, 246, 0.1); border-left: 3px solid #8A5CF6; padding: 1rem; border-radius: 8px; margin-top: 2rem;">
        <p style="color: #A8A9B3; font-size: 0.875rem; margin: 0;">
            <strong style="color: #FFFFFF;">💜 Remember:</strong> EmoSense Companion is an AI tool for emotional support and reflection, 
            not a replacement for professional mental health care. If you're in crisis, please reach out to a mental health 
            professional or crisis hotline immediately.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN UI LAYOUT - STATE MACHINE ROUTER
# ============================================================

with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "💜 EmoSense Companion",
        "Your emotionally intelligent AI friend. Type or talk — I'll understand."
    )
    
    # Route based on companion mode
    if st.session_state.companion_mode == "choice":
        render_choice_screen()
    elif st.session_state.companion_mode == "big_five":
        render_big_five_assessment()
    elif st.session_state.companion_mode == "onboarding":
        render_onboarding()
    elif st.session_state.companion_mode == "chat":
        render_chat_ui()
    else:
        # Default to choice
        st.session_state.companion_mode = "choice"
        st.rerun()
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
