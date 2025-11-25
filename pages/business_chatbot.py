"""
🤝 Business Buddy - AI Strategy Assistant
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
        "crisis_alerts": []
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
    use_enhanced: bool = False
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
        crisis_flags=crisis_flags
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


def build_chat_context() -> str:
    """Build comprehensive chat context from analysis results"""
    emotions = st.session_state.analysis_emotions.get('aggregated_emotions', {})
    sentiments = st.session_state.analysis_sentiments
    summary = st.session_state.analysis_summary.get('macro_summary', '')
    micro_summaries = st.session_state.analysis_summary.get('micro_summaries', [])
    insights = st.session_state.analysis_insights
    comments = st.session_state.analysis_raw_comments
    crisis_alerts = st.session_state.crisis_alerts
    
    # Extract top emotions
    top_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:8]
    top_emotions_str = "\n".join([f"  - {e.capitalize()}: {p:.1%}" for e, p in top_emotions])
    
    # Extract strengths and weaknesses
    sw = extract_strengths_and_weaknesses(emotions, comments)
    strengths_str = "\n".join([f"  ✅ {s}" for s in sw['strengths']]) if sw['strengths'] else "  (None detected)"
    weaknesses_str = "\n".join([f"  ❌ {w}" for w in sw['weaknesses']]) if sw['weaknesses'] else "  (None detected)"
    
    # Extract themes (already done in analysis)
    themes = extract_themes_from_comments(comments)
    themes_str = ", ".join(themes[:12]) if themes else "No themes extracted"
    
    # Format crisis alerts
    crisis_str = ""
    if crisis_alerts:
        crisis_categories = {}
        for alert in crisis_alerts:
            cat = alert['category']
            if cat not in crisis_categories:
                crisis_categories[cat] = []
            crisis_categories[cat].append(alert['keyword'])
        
        crisis_str = "\n**🚨 CRISIS FLAGS DETECTED:**\n"
        for cat, keywords in crisis_categories.items():
            crisis_str += f"  - {cat.capitalize()}: {', '.join(set(keywords))}\n"
    
    # Sample comments (up to 15 for context)
    comments_sample = comments[:15] if len(comments) > 15 else comments
    comments_str = "\n".join([f'{i+1}. "{c[:150]}{"..." if len(c) > 150 else ""}"' for i, c in enumerate(comments_sample)])
    
    # Build context document
    context = f"""
═══════════════════════════════════════════════════════════════
📊 CUSTOMER FEEDBACK DATASET - FULL ANALYSIS CONTEXT
═══════════════════════════════════════════════════════════════

**📈 SENTIMENT OVERVIEW:**
- Positive: {sentiments.get('positive', 0):.1%}
- Negative: {sentiments.get('negative', 0):.1%}
- Neutral: {sentiments.get('neutral', 0):.1%}
- Overall Status: {sentiments.get('status', 'Unknown')}

**🎭 TOP EMOTIONS DETECTED:**
{top_emotions_str}

**💪 STRENGTHS (Positive Signals):**
{strengths_str}

**⚠️ WEAKNESSES (Negative Signals):**
{weaknesses_str}

**🔍 KEY THEMES (Extracted Keywords):**
{themes_str}

**📝 MACRO SUMMARY:**
{summary}

**📄 SAMPLE CUSTOMER COMMENTS ({len(comments_sample)} of {len(comments)} total):**
{comments_str}
{crisis_str}

**💡 AI-GENERATED INSIGHTS:**
{insights.get('suggested_action', 'No insights generated yet')}

═══════════════════════════════════════════════════════════════
"""
    
    return context


def handle_business_chat_query(user_message: str) -> str:
    """Handle chat query with full context-aware analysis"""
    client = get_openai_client()
    
    if not client:
        return "⚠️ Chat feature requires OpenAI API key. Please set OPENAI_API_KEY in environment or secrets."
    
    # Check if analysis has been run
    if not st.session_state.analysis_complete:
        return "⚠️ Please run an analysis first before chatting. Upload comments and click 'Analyze' button."
    
    # Build comprehensive context
    context = build_chat_context()
    
    system_prompt = """You are a SENIOR CUSTOMER INSIGHTS ANALYST with 25+ years of experience in:
- AI/ML product development
- UX research & customer experience optimization
- Brand management & product strategy
- Growth marketing & retention analytics
- Business consulting & data-driven decision making

You are NOT a generic chatbot. You are a context-aware consultant analyzing REAL customer feedback.

═══════════════════════════════════════════════════════════════
🎯 YOUR ROLE & RESPONSIBILITIES
═══════════════════════════════════════════════════════════════

