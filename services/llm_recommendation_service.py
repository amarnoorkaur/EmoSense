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
                               category_context: Dict[str, Any] = None,
                               raw_comments: List[str] = None,
                               top_themes: List[str] = None,
                               crisis_flags: List[str] = None) -> Dict[str, Any]:
        """
        Generate dynamic business recommendation using LLM
        
        Args:
            summary: Text summary from BART
            dominant_emotion: Primary detected emotion
            all_emotions: All emotion probabilities
            confidence: Confidence level (0-1)
            research_context: Retrieved market research documents
            category_context: Optional post category detection results
            raw_comments: List of actual customer comments (NEW)
            top_themes: Extracted keywords/themes from comments (NEW)
            crisis_flags: Crisis keywords detected (NEW)
            
        Returns:
            Dictionary with recommendation, reasoning, and sources
        """
        # Build prompt with all context including raw comments
        prompt = self._build_prompt(
            summary=summary,
            dominant_emotion=dominant_emotion,
            all_emotions=all_emotions,
            confidence=confidence,
            research_context=research_context,
            category_context=category_context,
            raw_comments=raw_comments,
            top_themes=top_themes,
            crisis_flags=crisis_flags
        )
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert UX researcher + marketing strategist analyzing real customer feedback.

Your ONLY job: Generate hyper-specific, comment-grounded business recommendations.

ABSOLUTE RULES:
1. EVERY recommendation must cite actual customer comments
2. NO generic advice (e.g., "improve UX", "enhance marketing")
3. NO suggestions outside what customers explicitly mentioned
4. Quote customer phrases verbatim when possible
5. Mention frequency when relevant (e.g., "6 commenters requested...")
6. Tie business impact directly to the specific customer pain

You are a data-driven analyst, NOT a textbook marketer."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,  # Lower for more focused output
                max_tokens=700  # More space for detailed evidence
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
                     category_context: Dict[str, Any] = None,
                     raw_comments: List[str] = None,
                     top_themes: List[str] = None,
                     crisis_flags: List[str] = None) -> str:
        """
        Build hyper-specific, comment-grounded prompt
        """
        """
        Build hyper-specific, comment-grounded prompt
        """
        # Categorize emotions
        positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
        negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
        
        sentiment_category = "Positive" if dominant_emotion in positive_emotions else \
                            "Negative" if dominant_emotion in negative_emotions else "Neutral/Mixed"
        
        # Get top 5 emotions with counts
        top_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)[:5]
        emotions_list = "\n".join([f"  - {e.capitalize()}: {p:.1%}" for e, p in top_emotions])
        
        # Build ACTUAL COMMENTS section
        comments_section = ""
        if raw_comments and len(raw_comments) > 0:
            # Limit to first 20 comments to avoid token overflow
            comment_sample = raw_comments[:20]
            comments_section = f"\n\n**📝 ACTUAL CUSTOMER COMMENTS ({len(comment_sample)} shown, {len(raw_comments)} total):**\n"
            for i, comment in enumerate(comment_sample, 1):
                # Truncate very long comments
                comment_text = comment[:200] + "..." if len(comment) > 200 else comment
                comments_section += f'{i}. "{comment_text}"\n'
        
        # Build themes section
        themes_section = ""
        if top_themes and len(top_themes) > 0:
            themes_section = f"\n\n**🔍 EXTRACTED THEMES:** {', '.join(top_themes[:10])}"
        
        # Build crisis section
        crisis_section = ""
        if crisis_flags and len(crisis_flags) > 0:
            crisis_section = f"\n\n**🚨 CRISIS KEYWORDS DETECTED:** {', '.join(set(crisis_flags))}"
        
        # Add category context if available
        category_section = ""
        if category_context:
            category = category_context.get("category", "Unknown")
            cat_confidence = category_context.get("confidence", 0.0)
            category_section = f"\n**Content Category:** {category} ({cat_confidence:.0%} confidence)"
        
        # Build research context section (shortened)
        research_section = ""
        if research_context and len(research_context) > 0:
            research_section = "\n\n**📚 Relevant Market Research (for context only):**\n"
            for i, doc in enumerate(research_context[:2], 1):  # Only 2 docs
                source = doc["metadata"].get("filename", "Unknown source")
                research_section += f"{i}. {source}\n"
        
        prompt = f"""
═══════════════════════════════════════════════════════════════
🎯 CUSTOMER FEEDBACK ANALYSIS - COMMENT-GROUNDED RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

**📊 EMOTIONAL ANALYSIS:**
- Overall Sentiment: {sentiment_category}
- Dominant Emotion: {dominant_emotion.capitalize()} ({confidence:.0%} confidence)
- Top Emotions Detected:
{emotions_list}

**📝 SUMMARY OF COMMENT THREAD:**
{summary}
{category_section}
{comments_section}
{themes_section}
{crisis_section}
{research_section}

═══════════════════════════════════════════════════════════════
🎯 YOUR TASK: GENERATE HYPER-SPECIFIC RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

**CRITICAL INSTRUCTIONS:**

1. **ONLY recommend things DIRECTLY mentioned in the comments above**
   - If no one mentioned "dark mode", DO NOT suggest it
   - If no one mentioned bugs, DO NOT suggest fixing bugs
   - Every recommendation MUST tie to actual customer words

2. **Identify REAL issues from the comments:**
   - Bugs/crashes (quote the error descriptions)
   - UI confusion (quote confusing parts)
   - Feature requests (quote exactly what they asked for)
   - Pricing complaints (quote their concerns)
   - Emotional patterns (reference specific comments showing frustration/joy)

3. **For EACH recommendation, you MUST include:**
   ✅ Direct quote(s) from actual comments
   ✅ How many commenters mentioned this (if >1)
   ✅ Why this matters (root cause analysis)
   ✅ Specific action step (not generic advice)
   ✅ Expected impact tied to that exact issue

4. **GROUP similar comments by theme:**
   Examples:
   - "Product Quality Issues" (if multiple mention defects)
   - "App Performance Problems" (if multiple mention crashes)
   - "Feature Requests" (if multiple request same thing)
   - "Onboarding Confusion" (if multiple don't understand something)

5. **Use this EXACT format for each recommendation:**

---
### Issue [number]: [Specific Problem from Comments]

**Evidence from Comments:**
- "quote 1"
- "quote 2"
- "quote 3"
[Mention frequency: "X commenters mentioned this"]

**Why This Matters:**
[Root cause - what's actually broken/missing]

**Recommended Action:**
1. [Specific step 1 - NOT generic]
2. [Specific step 2 - NOT generic]

**Expected Impact:**
[How fixing THIS exact issue helps your business]
---

6. **ABSOLUTELY FORBIDDEN:**
   ❌ "Improve user experience" (too vague)
   ❌ "Enhance marketing strategy" (not tied to comments)
   ❌ "Add more features" (which features? who asked?)
   ❌ "Optimize performance" (unless crashes were mentioned)
   ❌ ANY suggestion not backed by actual comment content

7. **CRISIS HANDLING:**
   If crisis keywords detected, add this section FIRST:
   
---
### 🚨 URGENT: Crisis Issues Detected

**Critical Comments:**
[Quote the angry/legal/refund comments]

**Immediate Action Required:**
[Specific crisis response - refund flow, apology messaging, etc.]
---

8. **TONE:** Professional UX researcher. Data-driven. Specific. Brief.

9. **DELIVERABLE:** Provide 3-5 recommendations (fewer if comments are limited).

═══════════════════════════════════════════════════════════════

Now analyze the ACTUAL comments above and generate hyper-specific, evidence-backed recommendations.
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
