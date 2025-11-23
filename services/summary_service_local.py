"""
Alternative Smart Emotional Summary Service - Uses local transformers
This version loads the model locally instead of using the deprecated API
"""
import re
from functools import lru_cache
from typing import Dict, Any, Optional
import streamlit as st

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from services.summary_service import (
    EMOTION_KEYWORDS,
    EMOTION_ACTIONS,
    clean_text,
    validate_text_for_summary,
    generate_emotion_reasoning,
    extract_emotion_keywords
)

# Initialize summarization pipeline (cached)
@st.cache_resource
def load_summarization_model():
    """Load BART summarization model locally"""
    if not TRANSFORMERS_AVAILABLE:
        return None
    
    try:
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1  # CPU only
        )
        return summarizer
    except Exception as e:
        st.error(f"Failed to load summarization model: {e}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def summarize_text_local(text: str) -> str:
    """
    Generate summary using local transformers model
    
    Args:
        text: Input text to summarize
        
    Returns:
        Generated summary or error message
    """
    # Clean text
    cleaned_text = clean_text(text)
    
    # Validate text
    is_valid, error_msg = validate_text_for_summary(cleaned_text)
    if not is_valid:
        return f"⚠️ {error_msg}"
    
    # Check if transformers is available
    if not TRANSFORMERS_AVAILABLE:
        return "⚠️ Transformers library not available. Please install: pip install transformers"
    
    try:
        # Load model
        summarizer = load_summarization_model()
        if summarizer is None:
            return "⚠️ Failed to load summarization model"
        
        # Generate summary
        with st.spinner("Generating summary..."):
            result = summarizer(
                cleaned_text,
                max_length=130,
                min_length=30,
                do_sample=False
            )
        
        if result and len(result) > 0:
            summary = result[0].get("summary_text", "")
            return summary if summary else "Unable to generate summary"
        
        return "No summary generated"
    
    except Exception as e:
        return f"⚠️ Error generating summary: {str(e)[:150]}"


def combine_emotion_and_summary(emotion_output: Dict[str, Any], summary: str, original_text: str) -> Dict[str, Any]:
    """
    Combine emotion analysis with summary to create intelligent output
    
    Args:
        emotion_output: Dictionary containing emotion predictions
        summary: Generated text summary
        original_text: Original input text for context
        
    Returns:
        Structured dictionary with combined insights
    """
    # Extract dominant emotion
    all_emotions = emotion_output.get("probabilities", {})
    
    if all_emotions:
        dominant_emotion = max(all_emotions.items(), key=lambda x: x[1])[0]
    else:
        dominant_emotion = "neutral"
    
    # Generate reasoning
    reasoning = generate_emotion_reasoning(summary, dominant_emotion, all_emotions)
    
    # Get suggested action
    suggested_action = EMOTION_ACTIONS.get(
        dominant_emotion, 
        "💭 **Reflect**: Take a moment to understand your emotional state and respond accordingly."
    )
    
    # Create combined result
    result = {
        "summary": summary,
        "dominant_emotion": dominant_emotion,
        "all_emotions": all_emotions,
        "reasoning": reasoning,
        "suggested_action": suggested_action,
        "confidence": all_emotions.get(dominant_emotion, 0.0),
        "detected_keywords": extract_emotion_keywords(original_text, dominant_emotion)
    }
    
    return result
