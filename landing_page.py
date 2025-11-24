"""
EmoSense AI - Stunning Landing Page
Modern, premium UI with hero section and feature cards
"""
import streamlit as st

def render_landing_page():
    """Render the beautiful landing page"""
    
    # Hero Section with gradient background
    st.markdown("""
    <style>
    .hero-container {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 20px #fff, 0 0 30px #667eea, 0 0 40px #667eea;
        }
        to {
            text-shadow: 0 0 30px #fff, 0 0 40px #764ba2, 0 0 50px #764ba2;
        }
    }
    
    .hero-subtitle {
        font-size: 22px;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    .hero-emojis {
        font-size: 48px;
        margin: 30px 0;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 40px 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        height: 100%;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.2);
    }
    
    .feature-title {
        font-size: 28px;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 15px;
    }
    
    .feature-description {
        font-size: 16px;
        color: #64748b;
        line-height: 1.7;
        margin-bottom: 25px;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 14px 32px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">EmoSense AI</h1>
        <p class="hero-subtitle">Understand Emotions. Transform Insights.</p>
        <p class="hero-subtitle">Next-gen emotional intelligence for humans and businesses.<br/>
        Real-time analysis powered by BERT, BART, GPT-4o-mini, and RAG.</p>
        <div class="hero-emojis">
            😃 😐 😢 😡 🤩 😭 🤔 🫠
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2 class="feature-title">💛 Personal Emotion Companion</h2>
            <p class="feature-description">
                A safe space to express yourself. Real-time emotional recognition powered by EmoSense. 
                Chat with an AI that truly understands you. Get insights into your emotional patterns 
                and discover personalized coping strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ Start Personal Chatbot", key="personal", use_container_width=True, type="primary"):
            st.session_state.page = "personal_chatbot"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 class="feature-title">📊 Business Emotional Insights</h2>
            <p class="feature-description">
                Upload customer comments or social media posts and get AI-driven summaries, 
                emotion analysis, sentiment metrics, and category-aware insights. 
                Turn emotional data into actionable business intelligence.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ Start Business Analysis", key="business", use_container_width=True, type="primary"):
            st.session_state.page = "business_chatbot"
            st.rerun()
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("### 🚀 Powered By Advanced AI")
    
    tech_cols = st.columns(4)
    with tech_cols[0]:
        st.markdown('<div class="tech-badge">🤖 BERT</div>', unsafe_allow_html=True)
        st.caption("28 Emotions")
    with tech_cols[1]:
        st.markdown('<div class="tech-badge">📝 BART</div>', unsafe_allow_html=True)
        st.caption("Smart Summaries")
    with tech_cols[2]:
        st.markdown('<div class="tech-badge">🧠 GPT-4</div>', unsafe_allow_html=True)
        st.caption("Deep Insights")
    with tech_cols[3]:
        st.markdown('<div class="tech-badge">🔍 RAG</div>', unsafe_allow_html=True)
        st.caption("Research-Backed")
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # Stats Section
    stats_cols = st.columns(3)
    with stats_cols[0]:
        st.metric("Emotions Detected", "28", help="GoEmotions dataset labels")
    with stats_cols[1]:
        st.metric("Content Categories", "9", help="Context-aware classification")
    with stats_cols[2]:
        st.metric("Research Sources", "6+", help="HubSpot, Zendesk, Forrester & more")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 40px 20px; border-top: 1px solid rgba(0,0,0,0.1); margin-top: 40px;'>
        <p style='font-size: 14px; margin-bottom: 10px;'>
            Built with ❤️ using Streamlit, Transformers, OpenAI & ChromaDB
        </p>
        <p style='font-size: 12px; color: #94a3b8;'>
            © 2025 EmoSense AI. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)
