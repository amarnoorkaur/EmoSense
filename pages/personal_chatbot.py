"""
Personal Emotion Companion - EmoSense AI
A warm, human-centered interface for personal emotional reflection
Two-column layout: Input on left, conversation on right
"""
import streamlit as st
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, page_container, hero_section, emotion_chip, spacer
from components.footer import render_footer
import datetime

# Configure page
set_page_config()

# Initialize session state for personal history
if "personal_history" not in st.session_state:
    st.session_state.personal_history = []

# Main container
with page_container():
    # Hero Section
    hero_section(
        title="💛 Personal Emotion Companion",
        subtitle="A private space to express how you feel and see what your words reveal.",
        detail=""
    )
    
    spacer("md")
    
    # Two-column layout
    col_left, col_right = st.columns([1, 1], gap="large")
    
    # LEFT COLUMN - Input
    with col_left:
        st.markdown("### ✍️ Express Yourself")
        
        user_text = st.text_area(
            "What's on your mind today?",
            height=200,
            placeholder="Type freely. This is just between you and EmoSense. Share your thoughts, feelings, or anything that's on your mind...",
            label_visibility="collapsed"
        )
        
        # Analysis options
        analysis_option = st.selectbox(
            "What do you want from EmoSense?",
            [
                "Just label my emotions",
                "Help me reflect on this",
                "Suggest gentle coping ideas"
            ]
        )
        
        # Analyze button
        if st.button("🔍 Analyze my emotions", type="primary", use_container_width=True):
            if user_text.strip():
                with st.spinner("Understanding your emotions..."):
                    # Detect emotions
                    predicted_emotions, probabilities = predict_emotions(user_text, threshold=0.3)
                    
                    # Generate AI reflection based on option
                    if analysis_option == "Just label my emotions":
                        if predicted_emotions:
                            emotion_list = ", ".join([f"{e.capitalize()}" for e in predicted_emotions[:3]])
                            ai_message = f"I sense {emotion_list} in your words. These emotions are valid and it's okay to feel them."
                        else:
                            ai_message = "Your message seems emotionally neutral. Sometimes that's exactly what we need - a moment of calm."
                    
                    elif analysis_option == "Help me reflect on this":
                        if predicted_emotions:
                            top_emotion = max(probabilities.items(), key=lambda x: x[1])
                            
                            reflections = {
                                "joy": "It sounds like you're experiencing something positive. What aspects of this situation bring you the most happiness?",
                                "sadness": "I hear that you're going through a difficult time. It's brave to acknowledge these feelings. What would comfort you right now?",
                                "anger": "Your frustration comes through clearly. Anger often signals that something important to you isn't being honored. What boundary feels crossed?",
                                "fear": "Uncertainty can be uncomfortable. What specifically worries you most about this situation?",
                                "anxiety": "I notice worry in your words. Sometimes naming our fears makes them feel more manageable. What's the core of your concern?",
                                "love": "There's warmth in what you're sharing. Love connects us deeply to what matters. Who or what are you grateful for?",
                                "surprise": "Something unexpected has happened. How are you processing this change?",
                                "neutral": "Your thoughts seem calm and measured. Sometimes clarity comes from a neutral perspective."
                            }
                            
                            ai_message = reflections.get(top_emotion[0], 
                                "Thank you for sharing. What does this situation mean to you personally?")
                        else:
                            ai_message = "Your message has a balanced emotional tone. What would you like to explore further?"
                    
                    else:  # Suggest coping ideas
                        if predicted_emotions:
                            top_emotion = max(probabilities.items(), key=lambda x: x[1])
                            
                            coping_strategies = {
                                "joy": "💚 Savor this moment. Consider journaling about what went well today, or sharing your joy with someone you care about.",
                                "sadness": "💙 Be gentle with yourself. Try: Taking a short walk, talking to a trusted friend, or doing something small that usually brings comfort.",
                                "anger": "🧡 Healthy anger processing: Try physical movement, write out your feelings without filtering, or take 10 deep breaths.",
                                "fear": "💜 Grounding techniques can help: Name 5 things you see, 4 things you hear, 3 things you can touch, 2 things you smell, 1 thing you taste.",
                                "anxiety": "🩵 Anxiety management: Try the 4-7-8 breathing (breathe in 4 counts, hold 7, exhale 8). Break big worries into smaller, manageable pieces.",
                                "love": "❤️ Nurture connection: Express appreciation to those you care about, or take time to reflect on meaningful relationships.",
                                "surprise": "💛 Processing change: Give yourself time to adjust. Write down your thoughts to make sense of new information.",
                                "neutral": "🤍 Maintain balance: Keep up with routines that support your well-being, like sleep, movement, and connection."
                            }
                            
                            ai_message = coping_strategies.get(top_emotion[0], 
                                "🌟 General wellness: Practice self-compassion, stay connected to supportive people, and prioritize rest.")
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
                st.warning("Please enter some text to analyze.")
        
        # Clear history button
        spacer("sm")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.personal_history = []
            st.rerun()
    
    # RIGHT COLUMN - Output/Conversation
    with col_right:
        st.markdown("### 💬 Your Emotional Journey")
        
        if not st.session_state.personal_history:
            # Empty state
            st.markdown("""
            <div class="card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🌟</div>
                <h3 style="color: #a5b4fc; margin-bottom: 1rem;">Welcome to Your Safe Space</h3>
                <p style="color: #cbd5e1; line-height: 1.8;">
                    Start by sharing what's on your mind in the left panel. 
                    I'll help you understand the emotions in your words, 
                    reflect on your experiences, or suggest gentle coping strategies.
                </p>
                <p style="color: #94a3b8; font-size: 0.875rem; margin-top: 1.5rem; font-style: italic;">
                    Remember: EmoSense is not a replacement for professional mental health support.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display conversation history (scrollable)
            st.markdown('<div style="max-height: 600px; overflow-y: auto; padding-right: 1rem;">', unsafe_allow_html=True)
            
            for entry in st.session_state.personal_history:
                # User message
                st.markdown(f"""
                <div class="message-user">
                    {entry['user_text']}
                </div>
                """, unsafe_allow_html=True)
                
                # Emotion chips
                if entry['emotions']:
                    chips_html = " ".join([
                        emotion_chip(e.capitalize(), entry['probabilities'][e], EMOJI_MAP.get(e, "🎭"))
                        for e in entry['emotions'][:3]
                    ])
                    st.markdown(f'<div style="margin: 0.5rem 0 1rem 0;">{chips_html}</div>', unsafe_allow_html=True)
                
                # AI reflection
                st.markdown(f"""
                <div class="message-ai">
                    {entry['ai_reflection']}
                </div>
                """, unsafe_allow_html=True)
                
                # Timestamp
                timestamp_str = entry['timestamp'].strftime("%I:%M %p")
                st.markdown(f'<div style="text-align: left; color: #94a3b8; font-size: 0.75rem; margin-bottom: 1.5rem;">{timestamp_str}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reminder note
            spacer("sm")
            st.markdown("""
            <div style="background: rgba(102, 126, 234, 0.1); border-left: 3px solid #667eea; padding: 1rem; border-radius: 5px; margin-top: 1rem;">
                <p style="color: #a5b4fc; font-size: 0.875rem; margin: 0;">
                    <strong>Remember:</strong> EmoSense is not a replacement for professional mental health support. 
                    If you're experiencing a crisis, please reach out to a mental health professional or crisis hotline.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    spacer("lg")

# Footer
render_footer()
