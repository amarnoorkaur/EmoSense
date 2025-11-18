# Main Streamlit UI
# Emotion Analysis Chatbot using BERT
# Version 1.1 - Fixed HuggingFace Hub loading

import streamlit as st
import pandas as pd
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP


# Page configuration
st.set_page_config(
    page_title="EmoSense - Emotion Analysis",
    page_icon="🎭",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and branding
st.title("🎭 EmoSense - Emotion Analysis Chatbot")
st.markdown("*Analyze emotions in text using AI-powered BERT model*")

# Threshold slider in sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    threshold = st.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.3,
        step=0.05,
        help="Minimum probability to display an emotion"
    )
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🎭"):
            # Display detected emotions with emojis
            st.markdown("**Detected Emotions:**")
            
            if message["emotions"]:
                # Show emotion chips with emojis
                emotion_html = ""
                for emotion in message["emotions"]:
                    prob = message["probabilities"][emotion]
                    emoji = EMOJI_MAP.get(emotion, '🎭')
                    emotion_html += f"""
                    <span style='display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 8px 15px; border-radius: 20px; margin: 5px; font-weight: bold;'>
                    {emoji} {emotion.upper()} ({prob:.1%})
                    </span>
                    """
                st.markdown(emotion_html, unsafe_allow_html=True)
            else:
                st.info("No emotions detected above threshold.")
            
            # Show probability chart
            st.markdown("**Top Emotions:**")
            sorted_probs = sorted(message["probabilities"].items(), key=lambda x: x[1], reverse=True)
            top_emotions = sorted_probs[:5]
            
            df = pd.DataFrame(top_emotions, columns=["Emotion", "Probability"])
            df["Emoji"] = df["Emotion"].map(EMOJI_MAP)
            df["Display"] = df.apply(lambda row: f"{row['Emoji']} {row['Emotion'].capitalize()}", axis=1)
            df["Probability"] = df["Probability"] * 100
            
            chart_df = df[["Display", "Probability"]].set_index("Display")
            st.bar_chart(chart_df, height=200)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get predictions
    with st.spinner("Analyzing emotions..."):
        predicted_emotions, probabilities = predict_emotions(prompt, threshold=threshold)
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "emotions": predicted_emotions,
        "probabilities": probabilities
    })
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🎭"):
        st.markdown("**Detected Emotions:**")
        
        if predicted_emotions:
            emotion_html = ""
            for emotion in predicted_emotions:
                prob = probabilities[emotion]
                emoji = EMOJI_MAP.get(emotion, '🎭')
                emotion_html += f"""
                <span style='display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 8px 15px; border-radius: 20px; margin: 5px; font-weight: bold;'>
                {emoji} {emotion.upper()} ({prob:.1%})
                </span>
                """
            st.markdown(emotion_html, unsafe_allow_html=True)
        else:
            st.info("No emotions detected above threshold.")
        
        # Show probability chart
        st.markdown("**Top Emotions:**")
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        top_emotions = sorted_probs[:5]
        
        df = pd.DataFrame(top_emotions, columns=["Emotion", "Probability"])
        df["Emoji"] = df["Emotion"].map(EMOJI_MAP)
        df["Display"] = df.apply(lambda row: f"{row['Emoji']} {row['Emotion'].capitalize()}", axis=1)
        df["Probability"] = df["Probability"] * 100
        
        chart_df = df[["Display", "Probability"]].set_index("Display")
        st.bar_chart(chart_df, height=200)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by BERT & Streamlit | Built with ❤️"
    "</div>",
    unsafe_allow_html=True
)
