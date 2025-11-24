"""
🤝 Business Buddy - AI Strategy Assistant
Full-featured business analytics with conversational AI

Features:
- Single text or CSV batch analysis
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
import plotly.graph_objects as go

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


def run_rag_llm_analysis(
    summary: str, 
    emotions: Dict[str, float],
    dominant_emotion: str,
    original_text: str,
    use_enhanced: bool = False
) -> Dict[str, Any]:
    """Run RAG + LLM analysis for enhanced insights"""
    emotion_output = {"probabilities": emotions}
    
    result = combine_emotion_and_summary(
        emotion_output=emotion_output,
        summary=summary,
        original_text=original_text,
        use_enhanced_ai=use_enhanced,
        category_context=None
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


def handle_business_chat_query(user_message: str) -> str:
    """Handle chat query using analysis context"""
    client = get_openai_client()
    
    if not client:
        return "⚠️ Chat feature requires OpenAI API key. Please set OPENAI_API_KEY in environment or secrets."
    
    emotions = st.session_state.analysis_emotions.get('aggregated_emotions', {})
    sentiments = st.session_state.analysis_sentiments
    summary = st.session_state.analysis_summary.get('macro_summary', '')
    insights = st.session_state.analysis_insights
    comments = st.session_state.analysis_raw_comments[:20]
    
    system_prompt = f"""You are EmoSense AI's Business Buddy — an AI Business Consultant 
trained to analyze customer feedback and provide strategic, data-driven recommendations.

Here is the full analysis of the customer dataset:

**EMOTIONS:**
{json.dumps(emotions, indent=2)}

**SENTIMENT BREAKDOWN:**
- Positive: {sentiments.get('positive', 0):.1%}
- Negative: {sentiments.get('negative', 0):.1%}
- Neutral: {sentiments.get('neutral', 0):.1%}
- Status: {sentiments.get('status', 'Unknown')}

**SUMMARY:**
{summary}

**INSIGHTS:**
{json.dumps(insights, indent=2)}

**SAMPLE COMMENTS:**
{json.dumps(comments[:10], indent=2)}

**YOUR TASK:**
1. Answer the user's question using ONLY the above data.
2. Provide clear, actionable business recommendations.
3. Keep language professional, concise, and strategic.
4. Never invent false data — only reason from the provided insights.
5. Offer industry-validated strategies when relevant.
6. Use bullet points and clear structure.
7. Be conversational but professional.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
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
            Ask questions about your analysis. Business Buddy will provide strategic insights based on your data.
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
            placeholder="e.g., What should I focus on? How can I improve negative sentiment?",
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
        "Choose input method:",
        ["📝 Single Text", "📄 CSV Upload"],
        horizontal=True
    )
    
    spacer("sm")
    
    text_input = None
    csv_comments = []
    
    if input_method == "📝 Single Text":
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
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 24px; border-radius: 12px;">
                <h4 style="color: #FFFFFF; margin-bottom: 1rem;">Overall Status: {sentiments['status']}</h4>
                
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: #10B981;">✅ Positive</span>
                        <span style="color: #FFFFFF; font-weight: bold;">{sentiments['positive']:.1%}</span>
                    </div>
                    <div style="background: rgba(16, 185, 129, 0.2); height: 24px; border-radius: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #10B981, #34D399); 
                                    width: {sentiments['positive']*100}%; height: 100%;"></div>
                    </div>
                </div>
                
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: #EF4444;">❌ Negative</span>
                        <span style="color: #FFFFFF; font-weight: bold;">{sentiments['negative']:.1%}</span>
                    </div>
                    <div style="background: rgba(239, 68, 68, 0.2); height: 24px; border-radius: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #EF4444, #F87171); 
                                    width: {sentiments['negative']*100}%; height: 100%;"></div>
                    </div>
                </div>
                
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: #6B7280;">⚪ Neutral</span>
                        <span style="color: #FFFFFF; font-weight: bold;">{sentiments['neutral']:.1%}</span>
                    </div>
                    <div style="background: rgba(107, 114, 128, 0.2); height: 24px; border-radius: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #6B7280, #9CA3AF); 
                                    width: {sentiments['neutral']*100}%; height: 100%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
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
