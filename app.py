"""
EmoSense AI - Landing Page
Beautiful, modern home page with hero section and feature cards
"""
import streamlit as st
from components.layout import set_page_config, page_container, hero_section, feature_card, spacer
from components.footer import render_footer

# Configure page
set_page_config()

# Main container
with page_container():
    # Hero Section
    hero_section(
        title="EmoSense AI",
        subtitle="Emotion-aware AI for humans and brands.",
        detail="Powered by BERT, BART, GPT-4o-mini & RAG."
    )
    
    spacer("md")
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        btn_col1, btn_col2 = st.columns(2, gap="large")
        
        with btn_col1:
            if st.button("💛 Personal Emotion Companion", use_container_width=True, type="primary"):
                st.switch_page("pages/personal_chatbot.py")
        
        with btn_col2:
            if st.button("📊 Business Emotion Intelligence", use_container_width=True, type="primary"):
                st.switch_page("pages/business_chatbot.py")
    
    spacer("lg")
    
    # Feature Cards - Two Column Layout
    st.markdown("## 🌟 What EmoSense AI Offers")
    spacer("sm")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        feature_card(
            icon="💛",
            title="For Individuals (Personal Emotion Companion)",
            features=[
                "Reflect on your day with an AI that understands emotions.",
                "Get gentle, non-judgmental suggestions.",
                "See which emotions show up in your words.",
                "Track your emotional patterns over time."
            ]
        )
    
    with col2:
        feature_card(
            icon="📊",
            title="For Businesses (Comment & Feedback Intelligence)",
            features=[
                "Upload comments or reviews in bulk.",
                "See sentiment & emotion breakdowns instantly.",
                "Get AI-powered recommendations using real market research.",
                "Turn emotional data into actionable insights."
            ]
        )
    
    spacer("lg")
    
    # How It Works Section
    st.markdown("## 🚀 How It Works")
    spacer("sm")
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #667eea; margin-bottom: 1rem;">Detect</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">
                Advanced BERT model analyzes text and identifies 28 distinct emotions with high accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧾</div>
            <h3 style="color: #667eea; margin-bottom: 1rem;">Understand</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">
                Smart summarization and category detection provide context-aware insights.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <h3 style="color: #667eea; margin-bottom: 1rem;">Act</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">
                GPT-4 + RAG delivers research-backed recommendations and actionable strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Technology Stack
    st.markdown("## 🛠️ Powered By Advanced AI")
    spacer("sm")
    
    tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)
    
    with tech_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <h4 style="color: #a5b4fc; margin-bottom: 0.5rem;">BERT</h4>
            <p style="color: #94a3b8; font-size: 0.875rem;">28 Emotions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
            <h4 style="color: #a5b4fc; margin-bottom: 0.5rem;">BART</h4>
            <p style="color: #94a3b8; font-size: 0.875rem;">Smart Summaries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
            <h4 style="color: #a5b4fc; margin-bottom: 0.5rem;">GPT-4</h4>
            <p style="color: #94a3b8; font-size: 0.875rem;">Deep Insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <h4 style="color: #a5b4fc; margin-bottom: 0.5rem;">RAG</h4>
            <p style="color: #94a3b8; font-size: 0.875rem;">Research-Backed</p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("md")
    
    # Stats
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Emotions Detected", "28", help="GoEmotions dataset labels")
    with stats_col2:
        st.metric("Content Categories", "9", help="Context-aware classification")
    with stats_col3:
        st.metric("Research Sources", "6+", help="HubSpot, Zendesk, Forrester & more")
    
    spacer("lg")
    
    # Call to Action
    st.markdown("""
    <div class="hero-gradient" style="padding: 2rem;">
        <h2 style="color: white; margin-bottom: 1rem;">Ready to understand emotions?</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
            Choose your path: Personal reflection or Business intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("md")

# Footer
render_footer()
