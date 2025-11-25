"""
🤝 Business Buddy: Your brand therapist
Full-featured business analytics with conversational AI

Features:
- Single comment thread or CSV batch analysis
- Emotion detection (BERT)
- Summarization (BART)
- RAG-powered insights
- Sentiment breakdown
- Crisis detection
- Conversational chat interface
- Full business report export
"""
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Components
from components.layout import (
    set_page_config, 
    inject_global_styles, 
    page_container,
    gradient_hero,
    spacer
)
from components.footer import render_footer

# Core services
from utils.predict import predict_emotions
from utils.labels import EMOTIONS, EMOJI_MAP

# Summarization
try:
    from services.summary_service_local import summarize_text_local, combine_emotion_and_summary
    USE_LOCAL_SUMMARY = True
except:
    from services.summary_service import summarize_text, combine_emotion_and_summary
    USE_LOCAL_SUMMARY = False

# RAG and LLM services
try:
    from services.rag_service import initialize_rag_with_defaults
    from services.llm_recommendation_service import get_llm_service
    RAG_AVAILABLE = True
except Exception as e:
    RAG_AVAILABLE = False

# Pain point clustering and root cause analysis
try:
    from services.clustering_service import cluster_comments
    CLUSTERING_AVAILABLE = True
except Exception as e:
    CLUSTERING_AVAILABLE = False
    print(f"Clustering unavailable: {e}")

try:
    from services.root_cause_engine import get_root_cause_engine
    ROOT_CAUSE_AVAILABLE = True
except Exception as e:
    ROOT_CAUSE_AVAILABLE = False
    print(f"Root cause engine unavailable: {e}")

# OpenAI for chat
from openai import OpenAI

# Configure
set_page_config()
inject_global_styles()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "business_chat_history": [],
        "analysis_raw_comments": [],
        "analysis_emotions": {},
        "analysis_summary": "",
        "analysis_insights": {},
        "analysis_sentiments": {},
        "analysis_complete": False,
        "crisis_alerts": [],
        # New: Persistent chat context
        "chat_context_built": False,
        "chat_system_prompt": "",
        "extracted_themes": [],
        "extracted_strengths": [],
        "extracted_weaknesses": [],
        # New: Pain point clustering & root cause analysis
        "pain_point_clusters": None,
        "root_causes": None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def run_emotion_analysis(text_list: List[str], threshold: float = 0.3) -> Dict[str, Any]:
    """Run emotion analysis on list of texts"""
    all_results = []
    emotion_sum = {e: 0.0 for e in EMOTIONS}
    emotion_counts = {e: 0 for e in EMOTIONS}
    
    for text in text_list:
        if not text or not text.strip():
            continue
        
        predicted_emotions, probabilities = predict_emotions(text, threshold=threshold)
        all_results.append((text, predicted_emotions, probabilities))
        
        for emotion, prob in probabilities.items():
            emotion_sum[emotion] += prob
            if prob >= threshold:
                emotion_counts[emotion] += 1
    
    n = len(text_list) if text_list else 1
    aggregated_emotions = {e: emotion_sum[e] / n for e in EMOTIONS}
    dominant_emotion = max(aggregated_emotions.items(), key=lambda x: x[1])[0]
    
    return {
        'all_results': all_results,
        'aggregated_emotions': aggregated_emotions,
        'dominant_emotion': dominant_emotion,
        'emotion_counts': emotion_counts,
        'total_analyzed': len(all_results)
    }


def run_bart_summary(text_list: List[str]) -> Dict[str, Any]:
    """Generate micro and macro summaries using BART"""
    micro_summaries = []
    
    for text in text_list[:50]:
        if not text or len(text.strip()) < 20:
            continue
        
        if USE_LOCAL_SUMMARY:
            summary = summarize_text_local(text)
        else:
            from services.summary_service import summarize_text
            summary = summarize_text(text)
        
        micro_summaries.append(summary)
    
    combined_text = " ".join(text_list[:100])
    
    if USE_LOCAL_SUMMARY:
        macro_summary = summarize_text_local(combined_text)
    else:
        from services.summary_service import summarize_text
        macro_summary = summarize_text(combined_text)
    
    return {
        'micro_summaries': micro_summaries,
        'macro_summary': macro_summary
    }


def extract_themes_from_comments(comments: List[str]) -> List[str]:
    """Extract key themes/keywords from comments using simple frequency analysis"""
    from collections import Counter
    import re
    
    # Common words to ignore
    stop_words = {'the', 'is', 'it', 'and', 'to', 'a', 'of', 'for', 'in', 'on', 'this', 'that', 'with', 'are', 'was', 'be', 'have', 'has', 'but', 'not', 'can', 'my', 'i', 'you', 'your', 'me', 'so', 'very', 'just', 'will', 'at', 'from', 'they', 'we', 'or', 'an', 'as', 'by', 'been', 'all', 'would', 'there', 'their'}
    
    all_words = []
    for comment in comments:
        # Extract words (2+ chars, alphabetic)
        words = re.findall(r'\b[a-z]{2,}\b', comment.lower())
        all_words.extend([w for w in words if w not in stop_words])
    
    # Count frequency
    word_counts = Counter(all_words)
    
    # Return top 15 most common
    return [word for word, count in word_counts.most_common(15)]


