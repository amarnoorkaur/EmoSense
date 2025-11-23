"""
Smart Emotional Summary Service
Uses Hugging Face BART model for text summarization combined with emotion analysis
"""
import os
import re
import requests
from functools import lru_cache
from typing import Dict, Any, Optional
import streamlit as st

# Hugging Face API Configuration
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
HF_API_URL = f"https://api-inference.huggingface.co/models/{SUMMARIZATION_MODEL}"

# Emotion-based reasoning patterns
EMOTION_KEYWORDS = {
    "anger": ["delay", "frustration", "annoying", "irritating", "upset", "furious", "angry", "mad"],
    "sadness": ["lonely", "tired", "overwhelmed", "depressed", "sad", "unhappy", "miserable", "hopeless"],
    "joy": ["happy", "excited", "great", "wonderful", "amazing", "love", "fantastic", "delighted"],
    "fear": ["worried", "anxious", "scared", "nervous", "terrified", "panic", "afraid"],
    "confusion": ["confused", "unclear", "don't understand", "puzzled", "uncertain", "perplexed"],
    "disappointment": ["disappointed", "let down", "failed", "unmet expectations", "dissatisfied"]
}

# Suggested actions based on emotions
EMOTION_ACTIONS = {
    "anger": "🔥 **De-escalation Recommended**: Take a deep breath, step away if possible, and address the issue when calm.",
    "sadness": "🌱 **Grounding Exercise**: Practice mindfulness, reach out to support networks, or engage in self-care activities.",
    "joy": "✨ **Positive Reinforcement**: Celebrate this moment! Share your happiness and acknowledge what went well.",
    "fear": "🛡️ **Reassurance Needed**: Identify specific concerns, gather information, and create an action plan.",
    "confusion": "💡 **Clarification Required**: Break down the issue into smaller parts, ask questions, and seek clear explanations.",
    "disappointment": "🔄 **Reflection & Reset**: Acknowledge the feeling, learn from the experience, and set new realistic goals.",
    "excitement": "🎉 **Channel Energy**: Use this momentum productively and share your enthusiasm with others.",
    "nervousness": "🧘 **Calm & Prepare**: Practice relaxation techniques and focus on preparation rather than worry.",
    "optimism": "🌟 **Maintain Momentum**: Keep this positive outlook and use it to inspire action and perseverance.",
    "gratitude": "🙏 **Express Appreciation**: Share your gratitude with others and reflect on what you're thankful for.",
    "neutral": "⚖️ **Balanced State**: Continue with your current approach and monitor for any emotional shifts."
}


def clean_text(text: str) -> str:
    """
    Clean and prepare text for summarization
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_text_for_summary(text: str) -> tuple[bool, str]:
    """
    Validate if text is suitable for summarization
    
    Args:
        text: Input text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text:
        return False, "Text cannot be empty"
    
    word_count = len(text.split())
    
    if word_count < 10:
        return False, "Text too short for meaningful summary (minimum 10 words required)"
    
    if word_count > 1024:
        # BART has token limits
        return False, "Text too long for summarization (maximum ~1000 words)"
    
    return True, ""


@st.cache_data(ttl=3600, show_spinner=False)
def summarize_text(text: str) -> str:
    """
    Generate summary using Hugging Face BART model
    
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
    
    # Check API key
    if not HF_API_KEY:
        return "⚠️ Hugging Face API key not configured. Please set HUGGINGFACE_API_KEY environment variable."
    
    try:
        # Prepare API request
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {
            "inputs": cleaned_text,
            "parameters": {
                "max_length": 130,
                "min_length": 30,
                "do_sample": False
            }
        }
        
        # Call Hugging Face API
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                summary = result[0].get("summary_text", "")
                return summary if summary else "Unable to generate summary"
            return "Unexpected response format from API"
        
        elif response.status_code == 503:
            return "⏳ Model is loading, please try again in a moment (this can take 20-30 seconds for cold start)"
        
        elif response.status_code == 401:
            return "⚠️ Invalid API key. Please check your HUGGINGFACE_API_KEY"
        
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text[:100]}"
    
    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. The model may be overloaded, please try again."
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {str(e)[:100]}"
    
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)[:100]}"


def generate_emotion_reasoning(summary: str, dominant_emotion: str, all_emotions: dict) -> str:
    """
    Generate intelligent reasoning for why certain emotions were detected
    
    Args:
        summary: Text summary
        dominant_emotion: Primary detected emotion
        all_emotions: Dictionary of all emotion probabilities
        
    Returns:
        Reasoning explanation string
    """
    reasoning_parts = []
    
    # Check if summary contains emotion-related keywords
    summary_lower = summary.lower()
    matched_keywords = []
    
    if dominant_emotion in EMOTION_KEYWORDS:
        for keyword in EMOTION_KEYWORDS[dominant_emotion]:
            if keyword in summary_lower:
                matched_keywords.append(keyword)
    
    # Build reasoning
    confidence = all_emotions.get(dominant_emotion, 0)
    
    if matched_keywords:
        keywords_str = ", ".join([f"'{kw}'" for kw in matched_keywords[:3]])
        reasoning_parts.append(f"The text contains language suggesting {dominant_emotion} ({keywords_str})")
    
    if confidence > 0.8:
        reasoning_parts.append(f"Strong confidence ({confidence:.0%}) in {dominant_emotion} detection")
    elif confidence > 0.5:
        reasoning_parts.append(f"Moderate confidence ({confidence:.0%}) indicates {dominant_emotion}")
    else:
        reasoning_parts.append(f"Detected {dominant_emotion} with {confidence:.0%} confidence")
    
    # Check for secondary emotions
    sorted_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_emotions) > 1:
        secondary = sorted_emotions[1]
        if secondary[1] > 0.3:
            reasoning_parts.append(f"Secondary emotion of {secondary[0]} ({secondary[1]:.0%}) also present")
    
    return ". ".join(reasoning_parts) + "."


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


def extract_emotion_keywords(text: str, emotion: str) -> list:
    """
    Extract emotion-related keywords from text
    
    Args:
        text: Input text
        emotion: Target emotion
        
    Returns:
        List of matched keywords
    """
    if emotion not in EMOTION_KEYWORDS:
        return []
    
    text_lower = text.lower()
    matched = []
    
    for keyword in EMOTION_KEYWORDS[emotion]:
        if keyword in text_lower:
            matched.append(keyword)
    
    return matched[:5]  # Return top 5 matches
