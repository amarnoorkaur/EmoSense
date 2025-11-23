"""
Streamlit Component for Smart Emotional Summary Display
"""
import streamlit as st
from utils.labels import EMOJI_MAP


def render_emotional_summary(result: dict):
    """
    Render the Smart Emotional Summary for Business Social Media Analytics
    
    Args:
        result: Dictionary containing summary, emotions, and reasoning
    """
    st.markdown("---")
    st.subheader("📊 Social Media Sentiment Analysis Report")
    
    # Summary Section
    st.markdown("#### 📌 Customer Feedback Summary")
    if result["summary"].startswith("⚠️") or result["summary"].startswith("⏳"):
        st.warning(result["summary"])
    else:
        st.info(result["summary"])
    
    # Quick Brand Health Indicator
    dominant_emotion = result["dominant_emotion"]
    confidence = result.get("confidence", 0.0)
    
    # Categorize emotions for business
    positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
    negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
    neutral_emotions = ["curiosity", "surprise", "confusion", "realization", "neutral"]
    
    if dominant_emotion in positive_emotions:
        sentiment_category = "Positive"
        sentiment_color = "🟢"
        brand_health = "Healthy"
    elif dominant_emotion in negative_emotions:
        sentiment_category = "Negative"
        sentiment_color = "🔴"
        brand_health = "Needs Attention"
    else:
        sentiment_category = "Neutral/Mixed"
        sentiment_color = "🟡"
        brand_health = "Monitor Closely"
    
    # Brand Health Dashboard
    st.markdown("#### 🏢 Brand Health Indicator")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Overall Sentiment",
            value=f"{sentiment_color} {sentiment_category}",
            delta=brand_health
        )
    
    with col2:
        emoji = EMOJI_MAP.get(dominant_emotion, "🎭")
        st.metric(
            label="Dominant Emotion",
            value=f"{emoji} {dominant_emotion.capitalize()}",
            delta=f"{confidence:.0%} confidence"
        )
    
    with col3:
        # Calculate engagement score based on emotion diversity
        emotion_count = len([e for e in result.get("all_emotions", {}).values() if e > 0.2])
        st.metric(
            label="Emotion Diversity",
            value=f"{emotion_count} emotions",
            delta="High engagement" if emotion_count > 3 else "Focused response"
        )
    
    st.markdown("---")
    
    # Emotion Probability Breakdown
    st.markdown("#### 📊 Customer Emotion Breakdown")
    
    all_emotions = result.get("all_emotions", {})
    if all_emotions:
        # Sort emotions by probability
        sorted_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)
        
        # Display top emotions in columns
        top_emotions = sorted_emotions[:4]
        cols = st.columns(len(top_emotions))
        
        for idx, (emotion, prob) in enumerate(top_emotions):
            with cols[idx]:
                emotion_emoji = EMOJI_MAP.get(emotion, "🎭")
                
                # Add context for business
                if emotion in positive_emotions:
                    delta_indicator = "Positive signal"
                    delta_color = "normal"
                elif emotion in negative_emotions:
                    delta_indicator = "Action needed"
                    delta_color = "inverse"
                else:
                    delta_indicator = "Monitor"
                    delta_color = "off"
                
                st.metric(
                    label=f"{emotion_emoji} {emotion.capitalize()}",
                    value=f"{prob:.1%}",
                    delta=delta_indicator
                )
        
        # Full breakdown in expander
        with st.expander("📋 View All Customer Emotions"):
            emotion_df_data = {
                "Emotion": [f"{EMOJI_MAP.get(e, '🎭')} {e.capitalize()}" for e, _ in sorted_emotions],
                "Percentage": [f"{p:.2%}" for _, p in sorted_emotions],
                "Category": []
            }
            
            for e, _ in sorted_emotions:
                if e in positive_emotions:
                    emotion_df_data["Category"].append("🟢 Positive")
                elif e in negative_emotions:
                    emotion_df_data["Category"].append("🔴 Negative")
                else:
                    emotion_df_data["Category"].append("🟡 Neutral")
            
            st.table(emotion_df_data)
    else:
        st.info("No emotion probabilities available")
    
    st.markdown("---")
    
    # Business Insights
    st.markdown("#### 💡 Marketing Intelligence")
    
    # Reasoning Section
    st.markdown("**🔍 Why These Emotions Were Detected:**")
    st.markdown(f"_{result.get('reasoning', 'No reasoning available')}_")
    
    # Detected Keywords
    keywords = result.get("detected_keywords", [])
    if keywords:
        st.markdown("**🔑 Key Emotional Triggers in Customer Feedback:**")
        keyword_html = " ".join([f"`{kw}`" for kw in keywords])
        st.markdown(keyword_html)
    
    st.markdown("---")
    
    # Strategic Action Plan
    enhanced = result.get("enhanced", False)
    sources = result.get("sources", [])
    
    if enhanced:
        st.markdown("#### 🤖 AI-Generated Strategic Recommendations")
        st.caption("📊 Research-backed insights from HubSpot, Sprout Social, Zendesk & Forrester")
    else:
        st.markdown("#### 🎯 Recommended Business Actions")
        st.caption("📊 Based on industry best practices from HubSpot, Sprout Social, Zendesk & Forrester")
    
    suggested_action = result.get("suggested_action", "No action suggested")
    
    # Style the action based on emotion category
    if dominant_emotion in negative_emotions:
        st.error(f"**Priority Action Required:**\n\n{suggested_action}")
    elif dominant_emotion in positive_emotions:
        st.success(f"**Opportunity to Leverage:**\n\n{suggested_action}")
    else:
        st.info(f"**Strategic Recommendation:**\n\n{suggested_action}")
    
    # Show research sources if enhanced mode
    if enhanced and sources:
        with st.expander("📚 Research Sources Used"):
            for source in sources:
                st.markdown(f"- **{source.get('title', 'Unknown')}** ({source.get('category', 'General')}) - Relevance: {source.get('relevance', 0):.0%}")
    elif not enhanced:
        with st.expander("📚 Data Sources"):
            st.markdown("""
            This recommendation is informed by publicly available research from:
            - **HubSpot** State of Marketing Report 2024
            - **Sprout Social** Index 2024
            - **Zendesk** Customer Experience Trends 2024
            - **Forrester** Customer Experience Research
            - **Hootsuite** Social Media Trends
            
            *All sources are freely available industry reports from trusted platforms.*
            """)
    
    # Show sources if enhanced mode was used
    if enhanced and sources:
        with st.expander("📚 Research Sources Used"):
            st.markdown("*These market research documents informed the recommendations:*")
            for i, source in enumerate(sources, 1):
                relevance = source.get("relevance", 0.0)
                st.markdown(f"{i}. **{source.get('title', 'Unknown')}** "
                          f"({source.get('category', 'General')}) "
                          f"- Relevance: {relevance:.0%}")



def render_emotional_summary_compact(result: dict):
    """
    Render a compact version of the emotional summary (for bulk analysis)
    
    Args:
        result: Dictionary containing summary, emotions, and reasoning
    """
    dominant_emotion = result["dominant_emotion"]
    confidence = result.get("confidence", 0.0)
    emoji = EMOJI_MAP.get(dominant_emotion, "🎭")
    
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #333; border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4>{emoji} {dominant_emotion.capitalize()} ({confidence:.0%})</h4>
            <p><strong>Summary:</strong> {result['summary'][:200]}...</p>
            <p><em>{result.get('reasoning', '')[:150]}...</em></p>
        </div>
        """, unsafe_allow_html=True)