def run_rag_llm_analysis(
    summary: str, 
    emotions: Dict[str, float],
    dominant_emotion: str,
    original_text: str,
    raw_comments: List[str] = None,
    use_enhanced: bool = False,
    pain_point_clusters: List[Dict[str, Any]] = None,
    root_causes: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run RAG + LLM analysis for enhanced insights"""
    emotion_output = {"probabilities": emotions}
    
    # Extract themes from comments if available
    top_themes = extract_themes_from_comments(raw_comments) if raw_comments else []
    
    # Detect crisis keywords
    crisis_flags = []
    if raw_comments:
        crisis_alerts = detect_crisis_keywords(raw_comments)
        crisis_flags = [alert['keyword'] for alert in crisis_alerts]
    
    result = combine_emotion_and_summary(
        emotion_output=emotion_output,
        summary=summary,
        original_text=original_text,
        use_enhanced_ai=use_enhanced,
        category_context=None,
        raw_comments=raw_comments,
        top_themes=top_themes,
        crisis_flags=crisis_flags,
        pain_point_clusters=pain_point_clusters,
        root_causes=root_causes
    )
    
    return result


def compute_sentiment_breakdown(emotions: Dict[str, float]) -> Dict[str, Any]:
    """Compute sentiment statistics"""
    positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
    negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
    
    positive_score = min(sum([emotions.get(e, 0.0) for e in positive_emotions]), 1.0)
    negative_score = min(sum([emotions.get(e, 0.0) for e in negative_emotions]), 1.0)
    neutral_score = 1.0 - positive_score - negative_score
    
    if positive_score > negative_score:
        status = "Positive"
    elif negative_score > positive_score:
        status = "Negative"
    else:
        status = "Neutral"
    
    return {
        'positive': positive_score,
        'negative': negative_score,
        'neutral': max(neutral_score, 0.0),
        'status': status
    }


def detect_crisis_keywords(text_list: List[str]) -> List[Dict[str, Any]]:
    """Detect crisis-related keywords in comments"""
    crisis_keywords = {
        'complaint': ['complaint', 'complain', 'issue', 'problem', 'terrible', 'awful'],
        'frustration': ['frustrated', 'frustrating', 'annoying', 'annoyed', 'irritating'],
        'anger': ['angry', 'furious', 'outraged', 'unacceptable', 'disgusting'],
        'refund': ['refund', 'money back', 'return', 'cancel', 'subscription'],
        'legal': ['lawsuit', 'lawyer', 'sue', 'legal action', 'report']
    }
    
    alerts = []
    
    for text in text_list:
        text_lower = text.lower()
        
        for category, keywords in crisis_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    alerts.append({
                        'category': category,
                        'keyword': keyword,
                        'text': text[:100] + '...' if len(text) > 100 else text
                    })
                    break
    
    return alerts


def prepare_business_report() -> Dict[str, Any]:
    """Prepare comprehensive business report from session state"""
    return {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "report_type": "business_buddy_analysis",
            "tool": "EmoSense AI Business Buddy",
            "comments_analyzed": len(st.session_state.analysis_raw_comments)
        },
        "raw_comments": st.session_state.analysis_raw_comments,
        "emotion_analysis": st.session_state.analysis_emotions,
        "summary": st.session_state.analysis_summary,
        "sentiment_breakdown": st.session_state.analysis_sentiments,
        "insights": st.session_state.analysis_insights,
        "crisis_alerts": st.session_state.crisis_alerts
    }


# ============================================================================
# CHAT FUNCTIONS
# ============================================================================

def get_openai_client() -> Optional[OpenAI]:
    """Get OpenAI client if API key available"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and hasattr(st, 'secrets'):
            api_key = st.secrets.get("OPENAI_API_KEY", None)
        
        if api_key:
            return OpenAI(api_key=api_key)
        return None
    except:
        return None


def extract_strengths_and_weaknesses(emotions: Dict[str, float], comments: List[str]) -> Dict[str, List[str]]:
    """Extract strengths and weaknesses from emotions and comments"""
    positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
    negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment", "confusion", "frustration"]
    
    strengths = []
    weaknesses = []
    
    # Analyze emotions
    for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
        if score > 0.2:  # Significant presence
            if emotion in positive_emotions:
                strengths.append(f"{emotion.capitalize()} ({score:.0%})")
            elif emotion in negative_emotions:
                weaknesses.append(f"{emotion.capitalize()} ({score:.0%})")
    
    return {
        "strengths": strengths[:5],  # Top 5
        "weaknesses": weaknesses[:5]  # Top 5
    }


def build_persistent_chat_context():
    """
    Build persistent chat context from analysis results.
    This context is stored in session state and reused across all chat turns.
    """
    emotions = st.session_state.analysis_emotions.get('aggregated_emotions', {})
    sentiments = st.session_state.analysis_sentiments
    summary = st.session_state.analysis_summary.get('macro_summary', '')
    micro_summaries = st.session_state.analysis_summary.get('micro_summaries', [])
    insights = st.session_state.analysis_insights
    comments = st.session_state.analysis_raw_comments
    crisis_alerts = st.session_state.crisis_alerts
    
    # Extract and store themes (persistent)
    if not st.session_state.extracted_themes:
        st.session_state.extracted_themes = extract_themes_from_comments(comments)
    
    # Extract and store strengths/weaknesses (persistent)
    if not st.session_state.extracted_strengths or not st.session_state.extracted_weaknesses:
        sw = extract_strengths_and_weaknesses(emotions, comments)
        st.session_state.extracted_strengths = sw['strengths']
        st.session_state.extracted_weaknesses = sw['weaknesses']
    
    # Use stored values
    themes = st.session_state.extracted_themes
    strengths = st.session_state.extracted_strengths
    weaknesses = st.session_state.extracted_weaknesses
    
    # Format all data for system prompt
    
    # 1. Sentiment Overview
    sentiment_text = f"""
**📈 SENTIMENT OVERVIEW:**
- Positive: {sentiments.get('positive', 0):.1%}
- Negative: {sentiments.get('negative', 0):.1%}
- Neutral: {sentiments.get('neutral', 0):.1%}
- Overall Status: {sentiments.get('status', 'Unknown')}
"""
    
    # 2. Top Emotions (top 10)
    top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:10]
    emotions_text = "**🎭 TOP EMOTIONS DETECTED:**\n"
    for emotion, prob in top_emotions:
        emotions_text += f"  - {emotion.capitalize()}: {prob:.1%}\n"
    
    # 3. Strengths
    strengths_text = "**💪 STRENGTHS (Positive Signals):**\n"
    if strengths:
        for s in strengths:
            strengths_text += f"  ✅ {s}\n"
    else:
        strengths_text += "  (No significant positive emotions detected)\n"
    
    # 4. Weaknesses
    weaknesses_text = "**⚠️ WEAKNESSES (Negative Signals):**\n"
    if weaknesses:
        for w in weaknesses:
            weaknesses_text += f"  ❌ {w}\n"
    else:
        weaknesses_text += "  (No significant negative emotions detected)\n"
    
    # 5. Themes
    themes_text = f"**🔍 KEY THEMES (Extracted Keywords):**\n{', '.join(themes[:15]) if themes else 'No themes extracted'}\n"
    
    # 6. Crisis Flags
    crisis_text = ""
    if crisis_alerts:
        crisis_categories = {}
        for alert in crisis_alerts:
            cat = alert['category']
            if cat not in crisis_categories:
                crisis_categories[cat] = []
            crisis_categories[cat].append(alert['keyword'])
        
        crisis_text = "\n**🚨 CRISIS FLAGS DETECTED:**\n"
        for cat, keywords in crisis_categories.items():
            crisis_text += f"  - {cat.capitalize()}: {', '.join(set(keywords))}\n"
    else:
        crisis_text = "\n**✅ NO CRISIS FLAGS DETECTED**\n"
    
    # 7. Macro Summary
    summary_text = f"""
**📝 MACRO SUMMARY:**
{summary}
"""
    
    # 8. Raw Comments (sample - up to 20)
    comments_sample = comments[:20] if len(comments) > 20 else comments
    comments_text = f"**📄 CUSTOMER COMMENTS ({len(comments_sample)} of {len(comments)} total):**\n"
    for i, comment in enumerate(comments_sample, 1):
        comment_truncated = comment[:200] + "..." if len(comment) > 200 else comment
        comments_text += f'{i}. "{comment_truncated}"\n'
    
    # 9. Micro Summaries (if available)
    micro_text = ""
    if micro_summaries and len(micro_summaries) > 0:
        micro_text = f"\n**📋 MICRO SUMMARIES (First 5):**\n"
        for i, ms in enumerate(micro_summaries[:5], 1):
            # Handle both string and dict formats
            if isinstance(ms, dict):
                summary_content = ms.get("summary", "N/A")
            else:
                summary_content = str(ms)
            micro_text += f'{i}. {summary_content}\n'
    
    # 10. AI Insights
    insights_text = f"""
**💡 AI-GENERATED INSIGHTS:**
{insights.get('suggested_action', 'No insights generated yet')}
"""
    
    # 11. RAG Context (if available)
    rag_text = ""
    if insights.get('sources'):
        rag_text = "\n**📚 RELEVANT MARKET RESEARCH:**\n"
        for source in insights.get('sources', [])[:3]:
            rag_text += f"  - {source.get('title', 'Unknown')} ({source.get('category', 'General')})\n"
    
    # 12. Pain Point Clusters (NEW)
    clusters_text = ""
    if st.session_state.pain_point_clusters and st.session_state.pain_point_clusters.get('clusters'):
        clusters = st.session_state.pain_point_clusters['clusters']
        clusters_text = f"\n**🎯 PAIN POINT CLUSTERS ({len(clusters)} clusters identified):**\n"
        for cluster in clusters:
            clusters_text += f"""
  Cluster {cluster['cluster_id']}: {cluster['theme_name']}
    - Size: {cluster['size']} comments ({cluster['percentage']:.1f}%)
    - Keywords: {', '.join(cluster['theme_keywords'])}
    - Sentiment: {cluster['sentiment_summary']['status']}
    - Example: "{cluster['comment_examples'][0][:100]}..."
"""
    
    # 13. Root Causes (NEW)
    root_causes_text = ""
    if st.session_state.root_causes and st.session_state.root_causes.get('root_causes'):
        root_causes = st.session_state.root_causes['root_causes']
        root_causes_text = f"\n**🔬 ROOT CAUSE ANALYSIS ({len(root_causes)} causes identified):**\n"
        for rc in root_causes:
            evidence_preview = rc['evidence'][0][:80] + "..." if rc['evidence'] else "No evidence"
            root_causes_text += f"""
  {rc['theme_name']}:
    - Root Cause: {rc['root_cause'][:150]}...
    - Evidence: "{evidence_preview}"
    - Action: {rc['actionable_insight'][:100]}...
"""
    
    # Combine everything
    full_context = f"""
═══════════════════════════════════════════════════════════════
📊 CUSTOMER FEEDBACK DATASET - COMPLETE ANALYSIS CONTEXT
═══════════════════════════════════════════════════════════════

{sentiment_text}
{emotions_text}
{strengths_text}
{weaknesses_text}
{themes_text}
{crisis_text}
{summary_text}
{comments_text}
{micro_text}
{insights_text}
{rag_text}
{clusters_text}
{root_causes_text}

═══════════════════════════════════════════════════════════════
END OF CUSTOMER FEEDBACK CONTEXT
═══════════════════════════════════════════════════════════════
"""
    
    return full_context


