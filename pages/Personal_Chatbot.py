"""
Personal Emotion Companion - EmoSense AI
Continuous, context-aware, emotionally intelligent conversational agent
with Voice Chat support
"""
import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, emotion_chip, spacer, page_header, card
from components.footer import render_footer
from services.personal_llm_service import get_personal_llm_service
from services.voice_chat_service import get_voice_chat_service
import datetime
from typing import Optional, Dict, List, Tuple

# Configure page
set_page_config()
inject_global_styles()

# Initialize LLM service
llm_service = get_personal_llm_service()

# Initialize Voice Chat service
voice_service = get_voice_chat_service()

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

# Voice chat session state
if "voice_chat_history" not in st.session_state:
    st.session_state.voice_chat_history = []

if "show_voice_emotion" not in st.session_state:
    st.session_state.show_voice_emotion = True

if "last_voice_audio" not in st.session_state:
    st.session_state.last_voice_audio = None

if "voice_processing" not in st.session_state:
    st.session_state.voice_processing = False

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
        "Your emotionally intelligent AI friend. Chat naturally or talk to me — I'll understand."
    )
    
    # Create tabs for Text Chat and Voice Chat
    tab_text, tab_voice = st.tabs(["💬 Text Chat", "🎧 Voice Companion"])
    
    # ==================== TEXT CHAT TAB ====================
    with tab_text:
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
            if "user_message_input" not in st.session_state:
                st.session_state.user_message_input = ""
            
            if st.session_state.clear_input:
                st.session_state.user_message_input = ""
                st.session_state.clear_input = False
            
            user_input = st.text_area(
                "Message",
                value=st.session_state.user_message_input,
                height=100,
                placeholder="Just type naturally... I'm here to listen. 💜",
                label_visibility="collapsed",
                key="personal_chat_input_box"
            )
        
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
            # Store the input before clearing
            message_to_send = user_input
            # Clear the input immediately
            st.session_state.user_message_input = ""
            st.session_state.clear_input = True
            
            with st.spinner("💭 Thinking..."):
                handle_user_message(message_to_send)
            st.rerun()
    
    # ==================== VOICE CHAT TAB ====================
    with tab_voice:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #E5E7EB; margin: 0;">🎧 Voice Companion – Talk to EmoSense</h2>
            <p style="color: #9CA3AF; margin-top: 0.5rem;">Record your voice and I'll respond with speech</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice settings row
        col_voice_settings1, col_voice_settings2 = st.columns([3, 1])
        
        with col_voice_settings1:
            st.markdown("""
            <div class="voice-recording-hint">
                💡 <strong>Tip:</strong> Click the microphone button to record your message. 
                Speak naturally and click again to stop recording.
            </div>
            """, unsafe_allow_html=True)
        
        with col_voice_settings2:
            show_voice_emotion = st.checkbox(
                "Show detected emotion", 
                value=st.session_state.show_voice_emotion,
                key="voice_emotion_toggle"
            )
            st.session_state.show_voice_emotion = show_voice_emotion
        
        spacer("sm")
        
        # Voice chat history display
        render_voice_chat_history()
        
        spacer("md")
        
        # Voice input section
        st.markdown("""
        <div style="background: rgba(138, 92, 246, 0.1); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #C4B5FD; margin: 0 0 0.75rem; font-weight: 500;">🎙️ Record Your Message</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio input widget
        audio_input = st.audio_input(
            "Record your voice message",
            key="voice_audio_input",
            label_visibility="collapsed"
        )
        
        # Process voice input
        if audio_input is not None and not st.session_state.voice_processing:
            st.session_state.voice_processing = True
            
            if voice_service:
                try:
                    with st.spinner("🎙️ Transcribing your voice..."):
                        # Read audio bytes
                        audio_bytes = audio_input.read()
                        
                        # Step 1: Transcribe
                        user_text = voice_service.speech_to_text(audio_bytes)
                        
                        if user_text.strip():
                            st.success(f"📝 Transcribed: \"{user_text}\"")
                            
                    with st.spinner("🧠 Analyzing emotions..."):
                        # Step 2: Detect emotion
                        emotion, confidence = detect_emotion_for_voice(user_text)
                    
                    with st.spinner("💭 Generating supportive response..."):
                        # Step 3: Generate response
                        bot_response = voice_service.generate_supportive_reply(
                            user_text,
                            emotion,
                            confidence,
                            st.session_state.voice_chat_history
                        )
                    
                    with st.spinner("🔊 Converting to speech..."):
                        # Step 4: Convert to speech
                        audio_response = voice_service.text_to_speech(bot_response)
                    
                    # Step 5: Add to conversation history
                    st.session_state.voice_chat_history.append({
                        "role": "user",
                        "content": user_text,
                        "emotion": emotion,
                        "confidence": confidence,
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    
                    st.session_state.voice_chat_history.append({
                        "role": "assistant",
                        "content": bot_response,
                        "audio": audio_response,
                        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    
                    # Keep last 20 messages
                    st.session_state.voice_chat_history = st.session_state.voice_chat_history[-20:]
                    
                    # Store latest audio for playback
                    st.session_state.last_voice_audio = audio_response
                    
                    st.session_state.voice_processing = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing voice: {str(e)}")
                    st.session_state.voice_processing = False
            else:
                st.error("🔑 Voice service unavailable. Please configure OPENAI_API_KEY.")
                st.session_state.voice_processing = False
        
        spacer("sm")
        
        # Clear voice history button
        col_clear, col_spacer = st.columns([1, 3])
        with col_clear:
            if st.button("🗑️ Clear Voice History", use_container_width=True, key="clear_voice_btn"):
                st.session_state.voice_chat_history = []
                st.session_state.last_voice_audio = None
                st.session_state.voice_processing = False
                st.rerun()
    
    spacer("md")
    
    # Safety reminder (shown for both tabs)
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
