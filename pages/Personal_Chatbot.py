"""
Personal Emotion Companion - EmoSense AI
Warm, cozy, emotional interface with chat bubbles and emotion chips
"""
import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, emotion_chip, spacer
from components.footer import render_footer
import datetime

# Configure page
set_page_config()
inject_global_styles()

# Initialize session state
if "personal_history" not in st.session_state:
    st.session_state.personal_history = []

# Main container
with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "💛 Personal Emotion Companion",
        "A private space to express how you feel and see what your words reveal."
    )
    
    spacer("md")
    
    # Two-column layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    # LEFT COLUMN - Input
    with col_left:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">✍️ Express Yourself</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: -1rem;"></div>', unsafe_allow_html=True)
        
        user_text = st.text_area(
            "What's on your mind today?",
            height=200,
            placeholder="Type freely. This is just between you and EmoSense. Share your thoughts, feelings, or anything that's on your mind...",
            label_visibility="collapsed",
            key="user_input_text"
        )
        
        spacer("sm")
        
        analysis_option = st.selectbox(
            "What do you want from EmoSense?",
            [
                "Just label my emotions",
                "Help me reflect on this",
                "Suggest gentle coping ideas"
            ]
        )
        
        spacer("sm")
        
        if st.button("🔍 Analyze My Emotions", type="primary", use_container_width=True):
            if user_text.strip():
                with st.spinner("Understanding your emotions..."):
                    # Detect emotions
                    predicted_emotions, probabilities = predict_emotions(user_text, threshold=0.3)
                    
                    # Generate context-aware AI response
                    if analysis_option == "Just label my emotions":
                        if predicted_emotions:
                            emotion_list = ", ".join([f"{e.capitalize()}" for e in predicted_emotions[:3]])
                            ai_message = f"I sense {emotion_list} in your words. These emotions are valid and it's okay to feel them. 💜"
                        else:
                            ai_message = "Your message seems emotionally neutral. Sometimes that's exactly what we need - a moment of calm. 🌊"
                    
                    elif analysis_option == "Help me reflect on this":
                        if predicted_emotions:
                            top_emotion = max(probabilities.items(), key=lambda x: x[1])
                            
                            reflections = {
                                "joy": "✨ It sounds like you're experiencing something positive. What aspects of this situation bring you the most happiness?",
                                "sadness": "💙 I hear that you're going through a difficult time. It's brave to acknowledge these feelings. What would comfort you right now?",
                                "anger": "🔥 Your frustration comes through clearly. Anger often signals that something important to you isn't being honored. What boundary feels crossed?",
                                "fear": "🌙 Uncertainty can be uncomfortable. What specifically worries you most about this situation?",
                                "anxiety": "🌊 I notice worry in your words. Sometimes naming our fears makes them feel more manageable. What's the core of your concern?",
                                "love": "❤️ There's warmth in what you're sharing. Love connects us deeply to what matters. Who or what are you grateful for?",
                                "surprise": "⚡ Something unexpected has happened. How are you processing this change?",
                                "neutral": "🤍 Your thoughts seem calm and measured. Sometimes clarity comes from a neutral perspective."
                            }
                            
                            ai_message = reflections.get(top_emotion[0], 
                                "Thank you for sharing. What does this situation mean to you personally? 💭")
                        else:
                            ai_message = "Your message has a balanced emotional tone. What would you like to explore further? 🌟"
                    
                    else:  # Coping strategies
                        if predicted_emotions:
                            top_emotion = max(probabilities.items(), key=lambda x: x[1])
                            
                            coping_strategies = {
                                "joy": "💚 **Savor this moment.** Consider journaling about what went well today, or sharing your joy with someone you care about.",
                                "sadness": "💙 **Be gentle with yourself.** Try: Taking a short walk, talking to a trusted friend, or doing something small that usually brings comfort.",
                                "anger": "🧡 **Healthy anger processing:** Try physical movement, write out your feelings without filtering, or take 10 deep breaths.",
                                "fear": "💜 **Grounding technique:** Name 5 things you see, 4 you hear, 3 you can touch, 2 you smell, 1 you taste.",
                                "anxiety": "🩵 **Anxiety management:** Try 4-7-8 breathing (in 4, hold 7, out 8). Break big worries into smaller, manageable pieces.",
                                "love": "❤️ **Nurture connection:** Express appreciation to those you care about, or take time to reflect on meaningful relationships.",
                                "surprise": "💛 **Processing change:** Give yourself time to adjust. Write down your thoughts to make sense of new information.",
                                "neutral": "🤍 **Maintain balance:** Keep up routines that support your well-being, like sleep, movement, and connection."
                            }
                            
                            ai_message = coping_strategies.get(top_emotion[0], 
                                "🌟 **General wellness:** Practice self-compassion, stay connected to supportive people, and prioritize rest.")
                        else:
                            ai_message = "🌟 You seem balanced. Continue with practices that support your well-being: rest, connection, and gentle self-care."
                    
                    # Add to history
                    st.session_state.personal_history.append({
                        "timestamp": datetime.datetime.now(),
                        "user_text": user_text,
                        "emotions": predicted_emotions,
                        "probabilities": probabilities,
                        "ai_reflection": ai_message,
                        "option": analysis_option
                    })
                    
                    st.success("✨ Analysis complete!")
                    st.rerun()
            else:
                st.warning("⚠️ Please enter some text to analyze.")
        
        spacer("sm")
        
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state.personal_history = []
            st.rerun()
    
    # RIGHT COLUMN - Conversation
    with col_right:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">💬 Your Emotional Journey</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: -1rem;"></div>', unsafe_allow_html=True)
        
        if not st.session_state.personal_history:
            # Empty state
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem; margin-top: 1rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🌟</div>
                <h3 style="color: #FFFFFF; margin-bottom: 1rem;">Welcome to Your Safe Space</h3>
                <p style="color: #A8A9B3; line-height: 1.8; max-width: 400px; margin: 0 auto;">
                    Start by sharing what's on your mind in the left panel. 
                    I'll help you understand the emotions in your words, 
                    reflect on your experiences, or suggest gentle coping strategies.
                </p>
                <p style="color: #8A5CF6; font-size: 0.875rem; margin-top: 1.5rem; font-style: italic;">
                    💜 Remember: EmoSense is not a replacement for professional mental health support.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display conversation (newest first)
            st.markdown('<div style="max-height: 600px; overflow-y: auto; padding-right: 0.5rem; margin-top: 1rem;">', unsafe_allow_html=True)
            
            for entry in reversed(st.session_state.personal_history):
                # User message
                st.markdown(f"""
                <div class="message-user fade-in">
                    {entry['user_text']}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
                
                # Emotion chips
                if entry['emotions']:
                    chips_html = " ".join([
                        emotion_chip(e.capitalize(), entry['probabilities'][e], EMOJI_MAP.get(e, "🎭"))
                        for e in entry['emotions'][:3]
                    ])
                    st.markdown(f'<div style="text-align: right; margin: 0.5rem 0 1rem 0;">{chips_html}</div>', unsafe_allow_html=True)
                
                # AI reflection
                st.markdown(f"""
                <div class="message-ai fade-in">
                    {entry['ai_reflection']}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
                
                # Timestamp
                timestamp_str = entry['timestamp'].strftime("%I:%M %p")
                st.markdown(f'<div style="text-align: left; color: #A8A9B3; font-size: 0.75rem; margin-bottom: 1.5rem;">{timestamp_str}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reminder
            spacer("sm")
            st.markdown("""
            <div style="background: rgba(138, 92, 246, 0.1); border-left: 3px solid #8A5CF6; padding: 1rem; border-radius: 8px;">
                <p style="color: #A8A9B3; font-size: 0.875rem; margin: 0;">
                    <strong style="color: #FFFFFF;">Remember:</strong> EmoSense is not a replacement for professional mental health support. 
                    If you're experiencing a crisis, please reach out to a mental health professional or crisis hotline.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