def build_chat_system_prompt() -> str:
    """
    Build the FULL system prompt with ALL customer insights.
    This is called ONCE when analysis completes and stored in session state.
    It's reused for EVERY chat turn to maintain context.
    """
    
    # Get the full persistent context
    context_data = build_persistent_chat_context()
    
    system_prompt = f"""You are Business Buddy — an expert AI consultant and senior customer insights analyst with 25+ years of experience in:

- **Customer Analytics & Behavioral Psychology**
- **UX Research & Product Strategy**
- **Growth Marketing & Retention Optimization**
- **Brand Management & Crisis Response**
- **Data-Driven Decision Making**
- **AI-Powered Business Intelligence**

═══════════════════════════════════════════════════════════════
🎯 YOUR CORE MISSION
═══════════════════════════════════════════════════════════════

You analyze and speak based ONLY on the uploaded customer comments provided below.
You have been given a COMPLETE dataset of customer feedback with:
- Raw customer comments
- Emotion analysis
- Sentiment breakdown
- Extracted themes and patterns
- Strengths and weaknesses
- Crisis indicators
- AI-generated insights

YOU MUST USE THIS CONTEXT IN EVERY SINGLE ANSWER.

═══════════════════════════════════════════════════════════════
📊 CUSTOMER FEEDBACK CONTEXT (USE THIS FOR ALL ANSWERS)
═══════════════════════════════════════════════════════════════

{context_data}

═══════════════════════════════════════════════════════════════
🎯 HOW TO ANSWER QUESTIONS
═══════════════════════════════════════════════════════════════

**For ANY question the user asks, you MUST:**

1. **Reference the actual customer comments**
   - Quote specific comments when relevant
   - Mention frequencies ("5 customers mentioned...", "appeared 3 times")
   - Cite emotion patterns ("confusion at 38%", "joy at 62%")

2. **Use Pain Point Clusters (if available)**
   - Reference specific clusters by name
   - Cite cluster size and percentage
   - Use cluster keywords and themes

3. **Apply Root Cause Reasoning (CRITICAL)**
   - Identify WHY customers feel what they feel (not just WHAT)
   - Use the root cause analysis provided
   - Focus on underlying causes, not symptoms
   - Connect cause → effect → solution

4. **Tie recommendations to REAL issues in the data**
   - If they ask "What should I improve?" → Cite root causes from clusters
   - If they ask "What do customers love?" → Reference positive clusters
   - If they ask "How to reduce churn?" → Address root causes of frustration/disappointment

5. **Use ALL extracted insights**
   - Themes (keywords that appear frequently)
   - Strengths (what's working based on positive emotions)
   - Weaknesses (what's broken based on negative emotions)
   - Crisis flags (urgent issues detected)
   - **Pain point clusters (grouped themes)**
   - **Root causes (underlying reasons)**

6. **Be specific, never generic**
   ❌ BAD: "Improve user experience"
   ✅ GOOD: "Fix the onboarding confusion (Cluster 2, 28% of feedback) caused by unclear pricing labels - address the root cause by adding tooltips explaining tier differences"

7. **Support every claim with data**
   - "Based on Cluster 1 (Pricing Concerns, 7 comments)..."
   - "Root cause analysis shows this is caused by..."
   - "Evidence: 'quote from comment'"

═══════════════════════════════════════════════════════════════
📋 MANDATORY ANSWER FORMAT (USE FOR EVERY RESPONSE)
═══════════════════════════════════════════════════════════════

Structure EVERY response exactly like this:

### 🔬 Root Cause Insight
[Identify the UNDERLYING cause behind the customer pattern - WHY do customers feel this way?]
[Reference pain point clusters and root cause analysis]

### 🧠 Data Points Supporting This
- Quote actual customer comments or reference specific patterns
- Cite cluster names, sizes, and percentages
- Reference root causes identified
- Mention emotion percentages, themes, or frequencies

### 🎯 Recommendation / Answer
[Specific, actionable steps that directly address issues in the customer comments]
[Each recommendation should tie back to something customers actually said]

### 📈 Expected Impact
[Explain how this solves the REAL customer issues found in your data]
[Reference specific pain points or opportunities from the comments]

═══════════════════════════════════════════════════════════════
🚫 ABSOLUTELY FORBIDDEN
═══════════════════════════════════════════════════════════════

❌ Generic business advice not tied to the comments ("improve UX", "enhance marketing")
❌ Suggesting fixes for problems NOT mentioned in customer feedback
❌ Making up customer quotes or data
❌ Giving textbook answers without referencing the dataset
❌ Motivational fluff or vague statements
❌ Answering questions unrelated to business/product insights
❌ Forgetting previous context from earlier in the conversation
❌ Ignoring the emotions, themes, or crisis flags provided

**If asked something completely unrelated to business insights:**
Respond: "I can only answer questions related to insights from the customer feedback you uploaded. Please ask about your customers, product, marketing, features, or business strategy."

═══════════════════════════════════════════════════════════════
🧠 MULTI-TURN CONVERSATION INTELLIGENCE
═══════════════════════════════════════════════════════════════

Remember: You have FULL CONTEXT for the entire conversation.
- If user asks "What are my top weaknesses?" → Use the WEAKNESSES section
- If user asks "How do I fix confusion?" → Find "confusion" in emotions and related comments
- If user asks "What should my UX team prioritize?" → Reference specific UX issues mentioned
- If user asks "Give me campaign ideas" → Use positive comments and strengths
- If user asks "Why are customers annoyed?" → Find "annoyance" emotion and analyze related comments
- If user asks follow-up questions → Build on previous answers using the SAME dataset

═══════════════════════════════════════════════════════════════
🎯 REMEMBER YOUR ROLE
═══════════════════════════════════════════════════════════════

You are NOT a generic AI.
You are a $500/hour senior consultant analyzing THIS SPECIFIC business's customer feedback.
Every answer must be deeply personalized to THEIR data.
Quote their customers. Reference their specific issues. Solve their actual problems.

Now answer the user's question using ONLY the customer feedback context provided above.
"""
    
    return system_prompt


