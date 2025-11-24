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
    """Load BART summarization model locally - only when needed"""
    if not TRANSFORMERS_AVAILABLE:
        return None
    
    try:
        # Only load if explicitly needed
        import os
        if os.getenv("DISABLE_BART_MODEL", "true").lower() == "true":
            print("⚠️ BART model disabled to save memory. Using fallback summarization.")
            return None
            
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1  # CPU only
        )
        return summarizer
    except Exception as e:
        print(f"⚠️ Failed to load summarization model: {e}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def summarize_text_local(text: str) -> str:
    """
    Generate summary using local transformers model or fallback
    
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
        # Fallback: return a simple extractive summary
        sentences = cleaned_text.split('. ')
        if len(sentences) <= 3:
            return cleaned_text
        return '. '.join(sentences[:3]) + '...'
    
    try:
        # Load model
        summarizer = load_summarization_model()
        if summarizer is None:
            # Fallback: return extractive summary
            sentences = cleaned_text.split('. ')
            if len(sentences) <= 3:
                return cleaned_text
            return '. '.join(sentences[:3]) + '...'
        
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


def combine_emotion_and_summary(emotion_output: Dict[str, Any], 
                               summary: str, 
                               original_text: str,
                               use_enhanced_ai: bool = False,
                               category_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Combine emotion analysis with summary to create intelligent output
    
    Args:
        emotion_output: Dictionary containing emotion predictions
        summary: Generated text summary
        original_text: Original input text for context
        use_enhanced_ai: Whether to use LLM-powered recommendations (default: False)
        category_context: Optional category detection results for context-aware insights
        
    Returns:
        Structured dictionary with combined insights
    """
    # Add category to output if provided
    result_base = {
        "summary": summary,
        "emotions": emotion_output.get("probabilities", {}),
        "category": category_context if category_context else None
    }
    # Extract dominant emotion
    all_emotions = emotion_output.get("probabilities", {})
    
    if all_emotions:
        dominant_emotion = max(all_emotions.items(), key=lambda x: x[1])[0]
    else:
        dominant_emotion = "neutral"
    
    # Generate reasoning
    reasoning = generate_emotion_reasoning(summary, dominant_emotion, all_emotions)
    
    # Get suggested action (static or enhanced)
    if use_enhanced_ai:
        # Try to use enhanced AI recommendations
        try:
            from services.rag_service import get_rag_service, initialize_rag_with_defaults
            from services.llm_recommendation_service import get_llm_service
            
            # Initialize RAG and retrieve relevant research
            rag = initialize_rag_with_defaults()
            research_context = rag.search_relevant_research(
                query=summary,
                emotion=dominant_emotion,
                n_results=3
            )
            
            # Generate LLM recommendation with category context
            llm_service = get_llm_service()
            if llm_service:
                llm_result = llm_service.generate_recommendation(
                    summary=summary,
                    dominant_emotion=dominant_emotion,
                    all_emotions=all_emotions,
                    confidence=all_emotions.get(dominant_emotion, 0.0),
                    research_context=research_context,
                    category_context=category_context
                )
                
                suggested_action = llm_result.get("recommendation", "")
                enhanced = True
                sources = llm_result.get("sources", [])
            else:
                # Fallback to static
                suggested_action = EMOTION_ACTIONS.get(dominant_emotion, 
                    "💭 **Reflect**: Take a moment to understand your emotional state and respond accordingly.")
                enhanced = False
                sources = []
        
        except Exception as e:
            # Fallback to static on any error
            print(f"Enhanced AI failed, using static: {e}")
            suggested_action = EMOTION_ACTIONS.get(dominant_emotion, 
                "💭 **Reflect**: Take a moment to understand your emotional state and respond accordingly.")
            enhanced = False
            sources = []
    else:
        # Use static recommendations
        suggested_action = EMOTION_ACTIONS.get(
            dominant_emotion, 
            "💭 **Reflect**: Take a moment to understand your emotional state and respond accordingly."
        )
        enhanced = False
        sources = []
    
    # Create combined result
    result = {
        "summary": summary,
        "dominant_emotion": dominant_emotion,
        "all_emotions": all_emotions,
        "reasoning": reasoning,
        "suggested_action": suggested_action,
        "confidence": all_emotions.get(dominant_emotion, 0.0),
        "detected_keywords": extract_emotion_keywords(original_text, dominant_emotion),
        "enhanced": enhanced,
        "sources": sources
    }
    
    return result