You have been provided with a complete customer feedback dataset including:
- Raw customer comments
- Emotion analysis
- Sentiment breakdown
- Key themes
- Strengths and weaknesses
- Crisis flags
- AI-generated insights

Your job is to answer user questions by:
1. **ONLY using the provided customer data** (never make up information)
2. **Quoting actual customer comments** when relevant
3. **Referencing specific emotions and themes** detected in the data
4. **Providing data-backed recommendations** tied to actual customer issues
5. **Being specific, not generic** (e.g., not "improve UX" but "fix the onboarding confusion mentioned by 4 customers")

═══════════════════════════════════════════════════════════════
📋 ANSWER FORMAT (MANDATORY)
═══════════════════════════════════════════════════════════════

Structure EVERY response like this:

### 🔍 Insight Based on Your Customer Feedback
[Short interpretation based on the comment dataset]

### 🧠 Data Points Supporting This
- Quote or reference actual comments
- Mention emotion patterns
- Cite themes or frequencies

### 🎯 Recommendation / Answer
[Specific, actionable advice tailored to the uploaded comments]

### 📈 Expected Impact
[Explain how this addresses the real customer issues found in the data]

═══════════════════════════════════════════════════════════════
🚫 ABSOLUTELY FORBIDDEN
═══════════════════════════════════════════════════════════════

❌ Generic advice not tied to comments ("improve UX", "enhance marketing")
❌ Suggestions for issues NOT mentioned in the customer feedback
❌ Making up customer quotes or data points
❌ Textbook answers without referencing the actual dataset
❌ Motivational fluff or vague statements
❌ Answering questions unrelated to business/customer insights

If asked something unrelated to business insights, respond:
"I can only answer questions related to insights from the customer feedback you uploaded."

═══════════════════════════════════════════════════════════════
🧠 REASONING GUIDELINES
═══════════════════════════════════════════════════════════════

- If asked about "improvements" → Identify actual issues from negative emotions/comments
- If asked about "strengths" → Highlight positive emotions and what customers loved
- If asked about "marketing" → Reference what resonated (positive comments) and what didn't
- If asked about "features" → List actual feature requests mentioned in comments
- If asked about "crisis" → Reference crisis flags and urgent issues
- If asked about "retention" → Analyze disappointment, frustration, and what drives joy
- If asked about "competitors" → Can only comment if mentioned in the dataset

Be a data-driven analyst. Every statement should trace back to the customer feedback provided.

═══════════════════════════════════════════════════════════════
"""
    
    user_prompt = f"""
{context}

═══════════════════════════════════════════════════════════════
❓ USER QUESTION
═══════════════════════════════════════════════════════════════

{user_message}

═══════════════════════════════════════════════════════════════

Now answer the user's question using ONLY the customer feedback data above.
Follow the mandatory answer format. Be specific, quote actual comments, and provide data-backed insights.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,  # Lower for more focused, data-driven responses
            max_tokens=800  # More space for detailed analysis
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
        "🤝 Business Buddy — AI Strategy Assistant",
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
            progress_bar.progress(95)
            crisis_alerts = detect_crisis_keywords(csv_comments)
            st.session_state.crisis_alerts = crisis_alerts
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            st.session_state.analysis_complete = True
            
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
        
        # Insights
        st.markdown("""
        <div class="glass-card" style="padding: 32px;">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🧠 Strategic Insights</h3>
        </div>
        """, unsafe_allow_html=True)
        
        insights = st.session_state.analysis_insights
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px;">
                <h4 style="color: #8A5CF6; margin-bottom: 0.5rem;">💡 Reasoning</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <p style="color: #FFFFFF; line-height: 1.6; padding: 1rem;">
                {insights.get('reasoning', 'No reasoning available')}
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px;">
                <h4 style="color: #C06CFF; margin-bottom: 0.5rem;">🎯 Recommended Actions</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <p style="color: #FFFFFF; line-height: 1.6; padding: 1rem;">
                {insights.get('suggested_action', 'No suggestions available')}
            </p>
            """, unsafe_allow_html=True)
        
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
        
        # Download
        st.markdown("""
        <div class="glass-card" style="padding: 32px;">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">💾 Export Business Report</h3>
        </div>
        """, unsafe_allow_html=True)
        
        spacer("sm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_json = prepare_business_report()
            json_data = json.dumps(report_json, indent=2)
            
            st.download_button(
                label="📥 Download Full Report (JSON)",
                data=json_data,
                file_name=f"business_buddy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            st.info("💡 Use this report for team discussions, presentations, or further analysis")
        
        spacer("xl")
        
        # CHAT INTERFACE
        render_chat_interface()
    
    spacer("xl")
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
