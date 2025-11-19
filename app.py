# Main Streamlit UI
# Emotion Analysis Chatbot using BERT
# Version 1.1 - Fixed HuggingFace Hub loading

import streamlit as st
import pandas as pd
import io
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP


def get_user_comments():
    """
    Get comments from user via CSV upload or text paste.
    Returns a list of clean, non-empty comment strings.
    """
    st.subheader("📊 Bulk Comment Analysis")
    st.markdown("Analyze multiple comments at once from CSV file or pasted text")
    
    input_method = st.radio(
        "Choose input method:",
        ["Upload CSV File", "Paste Comment Thread"],
        horizontal=True
    )
    
    comments = []
    
    if input_method == "Upload CSV File":
        uploaded_file = st.file_uploader(
            "Upload CSV file with comments",
            type=["csv"],
            help="CSV file should contain a column with text comments"
        )
        
        if uploaded_file is not None:
            try:
                # Read CSV with UTF-8 encoding
                df = pd.read_csv(uploaded_file, encoding='utf-8')
                
                st.success(f"✅ File loaded: {len(df)} rows found")
                
                # Show preview
                with st.expander("📋 Preview first 5 rows"):
                    st.dataframe(df.head(), use_container_width=True)
                
                # Auto-detect comment column
                possible_columns = ["comment", "comments", "text", "message", "body", "content", "review", "feedback"]
                comment_column = None
                
                for col in df.columns:
                    if col.lower() in possible_columns:
                        comment_column = col
                        break
                
                if comment_column:
                    st.info(f"🎯 Auto-detected comment column: **{comment_column}**")
                else:
                    # Let user select column
                    comment_column = st.selectbox(
                        "Select the column containing comments:",
                        options=df.columns.tolist(),
                        help="Choose the column with text comments to analyze"
                    )
                
                if comment_column:
                    # Extract comments, remove empty and duplicates
                    raw_comments = df[comment_column].dropna().astype(str).tolist()
                    comments = [c.strip() for c in raw_comments if c.strip()]
                    comments = list(dict.fromkeys(comments))  # Remove duplicates while preserving order
                    
                    st.metric("Valid Comments Found", len(comments))
                    
            except Exception as e:
                st.error(f"❌ Error reading CSV file: {str(e)}")
                st.info("💡 Tip: Ensure your CSV is properly formatted and UTF-8 encoded")
    
    else:  # Paste Comment Thread
        pasted_text = st.text_area(
            "Paste comments here (one per line):",
            height=300,
            placeholder="Comment 1\nComment 2\nComment 3\n...",
            help="Paste multiple comments, each on a new line"
        )
        
        if pasted_text:
            try:
                # Split by newline, clean, and remove duplicates
                raw_comments = pasted_text.split('\n')
                comments = [c.strip() for c in raw_comments if c.strip()]
                comments = list(dict.fromkeys(comments))  # Remove duplicates
                
                st.metric("Valid Comments Found", len(comments))
                
                # Show preview
                if comments:
                    with st.expander("📋 Preview first 5 comments"):
                        for i, comment in enumerate(comments[:5], 1):
                            st.text(f"{i}. {comment[:100]}{'...' if len(comment) > 100 else ''}")
                
            except Exception as e:
                st.error(f"❌ Error processing pasted text: {str(e)}")
    
    return comments


# Page configuration
st.set_page_config(
    page_title="EmoSense - Emotion Analysis",
    page_icon="🎭",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - Mode Selection
with st.sidebar:
    st.header("⚙️ Settings")
    
    analysis_mode = st.radio(
        "Analysis Mode:",
        ["💬 Chat Mode", "📊 Bulk Analysis"],
        help="Choose between single message chat or bulk comment analysis"
    )
    
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

# ============================================================================
# BULK ANALYSIS MODE
# ============================================================================
if analysis_mode == "📊 Bulk Analysis":
    comments = get_user_comments()
    
    if comments:
        st.markdown("---")
        
        if st.button("🚀 Analyze All Comments", type="primary", use_container_width=True):
            results = []
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, comment in enumerate(comments):
                status_text.text(f"Analyzing comment {idx + 1} of {len(comments)}...")
                
                try:
                    # Call emotion prediction
                    predicted_emotions, probabilities = predict_emotions(comment, threshold=threshold)
                    
                    # Get top emotion
                    if predicted_emotions:
                        top_emotion = max(probabilities.items(), key=lambda x: x[1])
                        emotion_label = f"{EMOJI_MAP.get(top_emotion[0], '🎭')} {top_emotion[0].capitalize()}"
                        confidence = f"{top_emotion[1]:.1%}"
                    else:
                        emotion_label = "😐 Neutral"
                        confidence = "N/A"
                    
                    results.append({
                        "Comment": comment[:100] + "..." if len(comment) > 100 else comment,
                        "Top Emotion": emotion_label,
                        "Confidence": confidence,
                        "All Emotions": ", ".join([e.capitalize() for e in predicted_emotions]) if predicted_emotions else "None"
                    })
                    
                except Exception as e:
                    results.append({
                        "Comment": comment[:100] + "..." if len(comment) > 100 else comment,
                        "Top Emotion": "❌ Error",
                        "Confidence": "N/A",
                        "All Emotions": str(e)
                    })
                
                progress_bar.progress((idx + 1) / len(comments))
            
            status_text.text("✅ Analysis complete!")
            progress_bar.empty()
            
            # Display results
            st.markdown("---")
            st.subheader("📈 Analysis Results")
            
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True, height=400)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Comments", len(results))
            with col2:
                successful = len([r for r in results if r["Top Emotion"] != "❌ Error"])
                st.metric("Successfully Analyzed", successful)
            with col3:
                errors = len(results) - successful
                st.metric("Errors", errors)
            
            # Download button
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="emotion_analysis_results.csv",
                mime="text/csv",
                use_container_width=True
            )

# ============================================================================
# CHAT MODE (Original functionality)
# ============================================================================
else:
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
