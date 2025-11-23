"""
Streamlit Component for Smart Emotional Summary Display
"""
import streamlit as st
from utils.labels import EMOJI_MAP


def render_emotional_summary(result: dict):
    """
    Render the Smart Emotional Summary in a beautiful Streamlit card
    
    Args:
        result: Dictionary containing summary, emotions, and reasoning
    """
    st.markdown("---")
    st.subheader("🧠 Smart Emotional Summary")
    
    # Summary Section
    st.markdown("#### 📌 Summary")
    if result["summary"].startswith("⚠️") or result["summary"].startswith("⏳"):
        st.warning(result["summary"])
    else:
        st.info(result["summary"])
    
    # Dominant Emotion Section
    st.markdown("#### 🎭 Dominant Emotion")
    
    dominant_emotion = result["dominant_emotion"]
    confidence = result.get("confidence", 0.0)
    emoji = EMOJI_MAP.get(dominant_emotion, "🎭")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"<div style='font-size: 4em; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**{dominant_emotion.capitalize()}**")
        st.progress(confidence)
        st.caption(f"Confidence: {confidence:.1%}")
    
    # Emotion Probability Breakdown
    st.markdown("#### 📊 Emotion Probability Breakdown")
    
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
                st.metric(
                    label=f"{emotion_emoji} {emotion.capitalize()}",
                    value=f"{prob:.1%}"
                )
        
        # Full breakdown in expander
        with st.expander("📋 View All Emotions"):
            emotion_df_data = {
                "Emotion": [f"{EMOJI_MAP.get(e, '🎭')} {e.capitalize()}" for e, _ in sorted_emotions],
                "Probability": [f"{p:.2%}" for _, p in sorted_emotions]
            }
            st.table(emotion_df_data)
    else:
        st.info("No emotion probabilities available")
    
    # Reasoning Section
    st.markdown("#### 💭 Emotion Reasoning")
    st.markdown(f"_{result.get('reasoning', 'No reasoning available')}_")
    
    # Detected Keywords
    keywords = result.get("detected_keywords", [])
    if keywords:
        st.markdown("**Detected Keywords:** " + ", ".join([f"`{kw}`" for kw in keywords]))
    
    # Suggested Action
    st.markdown("#### 💡 Suggested Action")
    suggested_action = result.get("suggested_action", "No action suggested")
    
    # Style the action based on emotion
    if dominant_emotion in ["anger", "fear", "sadness", "disappointment"]:
        st.error(suggested_action)
    elif dominant_emotion in ["joy", "excitement", "gratitude", "optimism"]:
        st.success(suggested_action)
    else:
        st.info(suggested_action)


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
