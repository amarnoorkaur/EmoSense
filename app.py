"""
EmoSense AI - Emotional Landing Page
Glassmorphic design with gradient hero and modern feature cards
"""
import streamlit as st
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# Main container
with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero Section
    gradient_hero(
        "EmoSense AI",
        "Emotion-aware AI for humans and brands."
    )
    
    spacer("md")
    
    # Two large CTA buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        btn_col1, btn_col2 = st.columns(2, gap="large")
        
        with btn_col1:
            if st.button("💛 Personal Emotion Companion", use_container_width=True, type="primary"):
                st.switch_page("pages/personal_chatbot.py")
        
        with btn_col2:
            if st.button("🤝 Business Buddy", use_container_width=True, type="primary"):
                st.switch_page("pages/business_chatbot.py")
    
    spacer("lg")
    
    # Two Feature Cards
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem; font-size: 1.5rem;">
                💛 For Individuals
            </h3>
            <ul class="feature-list">
                <li>Reflect on your day with an AI that understands emotions</li>
                <li>Get gentle, non-judgmental suggestions</li>
                <li>See which emotions show up in your words</li>
                <li>Track your emotional patterns over time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #FFFFFF; margin-bottom: 1rem; font-size: 1.5rem;">
                🤝 Business Buddy
            </h3>
            <ul class="feature-list">
                <li>Analyze customer comments and social media feedback</li>
                <li>Get sentiment & emotion insights with AI-powered summaries</li>
                <li>Chat with Business Buddy for deeper understanding</li>
                <li>Turn emotional data into actionable business strategies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("lg")
    
    # How It Works - 3 Cards
    st.markdown("""
    <h2 style="text-align: center; color: #FFFFFF; margin-bottom: 2rem;">
        How It Works
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">Detect</h3>
            <p style="color: #A8A9B3; line-height: 1.6;">
                Advanced BERT model analyzes text and identifies 28 distinct emotions with high accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧾</div>
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">Understand</h3>
            <p style="color: #A8A9B3; line-height: 1.6;">
                BART summaries and context-aware classifier provide deep insights into emotional content.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <h3 style="color: #FFFFFF; margin-bottom: 1rem;">Act</h3>
            <p style="color: #A8A9B3; line-height: 1.6;">
                GPT-4 + RAG delivers research-backed recommendations and actionable strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Technology Showcase
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 2.5rem;">
        <h3 style="color: #FFFFFF; margin-bottom: 1.5rem;">Powered by Advanced AI</h3>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                <p style="color: #8A5CF6; font-weight: 600; margin-bottom: 0.25rem;">BERT</p>
                <p style="color: #A8A9B3; font-size: 0.875rem;">28 Emotions</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                <p style="color: #00C4CC; font-weight: 600; margin-bottom: 0.25rem;">BART</p>
                <p style="color: #A8A9B3; font-size: 0.875rem;">Smart Summaries</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
                <p style="color: #FB7185; font-weight: 600; margin-bottom: 0.25rem;">GPT-4</p>
                <p style="color: #A8A9B3; font-size: 0.875rem;">Deep Insights</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                <p style="color: #FFD166; font-weight: 600; margin-bottom: 0.25rem;">RAG</p>
                <p style="color: #A8A9B3; font-size: 0.875rem;">Research-Backed</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Stats
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Emotions Detected", "28", help="GoEmotions dataset labels")
    
    with stat_col2:
        st.metric("Content Categories", "9", help="Context-aware classification")
    
    with stat_col3:
        st.metric("Research Sources", "6+", help="HubSpot, Zendesk, Forrester & more")
    
    spacer("lg")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
