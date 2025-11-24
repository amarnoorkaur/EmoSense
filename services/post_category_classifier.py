"""
Context-Aware Post Category Classifier
Uses zero-shot classification to detect content type for adaptive insights
"""
import streamlit as st
from typing import Dict, List, Optional

# Categories for classification
POST_CATEGORIES = [
    "Product Review",
    "Service Complaint",
    "Customer Support Query",
    "General Feedback",
    "Marketing Content",
    "Technical Issue",
    "Feature Request",
    "Testimonial",
    "Experience Sharing"
]

# Category-specific emojis
CATEGORY_EMOJIS = {
    "Product Review": "⭐",
    "Service Complaint": "😤",
    "Customer Support Query": "🙋",
    "General Feedback": "💬",
    "Marketing Content": "📢",
    "Technical Issue": "🔧",
    "Feature Request": "💡",
    "Testimonial": "💖",
    "Experience Sharing": "📖"
}

# Category-specific colors for UI
CATEGORY_COLORS = {
    "Product Review": "#FFD700",
    "Service Complaint": "#FF6B6B",
    "Customer Support Query": "#4ECDC4",
    "General Feedback": "#95E1D3",
    "Marketing Content": "#A8E6CF",
    "Technical Issue": "#FF8B94",
    "Feature Request": "#C7CEEA",
    "Testimonial": "#FFC8DD",
    "Experience Sharing": "#FFAFCC"
}


@st.cache_resource
def load_classifier():
    """Load zero-shot classification pipeline"""
    try:
        from transformers import pipeline
        
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1  # CPU only
        )
        return classifier
    except Exception as e:
        print(f"⚠️ Failed to load classifier: {e}")
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def detect_post_category(text: str, top_k: int = 1) -> Dict:
    """
    Detect the category of a post using zero-shot classification
    
    Args:
        text: Input text to classify
        top_k: Number of top predictions to return (default: 1)
        
    Returns:
        dict with:
            - category: predicted label
            - confidence: confidence score (0-1)
            - all_scores: list of all category scores (if top_k > 1)
    """
    # Input validation
    if not text or len(text.strip()) < 10:
        return {
            "category": "General Feedback",
            "confidence": 0.5,
            "all_scores": []
        }
    
    # Load classifier
    classifier = load_classifier()
    
    # Fallback if classifier not available
    if classifier is None:
        # Simple keyword-based fallback
        return _fallback_classification(text)
    
    try:
        # Run zero-shot classification
        result = classifier(
            text[:512],  # Limit input length
            candidate_labels=POST_CATEGORIES,
            multi_label=False
        )
        
        # Parse results
        category = result['labels'][0]
        confidence = result['scores'][0]
        
        response = {
            "category": category,
            "confidence": float(confidence),
            "all_scores": []
        }
        
        # Add all scores if requested
        if top_k > 1:
            response["all_scores"] = [
                {
                    "category": label,
                    "confidence": float(score)
                }
                for label, score in zip(result['labels'][:top_k], result['scores'][:top_k])
            ]
        
        return response
        
    except Exception as e:
        print(f"⚠️ Classification error: {e}")
        return _fallback_classification(text)


def _fallback_classification(text: str) -> Dict:
    """
    Simple keyword-based fallback classification
    
    Args:
        text: Input text to classify
        
    Returns:
        dict with category and confidence
    """
    text_lower = text.lower()
    
    # Keyword patterns for each category
    keywords = {
        "Product Review": ["product", "quality", "recommend", "stars", "rating", "bought", "purchase"],
        "Service Complaint": ["disappointed", "terrible", "worst", "poor service", "complaint", "unacceptable"],
        "Customer Support Query": ["help", "support", "how do i", "question", "assistance", "issue", "problem"],
        "General Feedback": ["think", "opinion", "feel", "believe", "suggest"],
        "Marketing Content": ["announcement", "launch", "new", "exclusive", "offer", "deal"],
        "Technical Issue": ["bug", "error", "crash", "not working", "broken", "fix", "technical"],
        "Feature Request": ["would be nice", "please add", "feature", "suggestion", "could you"],
        "Testimonial": ["love", "amazing", "best", "changed my life", "grateful", "thank you"],
        "Experience Sharing": ["my experience", "i tried", "story", "journey", "happened"]
    }
    
    # Count keyword matches
    scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in text_lower)
        scores[category] = score
    
    # Get top category
    if max(scores.values()) > 0:
        category = max(scores, key=scores.get)
        confidence = min(0.7, 0.4 + (scores[category] * 0.1))
    else:
        category = "General Feedback"
        confidence = 0.5
    
    return {
        "category": category,
        "confidence": confidence,
        "all_scores": []
    }


def get_category_emoji(category: str) -> str:
    """Get emoji for a category"""
    return CATEGORY_EMOJIS.get(category, "📝")


def get_category_color(category: str) -> str:
    """Get color for a category"""
    return CATEGORY_COLORS.get(category, "#95E1D3")


def get_category_specific_prompt_addition(category: str) -> str:
    """
    Get category-specific additions for LLM prompts
    
    Args:
        category: The detected category
        
    Returns:
        String with category-specific guidance
    """
    prompts = {
        "Product Review": "Focus on product performance, quality, and value. Highlight specific features mentioned.",
        "Service Complaint": "Prioritize service quality issues, frustration points, and urgency. Suggest resolution steps.",
        "Customer Support Query": "Identify the specific help needed. Provide clear, actionable solutions.",
        "General Feedback": "Extract overall sentiment and key opinions. Identify actionable insights.",
        "Marketing Content": "Analyze audience emotional response and engagement potential. Identify resonating themes.",
        "Technical Issue": "Identify technical problems, severity, and impact. Suggest troubleshooting priorities.",
        "Feature Request": "Extract desired features and use cases. Assess demand and feasibility indicators.",
        "Testimonial": "Highlight success stories, transformative impact, and advocacy potential.",
        "Experience Sharing": "Extract journey insights, pain points, and emotional touchpoints."
    }
    
    return prompts.get(category, "Provide relevant business insights.")
