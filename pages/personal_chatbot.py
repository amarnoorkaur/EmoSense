"""
Personal Emotion Companion - Safe space for emotional expression
"""
import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
import datetime

def render_personal_chatbot():
    """Render the personal emotion companion page"""
    
    st.markdown("""
    <style>
    .chat-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
    }
    
    .chat-title {
        font-size: 32px;
        font-weight: 700;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .chat-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    .emotion-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px;
        font-size: 14px;
    }
    
    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    
    .message-ai {
        background: #f8f9ff;
        color: #1e293b;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="chat-container">
        <h1 class="chat-title">💛 Personal Emotion Companion</h1>
        <p class="chat-subtitle">
            A safe space to express yourself. I'm here to understand your emotions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "personal_messages" not in st.session_state:
        st.session_state.personal_messages = [
            {
                "role": "assistant",
                "content": "Hello! 👋 I'm your personal emotion companion. How are you feeling today? Share anything on your mind, and I'll help you understand your emotions better.",
                "emotions": []
            }
        ]
    
    # Display chat history
    for message in st.session_state.personal_messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-user">{message["content"]}</div><div style="clear: both;"></div>', unsafe_allow_html=True)
            
            if message.get("emotions"):
                emotion_badges = " ".join([
                    f'<span class="emotion-badge" style="background: rgba(102, 126, 234, 0.15); color: #667eea;">'
                    f'{EMOJI_MAP.get(e, "🎭")} {e.capitalize()}</span>'
                    for e in message["emotions"][:3]
                ])
                st.markdown(f'<div style="text-align: right; margin-bottom: 20px;">{emotion_badges}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-ai">🤖 {message["content"]}</div><div style="clear: both;"></div>', unsafe_allow_html=True)
            st.markdown("<br/>", unsafe_allow_html=True)
    
    # Chat input
    with st.form(key="personal_chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Express yourself...",
            placeholder="Type how you're feeling...",
            height=100,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([4, 1])
        with col2:
            submitted = st.form_submit_button("Send 💬", use_container_width=True, type="primary")
    
    if submitted and user_input:
        # Analyze emotions
        predicted_emotions, probabilities = predict_emotions(user_input, threshold=0.3)
        
        # Add user message
        st.session_state.personal_messages.append({
            "role": "user",
            "content": user_input,
            "emotions": predicted_emotions,
            "timestamp": datetime.datetime.now()
        })
        
        # Generate empathetic response
        if not predicted_emotions:
            response = "I sense you're sharing something neutral or complex. Sometimes emotions are subtle, and that's perfectly okay. Tell me more about what's on your mind."
        else:
            dominant = predicted_emotions[0]
            emoji = EMOJI_MAP.get(dominant, "🎭")
            
            # Empathetic responses based on emotion
            responses = {
                "joy": f"I can feel your happiness! {emoji} It's wonderful to see you feeling joyful. What brought this positive energy today?",
                "sadness": f"I hear you, and I'm here with you. {emoji} It's okay to feel sad. Would you like to talk about what's weighing on your heart?",
                "anger": f"I understand you're feeling frustrated. {emoji} Those feelings are valid. What happened that made you feel this way?",
                "fear": f"I sense some worry or anxiety. {emoji} It's brave of you to share this. Remember, you're not alone. What's causing this fear?",
                "love": f"Beautiful! {emoji} Love is such a powerful emotion. Who or what is bringing you this warmth?",
                "surprise": f"Oh! {emoji} Something unexpected happened! Tell me more about what surprised you.",
                "neutral": f"Thank you for sharing. {emoji} I'm listening. Feel free to express whatever comes to mind."
            }
            
            response = responses.get(dominant, f"I recognize you're feeling {dominant}. {emoji} Thank you for trusting me with this. How can I support you?")
            
            # Add insight
            if len(predicted_emotions) > 1:
                response += f"\n\nI also notice traces of {', '.join(predicted_emotions[1:3])}. It's natural to feel multiple emotions at once."
        
        # Add AI response
        st.session_state.personal_messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    # Sidebar with emotion journal
    with st.sidebar:
        st.markdown("### 📖 Emotion Journal")
        
        user_messages = [m for m in st.session_state.personal_messages if m["role"] == "user"]
        
        if user_messages:
            all_emotions = []
            for msg in user_messages:
                all_emotions.extend(msg.get("emotions", []))
            
            if all_emotions:
                from collections import Counter
                emotion_counts = Counter(all_emotions)
                
                st.markdown("**Your Emotional Patterns:**")
                for emotion, count in emotion_counts.most_common(5):
                    emoji = EMOJI_MAP.get(emotion, "🎭")
                    st.markdown(f"{emoji} **{emotion.capitalize()}**: {count} times")
            
            st.markdown(f"\n**Total Conversations:** {len(user_messages)}")
        else:
            st.info("Start chatting to see your emotional patterns!")
        
        if st.button("🔄 Start Fresh", use_container_width=True):
            st.session_state.personal_messages = [
                {
                    "role": "assistant",
                    "content": "Hello! 👋 I'm your personal emotion companion. How are you feeling today?",
                    "emotions": []
                }
            ]
            st.rerun()
