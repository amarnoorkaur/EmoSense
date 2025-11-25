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
                               crisis_flags: List[str] = None,
                               pain_point_clusters: List[Dict[str, Any]] = None,
                               root_causes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate dynamic business recommendation using LLM
        
        Args:
            summary: Text summary from BART
            dominant_emotion: Primary detected emotion
            all_emotions: All emotion probabilities
            confidence: Confidence level (0-1)
            research_context: Retrieved market research documents
            category_context: Optional post category detection results
            raw_comments: List of actual customer comments
            top_themes: Extracted keywords/themes from comments
            crisis_flags: Crisis keywords detected
            pain_point_clusters: Clustered customer feedback themes
            root_causes: Root cause analysis per cluster
            
        Returns:
            Dictionary with recommendation, reasoning, and sources
        """
        # Build prompt with all context including clusters and root causes
        prompt = self._build_prompt(
            summary=summary,
            dominant_emotion=dominant_emotion,
            all_emotions=all_emotions,
            confidence=confidence,
            research_context=research_context,
            category_context=category_context,
            raw_comments=raw_comments,
            top_themes=top_themes,
            crisis_flags=crisis_flags,
            pain_point_clusters=pain_point_clusters,
            root_causes=root_causes
        )
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert UX researcher + marketing strategist analyzing real customer feedback.

Your ONLY job: Generate hyper-specific, comment-grounded business recommendations using root cause analysis.

ABSOLUTE RULES:
1. EVERY recommendation must cite actual customer comments
2. NO generic advice (e.g., "improve UX", "enhance marketing")
3. NO suggestions outside what customers explicitly mentioned
4. Quote customer phrases verbatim when possible
5. Use pain point clusters to identify common themes
6. Apply root cause reasoning: Fix the WHY, not the WHAT
7. Mention cluster sizes and percentages when relevant (e.g., "28% of feedback relates to...")
8. Tie business impact directly to the specific customer pain AND its underlying cause

You are a data-driven analyst focused on root causes, NOT a textbook marketer."""
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
                     crisis_flags: List[str] = None,
                     pain_point_clusters: List[Dict[str, Any]] = None,
                     root_causes: List[Dict[str, Any]] = None) -> str:
        """
        Build hyper-specific, comment-grounded prompt with cluster and root cause analysis
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
        
        # Build pain point clusters section
        clusters_section = ""
        if pain_point_clusters and len(pain_point_clusters) > 0:
            clusters_section = "\n\n**🎯 PAIN POINT CLUSTERS (Grouped Customer Themes):**\n"
            for cluster in pain_point_clusters:
                cluster_id = cluster.get("cluster_id", "?")
                theme = cluster.get("theme_name", "Unknown Theme")
                size = cluster.get("size", 0)
                percentage = cluster.get("percentage", 0)
                keywords = cluster.get("theme_keywords", [])
                sentiment = cluster.get("sentiment_summary", {})
                examples = cluster.get("comment_examples", [])
                
                clusters_section += f"\n**Cluster {cluster_id}: {theme}** ({size} comments, {percentage:.1f}% of feedback)\n"
                clusters_section += f"  Keywords: {', '.join(keywords[:5])}\n"
                clusters_section += f"  Sentiment: {sentiment.get('dominant', 'neutral')} ({sentiment.get('positive', 0):.0%} positive, {sentiment.get('negative', 0):.0%} negative)\n"
                if examples:
                    clusters_section += f"  Example: \"{examples[0][:120]}...\"\n"
        
        # Build root causes section
        root_causes_section = ""
        if root_causes and len(root_causes) > 0:
            root_causes_section = "\n\n**🔬 ROOT CAUSE ANALYSIS (WHY Customers Feel This Way):**\n"
            for rc in root_causes:
                theme = rc.get("theme_name", "Unknown")
                cause = rc.get("root_cause", "Unknown cause")
                evidence = rc.get("evidence", [])
                action = rc.get("actionable_insight", "No action")
                
                root_causes_section += f"\n**{theme}:**\n"
                root_causes_section += f"  Root Cause: {cause[:200]}\n"
                if evidence:
                    root_causes_section += f"  Evidence: \"{evidence[0][:120]}...\"\n"
                root_causes_section += f"  Recommended Action: {action[:150]}\n"
        
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
{clusters_section}
{root_causes_section}
{crisis_section}
{research_section}

═══════════════════════════════════════════════════════════════
🎯 YOUR TASK: GENERATE HYPER-SPECIFIC RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

**CRITICAL INSTRUCTIONS:**

1. **USE PAIN POINT CLUSTERS (if provided):**
   - Reference clusters by name and percentage (e.g., "Cluster 2: Pricing Concerns (28% of feedback)")
   - Use clusters to identify patterns across multiple comments
   - Group recommendations by cluster themes when possible

2. **APPLY ROOT CAUSE REASONING (CRITICAL):**
   - Identify the WHY behind customer feelings, not just WHAT they said
   - Example: NOT "Users are confused" → YES "Users are confused BECAUSE onboarding doesn't explain pricing tiers"
   - Every recommendation must address the underlying cause
   - Reference root causes provided in the analysis above

3. **ONLY recommend things DIRECTLY mentioned in the comments above**
   - If no one mentioned "dark mode", DO NOT suggest it
   - If no one mentioned bugs, DO NOT suggest fixing bugs
   - Every recommendation MUST tie to actual customer words

4. **Identify REAL issues from the comments:**
   - Bugs/crashes (quote the error descriptions)
   - UI confusion (quote confusing parts)
   - Feature requests (quote exactly what they asked for)
   - Pricing complaints (quote their concerns)
   - Emotional patterns (reference specific comments showing frustration/joy)

5. **For EACH recommendation, you MUST include:**
   ✅ Direct quote(s) from actual comments
   ✅ How many commenters mentioned this (if >1) OR cluster percentage
   ✅ Root cause analysis (WHY this is happening)
   ✅ Specific action step targeting the root cause (not symptom)
   ✅ Expected impact tied to fixing the underlying cause

6. **GROUP similar comments by theme or use provided clusters:**
   Examples:
   - "Product Quality Issues" (if multiple mention defects)
   - "App Performance Problems" (if multiple mention crashes)
   - "Feature Requests" (if multiple request same thing)
   - "Onboarding Confusion" (if multiple don't understand something)
   OR use the pain point clusters provided above

7. **Use this EXACT format for each recommendation:**

---
### Issue [number]: [Specific Problem from Comments]
*[If using clusters: Cluster X: Theme Name (Y% of feedback)]*

**Evidence from Comments:**
- "quote 1"
- "quote 2"
- "quote 3"
[Mention frequency: "X commenters mentioned this" OR "Z% of feedback"]

**Root Cause Analysis (WHY this is happening):**
[Identify the underlying cause - not just symptoms]
[Reference root cause from analysis if provided]

**Recommended Action (targeting root cause):**
1. [Specific step 1 - fixes the WHY, not the WHAT]
2. [Specific step 2 - addresses underlying issue]

**Expected Impact:**
[How fixing the ROOT CAUSE helps your business]
---

8. **ABSOLUTELY FORBIDDEN:**
   ❌ "Improve user experience" (too vague)
   ❌ "Enhance marketing strategy" (not tied to comments)
   ❌ "Add more features" (which features? who asked?)
   ❌ "Optimize performance" (unless crashes were mentioned)
   ❌ ANY suggestion not backed by actual comment content
   ❌ Fixing symptoms without addressing root causes

9. **CRISIS HANDLING:**
   If crisis keywords detected, add this section FIRST:
   
---
### 🚨 URGENT: Crisis Issues Detected

**Critical Comments:**
[Quote the angry/legal/refund comments]

**Immediate Action Required:**
[Specific crisis response - refund flow, apology messaging, etc.]
---

10. **TONE:** Professional UX researcher. Data-driven. Specific. Brief.

11. **DELIVERABLE:** Provide 3-5 recommendations (fewer if comments are limited).

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
