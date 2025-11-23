# Main Streamlit UI
# Emotion Analysis Chatbot using BERT
# Version 2.0 - Added Smart Emotional Summary Feature

import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
from collections import Counter
from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from utils.ai_summary import generate_ai_summary

# Try to import local summarization, fallback to API version
try:
    from services.summary_service_local import summarize_text_local, combine_emotion_and_summary
    USE_LOCAL_MODEL = True
except:
    from services.summary_service import summarize_text, combine_emotion_and_summary
    USE_LOCAL_MODEL = False

from components.emotional_summary_card import render_emotional_summary


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


def render_emotion_dashboard(results_df):
    """
    Render analytics dashboard for emotion distribution analysis.
    
    Args:
        results_df: DataFrame with columns ['comment', 'emotion']
    """
    if results_df is None or len(results_df) == 0:
        st.warning("⚠️ No data available to display dashboard")
        return
    
    # Clean emotion labels (remove emojis and extra formatting)
    df = results_df.copy()
    
    # Extract clean emotion names from "Top Emotion" column if it has emojis
    if 'Top Emotion' in df.columns:
        df['emotion'] = df['Top Emotion'].str.split().str[-1].str.lower()
    elif 'emotion' not in df.columns:
        st.error("❌ DataFrame must have either 'emotion' or 'Top Emotion' column")
        return
    
    # Filter out errors
    df = df[df['emotion'] != 'error']
    
    if len(df) == 0:
        st.warning("⚠️ No valid emotion data to display")
        return
    
    st.markdown("---")
    st.header("📊 Emotion Analytics Dashboard")
    
    # Count emotions
    emotion_counts = df['emotion'].value_counts()
    total_comments = len(df)
    
    # Calculate percentages
    emotion_percentages = (emotion_counts / total_comments * 100).round(1)
    
    # Combine counts and percentages
    emotion_stats = pd.DataFrame({
        'Emotion': emotion_counts.index,
        'Count': emotion_counts.values,
        'Percentage': emotion_percentages.values
    })
    
    # === TOP 4 EMOTIONS ===
    st.subheader("🏆 Top 4 Dominant Emotions")
    top_4 = emotion_stats.head(4)
    
    cols = st.columns(4)
    for idx, (_, row) in enumerate(top_4.iterrows()):
        with cols[idx]:
            emoji = EMOJI_MAP.get(row['Emotion'], '🎭')
            st.metric(
                label=f"{emoji} {row['Emotion'].capitalize()}",
                value=f"{row['Count']} comments",
                delta=f"{row['Percentage']}%"
            )
    
    st.markdown("---")
    
    # === SUMMARY NARRATIVE ===
    try:
        top_emotions_text = ", ".join([
            f"{row['Emotion']} ({row['Percentage']}%)" 
            for _, row in top_4.head(3).iterrows()
        ])
        
        st.info(
            f"📝 **Summary:** Out of {total_comments:,} comments analyzed, "
            f"the dominant emotions were **{top_emotions_text}**."
        )
    except Exception as e:
        st.info(f"📝 **Summary:** Analyzed {total_comments:,} comments successfully.")
    
    st.markdown("---")
    
    # === VISUALIZATIONS ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Emotion Distribution (Bar Chart)")
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Bar chart
            bars = ax.bar(emotion_stats['Emotion'], emotion_stats['Count'], color='steelblue', alpha=0.7)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9)
            
            ax.set_xlabel('Emotion', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Comments', fontsize=12, fontweight='bold')
            ax.set_title('Comment Count by Emotion', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
        except Exception as e:
            st.error(f"Error creating bar chart: {str(e)}")
    
    with col2:
        st.subheader("🥧 Emotion Percentage (Pie Chart)")
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Pie chart
            wedges, texts, autotexts = ax.pie(
                emotion_stats['Percentage'],
                labels=emotion_stats['Emotion'],
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10}
            )
            
            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('Emotion Distribution by Percentage', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
        except Exception as e:
            st.error(f"Error creating pie chart: {str(e)}")
    
    st.markdown("---")
    
    # === DETAILED STATS TABLE ===
    st.subheader("📈 Detailed Emotion Statistics")
    
    # Format the stats table
    display_stats = emotion_stats.copy()
    display_stats['Emotion'] = display_stats['Emotion'].apply(
        lambda x: f"{EMOJI_MAP.get(x, '🎭')} {x.capitalize()}"
    )
    display_stats['Percentage'] = display_stats['Percentage'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        display_stats,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Emotion": st.column_config.TextColumn("Emotion", width="medium"),
            "Count": st.column_config.NumberColumn("Count", width="small"),
            "Percentage": st.column_config.TextColumn("Percentage", width="small")
        }
    )


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
        ["💬 Chat Mode", "📊 Bulk Analysis", "🧠 Smart Emotional Summary"],
        help="Choose between single message chat, bulk analysis, or smart emotional summary"
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
            
            # === RENDER ANALYTICS DASHBOARD ===
            render_emotion_dashboard(results_df)
            
            # === AI-POWERED SUMMARY & INSIGHTS ===
            st.markdown("---")
            st.subheader("🤖 AI-Powered Summary & Insights")
            st.markdown("Get intelligent analysis and actionable recommendations powered by AI")
            
            # Get OpenAI API key from Streamlit secrets or user input
            api_key = None
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
            else:
                with st.expander("🔑 Configure OpenAI API Key"):
                    st.markdown("""
                    To use AI-powered insights, you need an OpenAI API key:
                    1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
                    2. For Streamlit Cloud: Add `OPENAI_API_KEY` to your app secrets
                    3. For local development: Enter the key below (session only)
                    """)
                    api_key = st.text_input("Enter your OpenAI API Key:", type="password", key="openai_key_input")
            
            if st.button("✨ Generate AI Insights", type="primary", use_container_width=True):
                if not api_key:
                    st.warning("⚠️ Please configure your OpenAI API key to use this feature.")
                else:
                    with st.spinner("🧠 AI is analyzing your data and generating insights..."):
                        # Prepare data for AI analysis
                        ai_results_df = results_df.copy()
                        
                        # Extract primary emotion and confidence as numeric values
                        ai_results_df['Primary Emotion'] = ai_results_df['Top Emotion'].apply(
                            lambda x: x.split()[-1].lower() if '❌' not in x else 'error'
                        )
                        ai_results_df['Confidence'] = ai_results_df['Confidence'].apply(
                            lambda x: float(x.strip('%')) / 100 if x != 'N/A' else 0.0
                        )
                        
                        # Generate AI summary
                        summary = generate_ai_summary(ai_results_df, api_key=api_key)
                        
                        # Display the summary
                        st.markdown("### 📋 AI-Generated Insights Report")
                        st.markdown(summary)
                        
                        # Download option
                        summary_download = f"""# AI-Generated Insights Report
## Emotion Analysis Summary

Generated by EmoSense AI

---

{summary}

---

**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Comments Analyzed:** {len(results_df)}
"""
                        st.download_button(
                            label="📥 Download AI Insights Report",
                            data=summary_download,
                            file_name="ai_insights_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )

# ============================================================================
# CHAT MODE (Original functionality)
# ============================================================================
elif analysis_mode == "💬 Chat Mode":
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

# ============================================================================
# SMART EMOTIONAL SUMMARY MODE - BUSINESS SOCIAL MEDIA ANALYTICS
# ============================================================================
elif analysis_mode == "🧠 Smart Emotional Summary":
    st.title("🧠 Smart Social Media Analytics for Business")
    st.markdown("""
    ### 📱 Analyze Customer Reactions to Your Social Media Posts
    
    Understand how your audience is responding to your content. Get AI-powered insights about:
    - **Customer Sentiment** - What emotions your posts are generating
    - **Engagement Quality** - Whether reactions are positive, negative, or mixed
    - **Actionable Recommendations** - How to improve your social media strategy
    - **Brand Health** - Overall emotional perception of your brand
    """)
    
    st.info("💡 **Use Case**: Paste comments from Instagram, Facebook, Twitter, LinkedIn posts or product reviews to understand customer sentiment.")
    
    st.markdown("---")
    
    # Input text area
    input_text = st.text_area(
        "📝 Paste Customer Comments / Reviews / Social Media Feedback:",
        height=200,
        placeholder="Example: 'Love this product! Amazing quality and fast shipping. Highly recommend!' or paste multiple comments separated by line breaks...",
        help="Paste comments from your social media posts, product reviews, or customer feedback. Works best with 50-500 words."
    )
    
    # Configuration expander
    with st.expander("⚙️ Configuration"):
        st.markdown("""
        **API Keys Required:**
        - `HUGGINGFACE_API_KEY` - For text summarization (BART model)
        - `OPENAI_API_KEY` - Optional, for additional AI insights
        
        Set these as environment variables or in Streamlit secrets.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Min Words", "10")
        with col2:
            st.metric("Max Words", "~1000")
    
    st.markdown("---")
    
    # Generate button
    if st.button("✨ Generate Emotional Summary", type="primary", use_container_width=True):
        if not input_text or len(input_text.strip()) == 0:
            st.error("⚠️ Please enter some text to analyze")
        else:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📊 Complete Analysis", "📝 Summary Only"])
            
            with tab1:
                # Step 1: Emotion Analysis
                with st.spinner("🎭 Analyzing emotions..."):
                    predicted_emotions, probabilities = predict_emotions(input_text, threshold=threshold)
                    
                    if not predicted_emotions:
                        st.warning("No strong emotions detected. Try lowering the confidence threshold in the sidebar.")
                        predicted_emotions = ["neutral"]
                        probabilities = {"neutral": 0.5}
                
                st.success("✅ Emotion analysis complete!")
                
                # Step 2: Generate Summary
                with st.spinner("📝 Generating AI summary (this may take 20-30 seconds on first run)..."):
                    if USE_LOCAL_MODEL:
                        summary = summarize_text_local(input_text)
                    else:
                        summary = summarize_text(input_text)
                
                st.success("✅ Summary generated!")
                
                # Step 3: Combine Results
                emotion_output = {
                    "probabilities": probabilities
                }
                
                combined_result = combine_emotion_and_summary(
                    emotion_output,
                    summary,
                    input_text
                )
                
                # Step 4: Render Beautiful Output
                render_emotional_summary(combined_result)
                
                # Download option
                st.markdown("---")
                st.subheader("💾 Export Business Analytics Report")
                
                # Calculate business metrics
                positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
                negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
                
                # Calculate sentiment scores and cap at 100%
                positive_score = min(sum([prob for emotion, prob in combined_result['all_emotions'].items() if emotion in positive_emotions]), 1.0)
                negative_score = min(sum([prob for emotion, prob in combined_result['all_emotions'].items() if emotion in negative_emotions]), 1.0)
                
                if combined_result['dominant_emotion'] in positive_emotions:
                    sentiment_status = "Positive"
                    brand_health = "Healthy - Positive customer sentiment"
                elif combined_result['dominant_emotion'] in negative_emotions:
                    sentiment_status = "Negative"
                    brand_health = "Needs Attention - Address customer concerns"
                else:
                    sentiment_status = "Neutral/Mixed"
                    brand_health = "Monitor - Mixed customer reactions"
                
                # Prepare business-focused download data
                download_data = f"""# Social Media Sentiment Analysis Report
**Generated by EmoSense Business Analytics**
**Date:** {pd.Timestamp.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 📊 Executive Summary

**Brand Health Status:** {brand_health}
**Overall Sentiment:** {sentiment_status}
**Customer Emotion:** {combined_result['dominant_emotion'].capitalize()} ({combined_result['confidence']:.1%} confidence)

---

## 📝 Customer Feedback Summary

{combined_result['summary']}

---

## 💡 Key Insights

**Why These Emotions Were Detected:**
{combined_result['reasoning']}

**Emotional Triggers Identified:**
{', '.join(combined_result.get('detected_keywords', ['None detected'])) if combined_result.get('detected_keywords') else 'None detected'}

---

## 📈 Sentiment Metrics

- **Positive Sentiment Score:** {positive_score:.1%}
- **Negative Sentiment Score:** {negative_score:.1%}
- **Dominant Emotion Confidence:** {combined_result['confidence']:.1%}

---

## 🎭 Detailed Emotion Breakdown

"""
                for emotion, prob in sorted(combined_result['all_emotions'].items(), key=lambda x: x[1], reverse=True):
                    category = "Positive" if emotion in positive_emotions else "Negative" if emotion in negative_emotions else "Neutral"
                    download_data += f"- **{emotion.capitalize()}**: {prob:.1%} ({category})\n"
                
                download_data += f"""
---

## 🎯 Recommended Business Actions

{combined_result['suggested_action']}

---

## 📋 Original Customer Feedback

{input_text}

---

## 📊 Performance Indicators

- **Engagement Quality:** {"High" if combined_result['confidence'] > 0.7 else "Medium" if combined_result['confidence'] > 0.4 else "Low"}
- **Response Priority:** {"Immediate" if negative_score > 0.5 else "Normal" if negative_score > 0.3 else "Low"}
- **Brand Sentiment:** {sentiment_status}

---

*This report was generated using EmoSense AI-powered Social Media Analytics*
*For questions or support, visit your EmoSense dashboard*
"""
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Business Report (MD)",
                        data=download_data,
                        file_name=f"social_media_analytics_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    # JSON export for analytics tools
                    import json
                    
                    # Create business-focused JSON structure
                    business_json = {
                        "report_metadata": {
                            "generated_at": pd.Timestamp.now().isoformat(),
                            "report_type": "social_media_sentiment_analysis",
                            "tool": "EmoSense Business Analytics"
                        },
                        "brand_health": {
                            "status": brand_health,
                            "overall_sentiment": sentiment_status,
                            "positive_score": f"{positive_score:.2%}",
                            "negative_score": f"{negative_score:.2%}"
                        },
                        "dominant_emotion": {
                            "emotion": combined_result['dominant_emotion'],
                            "confidence": f"{combined_result['confidence']:.2%}",
                            "category": "positive" if combined_result['dominant_emotion'] in positive_emotions else "negative" if combined_result['dominant_emotion'] in negative_emotions else "neutral"
                        },
                        "summary": combined_result['summary'],
                        "reasoning": combined_result['reasoning'],
                        "all_emotions": {k: f"{v:.2%}" for k, v in combined_result['all_emotions'].items()},
                        "detected_keywords": combined_result.get('detected_keywords', []),
                        "recommended_actions": combined_result['suggested_action'],
                        "customer_feedback": input_text
                    }
                    
                    json_data = json.dumps(business_json, indent=2)
                    st.download_button(
                        label="📥 Download Analytics Data (JSON)",
                        data=json_data,
                        file_name=f"analytics_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
            
            with tab2:
                # Quick Business Snapshot View
                with st.spinner("Analyzing customer sentiment..."):
                    if USE_LOCAL_MODEL:
                        summary = summarize_text_local(input_text)
                    else:
                        summary = summarize_text(input_text)
                    predicted_emotions, probabilities = predict_emotions(input_text, threshold=threshold)
                
                st.subheader("📝 Customer Feedback Summary")
                st.info(summary)
                
                if predicted_emotions:
                    st.subheader("🏢 Brand Sentiment Snapshot")
                    top_emotion = max(probabilities.items(), key=lambda x: x[1])
                    emoji = EMOJI_MAP.get(top_emotion[0], "🎭")
                    
                    # Determine sentiment category
                    positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
                    negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
                    
                    if top_emotion[0] in positive_emotions:
                        sentiment_indicator = "🟢 Positive Sentiment"
                    elif top_emotion[0] in negative_emotions:
                        sentiment_indicator = "🔴 Negative Sentiment - Action Needed"
                    else:
                        sentiment_indicator = "🟡 Neutral/Mixed Sentiment"
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            label="Customer Emotion",
                            value=f"{emoji} {top_emotion[0].capitalize()}",
                            delta=f"{top_emotion[1]:.0%} confidence"
                        )
                    with col2:
                        st.metric(
                            label="Overall Sentiment",
                            value=sentiment_indicator.split()[1],
                            delta=sentiment_indicator
                        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by BERT & Streamlit | Built with ❤️"
    "</div>",
    unsafe_allow_html=True
)
