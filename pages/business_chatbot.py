"""
Business Buddy - EmoSense AI
Your intelligent business analytics companion with glassmorphic design
Includes: Chat Mode, Smart Summary, Category Detection, AI Insights, Interactive Chat
"""
import streamlit as st
import pandas as pd
import json
import datetime

from utils.predict import predict_emotions
from utils.labels import EMOJI_MAP
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, emotion_chip, spacer
from components.footer import render_footer

# Try to import local summarization, fallback to API version
try:
    from services.summary_service_local import summarize_text_local, combine_emotion_and_summary
    USE_LOCAL_MODEL = True
except:
    from services.summary_service import summarize_text, combine_emotion_and_summary
    USE_LOCAL_MODEL = False

from components.emotional_summary_card import render_emotional_summary

# Configure page
set_page_config()
inject_global_styles()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "buddy_chat" not in st.session_state:
    st.session_state.buddy_chat = []
if "analysis_context" not in st.session_state:
    st.session_state.analysis_context = None

# Main container
with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "🤝 Business Buddy",
        "Your AI companion for customer emotion analysis. Understand sentiment, detect patterns, and get actionable insights."
    )
    
    spacer("md")
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">⚙️ Analysis Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        analysis_mode = st.radio(
            "Analysis Mode:",
            ["💬 Chat Mode", "🧠 Smart Summary"],
            help="Choose between single message chat or smart emotional summary"
        )
        
        spacer("sm")
        
        threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.3,
            step=0.05,
            help="Minimum probability to display an emotion"
        )
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # ==================================================================
    # CHAT MODE
    # ==================================================================
    if analysis_mode == "💬 Chat Mode":
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-user fade-in">
                    {message["content"]}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)
            else:
                # Detected emotions
                if message["emotions"]:
                    chips_html = " ".join([
                        emotion_chip(e.capitalize(), message["probabilities"][e], EMOJI_MAP.get(e, "🎭"))
                        for e in message["emotions"]
                    ])
                    st.markdown(f'<div style="margin-bottom: 0.5rem;">{chips_html}</div>', unsafe_allow_html=True)
                else:
                    st.info("No emotions detected above threshold.")
                
                # Top emotions chart
                if message["probabilities"]:
                    sorted_probs = sorted(message["probabilities"].items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    st.markdown('<div class="glass-card" style="margin-bottom: 1rem;">', unsafe_allow_html=True)
                    st.markdown("**📊 Top Emotions:**")
                    
                    for emotion, prob in sorted_probs:
                        emoji = EMOJI_MAP.get(emotion, "🎭")
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0;">
                            <span style="color: #FFFFFF;">{emoji} {emotion.capitalize()}</span>
                            <span style="color: #8A5CF6; font-weight: bold;">{prob:.1%}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        spacer("sm")
        user_input = st.text_area(
            "Type your message:",
            height=100,
            placeholder="Enter text to analyze emotions...",
            key="chat_input"
        )
        
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            if user_input.strip():
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Analyze emotions
                with st.spinner("Analyzing emotions..."):
                    predicted_emotions, probabilities = predict_emotions(user_input, threshold=threshold)
                
                # Add assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "emotions": predicted_emotions,
                    "probabilities": probabilities
                })
                
                st.rerun()
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    
    # ==================================================================
    # SMART SUMMARY MODE
    # ==================================================================
    elif analysis_mode == "🧠 Smart Summary":
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🧠 Smart Social Media Analytics</h3>
            <p style="color: #A8A9B3; line-height: 1.8;">
                Analyze customer reactions to your social media posts. Get insights about:
            </p>
            <ul style="color: #A8A9B3; line-height: 1.8;">
                <li><strong>Customer Sentiment</strong> - Emotions your posts generate</li>
                <li><strong>Engagement Quality</strong> - Positive, negative, or mixed reactions</li>
                <li><strong>Actionable Recommendations</strong> - Improve your strategy</li>
                <li><strong>Brand Health</strong> - Overall emotional perception</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        spacer("sm")
        
        st.info("💡 **Use Case**: Paste comments from Instagram, Facebook, Twitter, LinkedIn posts or product reviews.")
        
        input_text = st.text_area(
            "📝 Paste Customer Comments / Reviews / Social Media Feedback:",
            height=200,
            placeholder="Paste comments from your social media posts, reviews, or customer feedback..."
        )
        
        spacer("sm")
        
        use_enhanced_ai = st.checkbox(
            "🤖 Enable Enhanced AI Recommendations (GPT-4 + Market Research)",
            value=False,
            help="Advanced recommendations using market research database and GPT-4"
        )
        
        spacer("sm")
        
        if st.button("✨ Generate Emotional Summary", type="primary", use_container_width=True):
            if not input_text or len(input_text.strip()) == 0:
                st.error("⚠️ Please enter some text to analyze")
            else:
                # Emotion Analysis
                with st.spinner("🎭 Analyzing emotions..."):
                    predicted_emotions, probabilities = predict_emotions(input_text, threshold=threshold)
                    
                    if not predicted_emotions:
                        predicted_emotions = ["neutral"]
                        probabilities = {"neutral": 0.5}
                
                st.success("✅ Emotion analysis complete!")
                
                # Category Detection
                with st.spinner("🧩 Detecting content category..."):
                    from services.post_category_classifier import (
                        detect_post_category, 
                        get_category_emoji,
                        get_category_color
                    )
                    category_result = detect_post_category(input_text)
                
                category = category_result.get("category", "General Feedback")
                category_confidence = category_result.get("confidence", 0.0)
                category_emoji = get_category_emoji(category)
                category_color = get_category_color(category)
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {category_color}33, {category_color}11); 
                            border-left: 4px solid {category_color}; 
                            padding: 12px 20px; 
                            border-radius: 8px; 
                            margin: 10px 0;'>
                    <p style='margin: 0; font-size: 14px; font-weight: 600; color: #FFFFFF;'>
                        {category_emoji} Detected Category: <strong>{category}</strong> ({category_confidence:.0%} confidence)
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate Summary
                with st.spinner("📝 Generating AI summary..."):
                    if USE_LOCAL_MODEL:
                        summary = summarize_text_local(input_text)
                    else:
                        summary = summarize_text(input_text)
                
                st.success("✅ Summary generated!")
                
                # Combine Results
                emotion_output = {"probabilities": probabilities}
                combined_result = combine_emotion_and_summary(
                    emotion_output,
                    summary,
                    input_text,
                    use_enhanced_ai=use_enhanced_ai,
                    category_context=category_result
                )
                
                # Render Output
                render_emotional_summary(combined_result)
                
                # Download Business Report
                spacer("md")
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #FFFFFF; margin-bottom: 1rem;">💾 Export Business Report</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate metrics
                positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
                negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment"]
                
                positive_score = min(sum([prob for emotion, prob in combined_result['all_emotions'].items() if emotion in positive_emotions]), 1.0)
                negative_score = min(sum([prob for emotion, prob in combined_result['all_emotions'].items() if emotion in negative_emotions]), 1.0)
                
                if combined_result['dominant_emotion'] in positive_emotions:
                    sentiment_status = "Positive"
                    brand_health = "Healthy - Positive customer sentiment"
                elif combined_result['dominant_emotion'] in negative_emotions:
                    sentiment_status = "Negative"
                    brand_health = "Needs Attention - Address concerns"
                else:
                    sentiment_status = "Neutral/Mixed"
                    brand_health = "Monitor - Mixed reactions"
                
                # Markdown report
                download_data = f"""# Social Media Sentiment Analysis Report
**Generated by EmoSense Business Analytics**
**Date:** {pd.Timestamp.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 📊 Executive Summary

**Brand Health:** {brand_health}
**Overall Sentiment:** {sentiment_status}
**Customer Emotion:** {combined_result['dominant_emotion'].capitalize()} ({combined_result['confidence']:.1%})

---

## 📝 Customer Feedback Summary

{combined_result['summary']}

---

## 💡 Key Insights

**Reasoning:**
{combined_result['reasoning']}

---

## 📈 Sentiment Metrics

- Positive Score: {positive_score:.1%}
- Negative Score: {negative_score:.1%}
- Confidence: {combined_result['confidence']:.1%}

---

## 🎭 Emotion Breakdown

"""
                for emotion, prob in sorted(combined_result['all_emotions'].items(), key=lambda x: x[1], reverse=True):
                    category_label = "Positive" if emotion in positive_emotions else "Negative" if emotion in negative_emotions else "Neutral"
                    download_data += f"- **{emotion.capitalize()}**: {prob:.1%} ({category_label})\n"
                
                download_data += f"""
---

## 🎯 Recommended Actions

{combined_result['suggested_action']}

---

## 📋 Original Feedback

{input_text}

---

*Generated by EmoSense AI*
"""
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Report (MD)",
                        data=download_data,
                        file_name=f"business_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col2:
                    business_json = {
                        "report_metadata": {
                            "generated_at": pd.Timestamp.now().isoformat(),
                            "report_type": "social_media_sentiment",
                            "tool": "EmoSense Business Analytics"
                        },
                        "brand_health": {
                            "status": brand_health,
                            "sentiment": sentiment_status,
                            "positive_score": f"{positive_score:.2%}",
                            "negative_score": f"{negative_score:.2%}"
                        },
                        "dominant_emotion": {
                            "emotion": combined_result['dominant_emotion'],
                            "confidence": f"{combined_result['confidence']:.2%}"
                        },
                        "summary": combined_result['summary'],
                        "reasoning": combined_result['reasoning'],
                        "all_emotions": {k: f"{v:.2%}" for k, v in combined_result['all_emotions'].items()},
                        "actions": combined_result['suggested_action'],
                        "feedback": input_text
                    }
                    
                    json_data = json.dumps(business_json, indent=2)
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_data,
                        file_name=f"analytics_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                # Store analysis context for chat
                st.session_state.analysis_context = {
                    "input_text": input_text,
                    "summary": combined_result['summary'],
                    "dominant_emotion": combined_result['dominant_emotion'],
                    "all_emotions": combined_result['all_emotions'],
                    "reasoning": combined_result['reasoning'],
                    "suggested_action": combined_result['suggested_action'],
                    "category": category,
                    "sentiment_status": sentiment_status,
                    "brand_health": brand_health
                }
                
                # Business Buddy Chat Feature
                spacer("lg")
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color: #FFFFFF; margin-bottom: 0.5rem;">💬 Chat with Business Buddy</h3>
                    <p style="color: #A8A9B3;">Have questions about your analysis? Chat with Business Buddy for deeper insights!</p>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("sm")
                
                # Display chat history
                if st.session_state.buddy_chat:
                    for chat_msg in st.session_state.buddy_chat:
                        if chat_msg["role"] == "user":
                            st.markdown(f"""
                            <div class="message-user fade-in">
                                {chat_msg['content']}
                            </div>
                            <div style="clear: both;"></div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="message-ai fade-in">
                                {chat_msg['content']}
                            </div>
                            <div style="clear: both;"></div>
                            """, unsafe_allow_html=True)
                    spacer("sm")
                
                # Chat input
                user_question = st.text_input(
                    "Ask Business Buddy:",
                    placeholder="e.g., What should I focus on first? How can I improve negative sentiment?",
                    key="buddy_question"
                )
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("💬 Ask Buddy", type="primary", use_container_width=True):
                        if user_question.strip():
                            # Add user question to chat
                            st.session_state.buddy_chat.append({
                                "role": "user",
                                "content": user_question
                            })
                            
                            # Generate contextual response
                            context = st.session_state.analysis_context
                            
                            # Smart contextual responses
                            question_lower = user_question.lower()
                            
                            if "focus" in question_lower or "priority" in question_lower or "first" in question_lower:
                                if context['sentiment_status'] == "Negative":
                                    response = f"""Based on your analysis showing **{context['dominant_emotion']}** as the dominant emotion, I recommend:

1. **Address negative sentiment immediately** - Your brand health status is "{context['brand_health']}"
2. **Review the specific comments** causing {context['dominant_emotion']} - understand the root cause
3. **Implement the suggested actions**: {context['suggested_action'][:200]}...
4. **Monitor response** after making changes

The priority is damage control and rebuilding trust."""
                                else:
                                    response = f"""Great news! Your sentiment is **{context['sentiment_status']}** with **{context['dominant_emotion']}** as the dominant emotion.

Focus areas:
1. **Amplify what's working** - your customers are responding positively!
2. **Engage with positive commenters** to build loyalty
3. **Apply these insights**: {context['suggested_action'][:200]}...
4. **Scale successful strategies** across other channels"""
                            
                            elif "improve" in question_lower or "fix" in question_lower or "negative" in question_lower:
                                response = f"""To improve negative sentiment and address **{context['dominant_emotion']}** emotions:

**Immediate Actions:**
- Acknowledge customer concerns publicly
- Show empathy and understanding
- Provide clear solutions or timelines

**Strategic Improvements:**
{context['suggested_action']}

**Category-specific tip for {context['category']}:**
- If this is a recurring theme, consider a proactive communication strategy
- Set up monitoring alerts for similar sentiment spikes"""
                            
                            elif "emotion" in question_lower or "feel" in question_lower:
                                top_emotions = sorted(context['all_emotions'].items(), key=lambda x: x[1], reverse=True)[:3]
                                emotion_text = ", ".join([f"**{e[0].capitalize()}** ({e[1]:.1%})" for e in top_emotions])
                                response = f"""Your customers are primarily feeling: {emotion_text}

**Emotional Breakdown:**
{context['reasoning']}

**What this means:**
The emotional tone is **{context['sentiment_status']}** overall. These emotions indicate {context['brand_health'].lower()}.

Understanding these emotions helps you craft responses that resonate emotionally with your audience."""
                            
                            elif "category" in question_lower or "type" in question_lower:
                                response = f"""This feedback falls under **{context['category']}** category.

**Why this matters:**
- Different categories require different response strategies
- {context['category']} typically involves {context['reasoning'][:150]}...

**Best practices for {context['category']}:**
- Respond promptly (within 24 hours for negative feedback)
- Use category-specific language and tone
- Track patterns over time in this category"""
                            
                            elif "action" in question_lower or "do" in question_lower or "next" in question_lower:
                                response = f"""Here's your action plan:

**Suggested Actions:**
{context['suggested_action']}

**Next Steps:**
1. Download the full report (MD or JSON format above)
2. Share insights with your team
3. Implement top 2-3 recommendations this week
4. Monitor sentiment changes after implementation
5. Return to Business Buddy for follow-up analysis

Would you like me to elaborate on any specific action?"""
                            
                            elif "summary" in question_lower or "overview" in question_lower:
                                response = f"""**Quick Summary:**

{context['summary']}

**Key Metrics:**
- Dominant Emotion: {context['dominant_emotion'].capitalize()}
- Sentiment: {context['sentiment_status']}
- Brand Health: {context['brand_health']}
- Category: {context['category']}

This gives you a high-level view of customer sentiment. Need specifics on any area?"""
                            
                            else:
                                # Generic helpful response
                                response = f"""I'm here to help you understand your analysis! 

**Your Analysis Summary:**
- Dominant emotion: **{context['dominant_emotion'].capitalize()}**
- Sentiment: **{context['sentiment_status']}**
- Brand health: {context['brand_health']}

**I can help you with:**
- Understanding specific emotions in detail
- Prioritizing actions and next steps
- Strategies to improve sentiment
- Interpreting the category classification
- Creating an action plan

What would you like to know more about?"""
                            
                            # Add buddy response to chat
                            st.session_state.buddy_chat.append({
                                "role": "assistant",
                                "content": response
                            })
                            
                            st.rerun()
                        else:
                            st.warning("⚠️ Please enter a question.")
                
                with col2:
                    if st.button("🗑️ Clear Chat", use_container_width=True):
                        st.session_state.buddy_chat = []
                        st.rerun()
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