def handle_business_chat_query(user_message: str) -> str:
    """
    Handle chat query with FULL persistent context.
    System prompt is built once and reused across all turns.
    """
    client = get_openai_client()
    
    if not client:
        return "⚠️ Chat feature requires OpenAI API key. Please set OPENAI_API_KEY in environment or secrets."
    
    # Check if analysis has been run
    if not st.session_state.analysis_complete:
        return "⚠️ Please run an analysis first before chatting. Upload comments and click 'Analyze' button."
    
    # Build system prompt ONCE if not already built, then reuse it
    if not st.session_state.chat_context_built or not st.session_state.chat_system_prompt:
        st.session_state.chat_system_prompt = build_chat_system_prompt()
        st.session_state.chat_context_built = True
    
    # Use the persistent system prompt
    system_prompt = st.session_state.chat_system_prompt
    
    try:
        # Send request with persistent context
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6,  # Lower for focused, data-driven responses
            max_tokens=900  # More space for detailed, multi-turn analysis
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Chat error: {str(e)}"


# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_emotion_distribution_chart(emotions: Dict[str, float]):
    """Render emotion distribution bar chart"""
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if not PLOTLY_AVAILABLE:
        # Fallback: Simple text display
        st.markdown("### Top 10 Detected Emotions")
        for emotion, prob in sorted_emotions:
            emoji = EMOJI_MAP.get(emotion, "🎭")
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px; 
                        background: rgba(255,255,255,0.05); margin: 4px 0; border-radius: 8px;">
                <span style="color: #FFFFFF;">{emoji} {emotion.capitalize()}</span>
                <span style="color: #8A5CF6; font-weight: bold;">{prob*100:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        return
    
    emotion_names = [e[0].capitalize() for e in sorted_emotions]
    emotion_values = [e[1] * 100 for e in sorted_emotions]
    emotion_emojis = [EMOJI_MAP.get(e[0], "🎭") for e in sorted_emotions]
    
    labels = [f"{emoji} {name}" for emoji, name in zip(emotion_emojis, emotion_names)]
    
    fig = go.Figure(data=[
        go.Bar(
            y=labels,
            x=emotion_values,
            orientation='h',
            marker=dict(
                color=emotion_values,
                colorscale='Purples',
                showscale=False
            ),
            text=[f"{v:.1f}%" for v in emotion_values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Probability: %{x:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top 10 Detected Emotions",
        xaxis_title="Probability (%)",
        yaxis_title="",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color='#FFFFFF'),
        margin=dict(l=150, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_sentiment_pie_chart(sentiments: Dict[str, float]):
    """Render sentiment pie chart"""
    if not PLOTLY_AVAILABLE:
        # Fallback: Simple progress bars
        st.markdown("### Sentiment Distribution")
        
        for label, value, color in [
            ('Positive', sentiments.get('positive', 0), '#10B981'),
            ('Negative', sentiments.get('negative', 0), '#EF4444'),
            ('Neutral', sentiments.get('neutral', 0), '#6B7280')
        ]:
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: {color};">{label}</span>
                    <span style="color: #FFFFFF; font-weight: bold;">{value*100:.1f}%</span>
                </div>
                <div style="background: rgba(255,255,255,0.1); height: 20px; border-radius: 10px; overflow: hidden;">
                    <div style="background: {color}; width: {value*100}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        return
    
    labels = ['Positive', 'Negative', 'Neutral']
    values = [
        sentiments.get('positive', 0) * 100,
        sentiments.get('negative', 0) * 100,
        sentiments.get('neutral', 0) * 100
    ]
    colors = ['#10B981', '#EF4444', '#6B7280']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(color='#FFFFFF', size=14),
            hovertemplate='<b>%{label}</b><br>%{value:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Sentiment Distribution",
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_chat_interface():
    """Render Business Buddy chat interface"""
    st.markdown("""
    <div class="glass-card" style="padding: 24px; margin-top: 2rem;">
        <h3 style="color: #FFFFFF; margin-bottom: 0.5rem;">💬 Chat with Business Buddy</h3>
        <p style="color: #A8A9B3; margin-bottom: 1rem;">
            Ask questions about your customer feedback. Business Buddy is a senior customer insights analyst 
            with 25+ years of experience who will provide data-backed recommendations based on YOUR actual comments.
        </p>
        <p style="color: #8A5CF6; font-size: 0.9rem; margin-bottom: 0;">
            💡 Try asking: "What are customers most frustrated about?", "How can I improve retention?", 
            "What features are they requesting?", "Should I be worried about these comments?"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    if st.session_state.business_chat_history:
        for msg in st.session_state.business_chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="message-user fade-in">
                    {msg['content']}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-ai fade-in">
                    {msg['content']}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
        
        spacer("sm")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_question = st.text_input(
            "Ask Business Buddy:",
            placeholder="e.g., What are the biggest issues? How can I reduce churn? What do customers love most?",
            key="buddy_question",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("💬 Send", type="primary", use_container_width=True)
    
    if send_button and user_question.strip():
        st.session_state.business_chat_history.append({
            "role": "user",
            "content": user_question
        })
        
        with st.spinner("🤔 Business Buddy is thinking..."):
            response = handle_business_chat_query(user_question)
        
        st.session_state.business_chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()
    
    if st.session_state.business_chat_history:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.business_chat_history = []
            st.rerun()


# ============================================================================
# MAIN APP
# ============================================================================

with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    gradient_hero(
        "🤝 Business Buddy: Your Brand Therapist",
        "Analyze customer feedback. Understand emotions. Take action. Your intelligent business analytics companion."
    )
    
    spacer("lg")
    
    # INPUT CARD
    st.markdown("""
    <div class="glass-card" style="padding: 32px;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Upload Customer Feedback</h3>
        <p style="color: #A8A9B3; line-height: 1.6;">
            Analyze single comments or upload a CSV file with multiple customer responses.
            Get comprehensive emotion analysis, summaries, and strategic recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("md")
    
    input_method = st.radio(
        "Choose Input Method:",
        ["📝 Single Comment Thread", "📄 CSV Upload"],
        horizontal=True
    )
    
    spacer("sm")
    
    text_input = None
    csv_comments = []
    
    if input_method == "📝 Single Comment Thread":
        text_input = st.text_area(
            "Enter customer feedback:",
            height=150,
            placeholder="Paste customer comments, reviews, or social media feedback here..."
        )
        
        if text_input:
            csv_comments = [text_input]
    
    else:
        uploaded_file = st.file_uploader(
            "Upload CSV file:",
            type=['csv'],
            help="CSV should contain a column with customer comments"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded {len(df)} rows from CSV")
                
                text_columns = df.select_dtypes(include=['object']).columns.tolist()
                
                if text_columns:
                    comment_column = st.selectbox(
                        "Select the column containing comments:",
                        text_columns
                    )
                    
                    csv_comments = df[comment_column].dropna().astype(str).tolist()
                    st.info(f"📊 Found {len(csv_comments)} valid comments")
                else:
                    st.error("❌ No text columns found in CSV")
            
            except Exception as e:
                st.error(f"❌ Error reading CSV: {str(e)}")
    
    spacer("sm")
    
    col1, col2 = st.columns(2)
    
    with col1:
        threshold = st.slider(
            "Emotion Confidence Threshold:",
            min_value=0.1,
            max_value=0.9,
            value=0.3,
            step=0.05
        )
    
    with col2:
        use_enhanced_ai = st.checkbox(
            "🤖 Enable Enhanced AI (RAG + GPT-4o-mini)",
            value=True,
            help="Use advanced recommendations with market research context"
        )
    
    spacer("md")
    
    analyze_button = st.button(
        "✨ Analyze Now",
        type="primary",
        use_container_width=True
    )
    
    # ANALYSIS EXECUTION
    if analyze_button:
        if not csv_comments:
            st.error("⚠️ Please enter text or upload a CSV file")
        else:
            st.session_state.analysis_complete = False
            st.session_state.business_chat_history = []
            st.session_state.analysis_raw_comments = csv_comments
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🎭 Analyzing emotions...")
            progress_bar.progress(20)
            emotion_results = run_emotion_analysis(csv_comments, threshold=threshold)
            st.session_state.analysis_emotions = emotion_results
            
            status_text.text("📝 Generating summaries...")
            progress_bar.progress(40)
            summary_results = run_bart_summary(csv_comments)
            st.session_state.analysis_summary = summary_results
            
            status_text.text("📊 Computing sentiment breakdown...")
            progress_bar.progress(60)
            sentiment_breakdown = compute_sentiment_breakdown(emotion_results['aggregated_emotions'])
            st.session_state.analysis_sentiments = sentiment_breakdown
            
            status_text.text("🧠 Generating strategic insights...")
            progress_bar.progress(80)
            insights = run_rag_llm_analysis(
                summary=summary_results['macro_summary'],
                emotions=emotion_results['aggregated_emotions'],
                dominant_emotion=emotion_results['dominant_emotion'],
                original_text=" ".join(csv_comments[:50]),
                raw_comments=csv_comments,  # Pass raw comments
                use_enhanced=use_enhanced_ai and RAG_AVAILABLE
            )
            st.session_state.analysis_insights = insights
            
            status_text.text("🚨 Detecting crisis keywords...")
            progress_bar.progress(85)
            crisis_alerts = detect_crisis_keywords(csv_comments)
            st.session_state.crisis_alerts = crisis_alerts
            
            # NEW: Pain point clustering
            if CLUSTERING_AVAILABLE and use_enhanced_ai:
                status_text.text("🔍 Clustering pain points...")
                progress_bar.progress(90)
                
                # Get emotions per comment for clustering
                emotions_per_comment = []
                for result in emotion_results.get('individual_results', []):
                    emotions_per_comment.append(result.get('probabilities', {}))
                
                clustering_result = cluster_comments(
                    comments=csv_comments,
                    emotions_per_comment=emotions_per_comment,
                    min_cluster_size=2,
                    max_clusters=8
                )
                st.session_state.pain_point_clusters = clustering_result
            else:
                st.session_state.pain_point_clusters = None
            
            # NEW: Root cause analysis
            if ROOT_CAUSE_AVAILABLE and use_enhanced_ai and st.session_state.pain_point_clusters:
                status_text.text("🧠 Analyzing root causes...")
                progress_bar.progress(95)
                
                try:
                    root_cause_engine = get_root_cause_engine()
                    if root_cause_engine and st.session_state.pain_point_clusters.get('clusters'):
                        root_cause_result = root_cause_engine.infer_root_causes(
                            clusters=st.session_state.pain_point_clusters['clusters'],
                            emotions=emotion_results['aggregated_emotions'],
                            themes=st.session_state.extracted_themes if st.session_state.extracted_themes else [],
                            macro_summary=summary_results['macro_summary'],
                            raw_comments=csv_comments
                        )
                        st.session_state.root_causes = root_cause_result
                    else:
                        st.session_state.root_causes = None
                except Exception as e:
                    print(f"Root cause analysis error: {e}")
                    st.session_state.root_causes = None
            else:
                st.session_state.root_causes = None
            
            # Regenerate insights with clusters and root causes (if enhanced AI enabled)
            if use_enhanced_ai and (st.session_state.pain_point_clusters or st.session_state.root_causes):
                status_text.text("🔬 Regenerating insights with root cause analysis...")
                insights_enhanced = run_rag_llm_analysis(
                    summary=summary_results['macro_summary'],
                    emotions=emotion_results['aggregated_emotions'],
                    dominant_emotion=emotion_results['dominant_emotion'],
                    original_text=" ".join(csv_comments[:50]),
                    raw_comments=csv_comments,
                    use_enhanced=True,
                    pain_point_clusters=st.session_state.pain_point_clusters.get('clusters') if st.session_state.pain_point_clusters else None,
                    root_causes=st.session_state.root_causes
                )
                st.session_state.analysis_insights = insights_enhanced
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            st.session_state.analysis_complete = True
            
            # Reset chat context so it rebuilds with new data
            st.session_state.chat_context_built = False
            st.session_state.chat_system_prompt = ""
            
            import time
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 Analysis complete! Scroll down to view results.")
            st.rerun()
    
    # RESULTS DISPLAY
    if st.session_state.analysis_complete:
        spacer("xl")
        
        # Summary
        st.markdown("""
        <div class="glass-card" style="padding: 32px;">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📝 Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-top: 1rem;">
            <p style="color: #FFFFFF; line-height: 1.8; font-size: 1rem;">
                {st.session_state.analysis_summary.get('macro_summary', 'No summary available')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        spacer("lg")
        
        # Emotions
        st.markdown("""
        <div class="glass-card" style="padding: 32px;">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🎭 Emotion Distribution</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_emotion_distribution_chart(
                st.session_state.analysis_emotions['aggregated_emotions']
            )
        
        with col2:
            dominant = st.session_state.analysis_emotions['dominant_emotion']
            dominant_prob = st.session_state.analysis_emotions['aggregated_emotions'][dominant]
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(138, 92, 246, 0.2), rgba(192, 108, 255, 0.2)); 
                        padding: 24px; border-radius: 12px; text-align: center;">
                <h4 style="color: #FFFFFF; margin-bottom: 0.5rem;">Dominant Emotion</h4>
                <div style="font-size: 3rem; margin: 1rem 0;">
                    {EMOJI_MAP.get(dominant, '🎭')}
                </div>
                <h3 style="color: #FFFFFF; margin: 0.5rem 0;">{dominant.capitalize()}</h3>
                <p style="color: #A8A9B3; font-size: 1.2rem; margin: 0;">
                    {dominant_prob:.1%} confidence
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            spacer("sm")
            st.metric("Comments Analyzed", st.session_state.analysis_emotions['total_analyzed'])
        
        spacer("lg")
        
        # Sentiment
        st.markdown("""
        <div class="glass-card" style="padding: 32px;">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Sentiment Breakdown</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            render_sentiment_pie_chart(st.session_state.analysis_sentiments)
        
        with col2:
            sentiments = st.session_state.analysis_sentiments
            
            st.markdown(f"#### Overall Status: **{sentiments['status']}**")
            
            spacer("sm")
            
            # Positive
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown("✅ **Positive**")
            with col_b:
                st.markdown(f"**{sentiments['positive']:.1%}**")
            st.progress(sentiments['positive'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Negative
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown("❌ **Negative**")
            with col_b:
                st.markdown(f"**{sentiments['negative']:.1%}**")
            st.progress(sentiments['negative'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Neutral
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown("⚪ **Neutral**")
            with col_b:
                st.markdown(f"**{sentiments['neutral']:.1%}**")
            st.progress(sentiments['neutral'])
        
        spacer("lg")
        
        # Insights with Download Button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="glass-card" style="padding: 32px;">
                <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🧠 Strategic Insights</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
            report_json = prepare_business_report()
            json_data = json.dumps(report_json, indent=2)
            
            st.download_button(
                label="📥 Download Report",
                data=json_data,
                file_name=f"business_buddy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        insights = st.session_state.analysis_insights
        
        # Show only Recommended Actions (no Reasoning column)
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-top: 1rem;">
            <h4 style="color: #C06CFF; margin-bottom: 0.5rem;">🎯 Recommended Actions</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(insights.get('suggested_action', 'No suggestions available'))
        
        spacer("lg")
        
        # Crisis Alerts
        if st.session_state.crisis_alerts:
            st.markdown(f"""
            <div class="glass-card" style="padding: 32px; border-left: 4px solid #EF4444;">
                <h3 style="color: #EF4444; margin-bottom: 1rem;">🚨 Crisis Alerts Detected</h3>
                <p style="color: #A8A9B3;">
                    Found {len(st.session_state.crisis_alerts)} comments with critical keywords that require immediate attention.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            spacer("sm")
            
            for alert in st.session_state.crisis_alerts[:5]:
                st.warning(f"**{alert['category'].upper()}**: *{alert['keyword']}* — {alert['text']}")
            
            spacer("lg")
        
        # CHAT INTERFACE - Moved before Download section
        render_chat_interface()
        
        spacer("xl")
    
    spacer("xl")
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
