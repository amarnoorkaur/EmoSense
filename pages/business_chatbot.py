"""
Business Intelligence Chatbot - Category-aware analytics
"""
import streamlit as st

def render_business_chatbot():
    """Render the business intelligence chatbot page"""
    
    st.markdown("""
    <style>
    .business-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .business-title {
        font-size: 36px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="business-hero">
        <h1 class="business-title">📊 Business Emotional Insights</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 18px;">
            Transform customer feedback into actionable business intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Import and render the Smart Summary functionality
    st.info("💼 **Business Features**: Category detection, sentiment analysis, RAG-powered insights, GPT-4 recommendations")
    
    # This would normally import the Smart Summary section from app.py
    st.markdown("### 🚀 Coming Soon: Dedicated Business Analytics Interface")
    st.markdown("""
    For now, please use the **Smart Emotional Summary** mode from the main app.
    
    This page will soon feature:
    - Real-time dashboard
    - Historical trend analysis  
    - Multi-platform integration
    - Custom reports
    """)
