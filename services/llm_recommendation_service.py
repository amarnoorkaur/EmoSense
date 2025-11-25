"""
LLM-Powered Recommendation Service
Generates dynamic, context-aware business recommendations using OpenAI
"""
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
import streamlit as st


class LLMRecommendationService:
    """
    Service for generating AI-powered business recommendations
    based on emotion analysis and market research context
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Cost-effective, fast
    
    def generate_recommendation(self,
                               summary: str,
                               dominant_emotion: str,
                               all_emotions: Dict[str, float],
                               confidence: float,
                               research_context: List[Dict[str, Any]] = None,
                               category_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate dynamic business recommendation using LLM
        
        Args:
            summary: Text summary from BART
            dominant_emotion: Primary detected emotion
            all_emotions: All emotion probabilities
            confidence: Confidence level (0-1)
            research_context: Retrieved market research documents
            category_context: Optional post category detection results
            
        Returns:
            Dictionary with recommendation, reasoning, and sources
        """
        # Build prompt with category context
        prompt = self._build_prompt(
            summary=summary,
            dominant_emotion=dominant_emotion,
            all_emotions=all_emotions,
            confidence=confidence,
            research_context=research_context,
            category_context=category_context
        )
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert social media strategist and customer sentiment analyst. 
                        Generate actionable business recommendations based on customer emotion analysis and market research. 
                        Be specific, data-driven, and practical. Focus on ROI and measurable outcomes."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            recommendation_text = response.choices[0].message.content.strip()
            
            # Extract sources used
            sources = []
            if research_context:
                sources = [
                    {
                        "title": doc["metadata"].get("filename", "Unknown"),
                        "category": doc["metadata"].get("category", "General"),
                        "relevance": doc.get("relevance_score", 0.0)
                    }
                    for doc in research_context
                ]
            
            return {
                "recommendation": recommendation_text,
                "enhanced": True,
                "sources": sources,
                "model": self.model,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
        
        except Exception as e:
            # Return error info for debugging
            return {
                "recommendation": f"⚠️ AI recommendation unavailable: {str(e)}",
                "enhanced": False,
                "sources": [],
                "error": str(e)
            }
    
    def _build_prompt(self,
                     summary: str,
                     dominant_emotion: str,
                     all_emotions: Dict[str, float],
                     confidence: float,
                     research_context: List[Dict[str, Any]],
                     category_context: Dict[str, Any] = None) -> str:
        """
        Build the LLM prompt with all context including category
        """
        # Categorize emotions
        positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
        negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
        
        sentiment_category = "Positive" if dominant_emotion in positive_emotions else \
                            "Negative" if dominant_emotion in negative_emotions else "Neutral/Mixed"
        
        # Get top 3 emotions
        top_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        top_emotions_str = ", ".join([f"{e.capitalize()} ({p:.0%})" for e, p in top_emotions])
        
        # Add category context if available
        category_section = ""
        if category_context:
            category = category_context.get("category", "Unknown")
            cat_confidence = category_context.get("confidence", 0.0)
            category_section = f"\n**Content Category:** {category} ({cat_confidence:.0%} confidence)"
            
            # Add category-specific guidance
            from services.post_category_classifier import get_category_specific_prompt_addition
            category_guidance = get_category_specific_prompt_addition(category)
            category_section += f"\n**Analysis Focus:** {category_guidance}"
        
        # Build research context section
        research_section = ""
        if research_context and len(research_context) > 0:
            research_section = "\n\n**Relevant Market Research Context:**\n"
            for i, doc in enumerate(research_context[:3], 1):
                content_preview = doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"]
                source = doc["metadata"].get("filename", "Unknown source")
                research_section += f"\n{i}. From '{source}':\n{content_preview}\n"
        
        prompt = f"""
**Customer Feedback Analysis:**

**Summary of Comment Thread:** {summary}
{category_section}

**Emotional Analysis:**
- Overall Sentiment: {sentiment_category}
- Dominant Emotion: {dominant_emotion.capitalize()} ({confidence:.0%} confidence)
- Top Emotions: {top_emotions_str}

{research_section}

**Your Task:**
Analyze the comment thread summary above and generate strategic business recommendations that DIRECTLY address the specific issues, complaints, praises, or requests mentioned in the comment thread.

**CRITICAL INSTRUCTIONS:**
- Base ALL recommendations on ACTUAL content from the comment thread
- If commenters mention specific problems (e.g., bugs, pricing, features), address THOSE specific issues
- If commenters praise specific aspects, recommend ways to amplify THOSE strengths
- DO NOT suggest generic improvements unrelated to the actual comment thread
- Quote or reference specific themes from the comment thread

**Required Output Format:**

1. **Key Insight** (What are commenters actually saying? What specific patterns or themes emerge from their comments?)

2. **Recommended Actions** (3-5 specific steps that directly address the issues or opportunities mentioned in the comment thread)
   - Each action should reference a specific commenter concern or praise from the thread
   - Be actionable and specific, not generic

3. **Expected Impact** (How will addressing these specific commenter concerns improve your business?)

Be concise, professional, and laser-focused on the ACTUAL comment thread content.
"""
        
        return prompt


@st.cache_resource
def get_llm_service():
    """
    Get cached LLM recommendation service instance
    
    Returns:
        LLMRecommendationService instance
    """
    try:
        return LLMRecommendationService()
    except ValueError as e:
        st.warning(f"⚠️ LLM service unavailable: {e}")
        return None
