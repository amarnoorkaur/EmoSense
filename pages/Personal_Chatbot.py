"""
Personal Emotion Companion - EmoSense AI
Continuous, context-aware, emotionally intelligent conversational agent
"""
import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, emotion_chip, spacer, page_header, card, render_header
from components.footer import render_footer
from services.personal_llm_service import get_personal_llm_service
import datetime
from typing import Optional, Dict, List

# Configure page
set_page_config()
inject_global_styles()
render_header()

# Initialize LLM service
llm_service = get_personal_llm_service()

# Initialize session state for conversation memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Last 10 messages

if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []  # Emotion analyses over time

if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = "Casual Chat"

if "bot_personality" not in st.session_state:
    st.session_state.bot_personality = "Friendly"

if "show_emotion_analysis" not in st.session_state:
    st.session_state.show_emotion_analysis = False

if "last_emotion_data" not in st.session_state:
    st.session_state.last_emotion_data = None

if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

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
</style>
""", unsafe_allow_html=True)


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
        # Generate natural conversational response
        response = llm_service.generate_response(
            user_message=user_message,
            chat_history=st.session_state.chat_history,
            mode=mode,
            personality=personality,
            emotion_context=emotion_context,
            emotion_trend=emotion_trend
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


# Main UI Layout
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "💜 EmoSense Companion",
        "Your emotionally intelligent AI friend. Just chat naturally — I'll understand."
    )
    
    # Settings row
    col_settings1, col_settings2, col_settings3 = st.columns([2, 2, 1])
    
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
    
    with col_settings3:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        show_emotions = st.checkbox("Show emotions", value=st.session_state.show_emotion_analysis)
        st.session_state.show_emotion_analysis = show_emotions
    
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
        <span class="mode-badge">{mode}</span>
        <span style="color: #9CA3AF; font-size: 0.875rem;">{mode_descriptions.get(mode, '')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Chat history display
    render_chat_history()
    
    spacer("md")
    
    # Input area
    col_input, col_buttons = st.columns([4, 1])
    
    with col_input:
        # Clear input after message is sent
        default_value = "" if st.session_state.clear_input else st.session_state.get("user_message_input", "")
        
        user_input = st.text_area(
            "Message",
            value=default_value,
            height=100,
            placeholder="Just type naturally... I'm here to listen. 💜",
            label_visibility="collapsed",
            key="user_message_input"
        )
        
        # Reset the clear flag
        if st.session_state.clear_input:
            st.session_state.clear_input = False
    
    with col_buttons:
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        send_button = st.button("💬 Send", type="primary", use_container_width=True)
        
        if st.button("🔍 Analyze", use_container_width=True, help="Explicitly analyze emotions in your message"):
            if user_input.strip():
                # Force emotion analysis
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
                    
                    # Add to history
                    timestamp = datetime.datetime.now().strftime("%I:%M %p")
                    emotion_context = {
                        "emotions": predicted_emotions,
                        "probabilities": probabilities
                    }
                    
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_input,
                        "timestamp": timestamp,
                        "emotion_data": emotion_context
                    })
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": reflection,
                        "timestamp": timestamp
                    })
                    
                    st.session_state.chat_history = st.session_state.chat_history[-20:]
                    
                    # Store emotion data
                    st.session_state.emotion_history.append({
                        "timestamp": datetime.datetime.now(),
                        "emotions": predicted_emotions,
                        "probabilities": probabilities,
                        "message": user_input
                    })
                    st.session_state.emotion_history = st.session_state.emotion_history[-10:]
                    
                    # Clear input box
                    st.session_state.clear_input = True
                    st.rerun()
        
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.emotion_history = []
            st.session_state.last_emotion_data = None
            st.session_state.clear_input = True
            st.rerun()
    
    # Handle send button
    if send_button and user_input.strip():
        with st.spinner("💭 Thinking..."):
            handle_user_message(user_input)
        st.session_state.clear_input = True
        st.rerun()
    
    spacer("md")
    
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
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
