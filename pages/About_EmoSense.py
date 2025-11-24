"""
About EmoSense AI - Complete Information Page
Beautiful, gradient-styled about page with mission, features, and creator info
"""
import streamlit as st
from components.footer import render_footer

def render_about_emosense():
    """Render the complete about page"""
    
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-about {
        text-align: center;
        padding: 50px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        animation: fadeIn 1s ease-out;
    }
    
    .hero-title {
        font-size: 52px;
        font-weight: 800;
        color: white;
        margin-bottom: 15px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
    }
    
    .section-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 20px;
        padding: 35px;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        animation: fadeIn 1.2s ease-out;
    }
    
    .section-title {
        font-size: 32px;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 20px;
    }
    
    .section-content {
        font-size: 17px;
        line-height: 1.8;
        color: #334155;
    }
    
    .feature-list {
        list-style: none;
        padding-left: 0;
    }
    
    .feature-list li {
        padding: 12px 0;
        font-size: 16px;
        color: #475569;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-list li:last-child {
        border-bottom: none;
    }
    
    .creator-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 8px 32px rgba(252, 182, 159, 0.3);
    }
    
    .creator-name {
        font-size: 28px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }
    
    .creator-title {
        font-size: 18px;
        color: #64748b;
        margin-bottom: 15px;
    }
    
    .creator-contact {
        font-size: 16px;
        color: #475569;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-about">
        <h1 class="hero-title">About EmoSense AI</h1>
        <p class="hero-subtitle">Emotion understanding made intelligent, empathetic, and actionable.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown("""
    <div class="section-card">
        <h2 class="section-title">🧠 Welcome to EmoSense AI</h2>
        <div class="section-content">
            <p>EmoSense AI is an advanced emotional-intelligence analytics platform designed to help individuals and businesses understand human emotion at scale. Powered by transformer-based models, contextual summaries, and a hybrid RAG+LLM recommendation engine, EmoSense delivers:</p>
            <ul style="margin-top: 20px; line-height: 2;">
                <li>✨ <strong>Deep emotional insights</strong></li>
                <li>🎯 <strong>Context-aware summarization</strong></li>
                <li>📊 <strong>Business-ready intelligence</strong></li>
                <li>💛 <strong>Real-time personal emotional guidance</strong></li>
            </ul>
            <p style="margin-top: 20px; font-weight: 600; color: #667eea;">Our mission is to make emotional understanding accessible, intelligent, and useful.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission Section
    st.markdown("""
    <div class="section-card">
        <h2 class="section-title">🎯 Our Mission</h2>
        <div class="section-content">
            <p>To bridge the gap between human emotion and meaningful action — whether you're a brand interpreting customer feedback or an individual exploring your emotional well-being.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <div class="section-card">
        <h2 class="section-title">🔧 How EmoSense Works</h2>
        <div class="section-content">
            <ul class="feature-list">
                <li>
                    <strong style="color: #667eea; font-size: 18px;">• Emotion Detection (BERT)</strong><br/>
                    <span style="color: #64748b;">Recognizes 28 nuanced emotions with high accuracy.</span>
                </li>
                <li>
                    <strong style="color: #667eea; font-size: 18px;">• Summarization (BART/PEGASUS)</strong><br/>
                    <span style="color: #64748b;">Produces context-aware summaries.</span>
                </li>
                <li>
                    <strong style="color: #667eea; font-size: 18px;">• Smart Emotional Analytics</strong><br/>
                    <span style="color: #64748b;">Hybrid GPT-4o-mini with RAG + ChromaDB + sentence-transformers embeddings + real market research data.</span>
                </li>
                <li>
                    <strong style="color: #667eea; font-size: 18px;">• Business Intelligence</strong><br/>
                    <span style="color: #64748b;">Upload hundreds of comments and instantly get:</span>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        <li>Sentiment breakdown</li>
                        <li>Emotion distribution</li>
                        <li>Category detection</li>
                        <li>Insights</li>
                        <li>Recommendations</li>
                        <li>AI summaries</li>
                    </ul>
                </li>
                <li>
                    <strong style="color: #667eea; font-size: 18px;">• Personal Emotion Companion</strong><br/>
                    <span style="color: #64748b;">A friendly, safe AI that helps you understand your emotions better.</span>
                </li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Creator Section
    st.markdown("""
    <div class="creator-card">
        <h2 style="color: #1e293b; margin-bottom: 25px;">🖤 Created By</h2>
        <p class="creator-name">Amarnoor Kaur</p>
        <p class="creator-title">Founder & Lead Developer</p>
        <p class="creator-contact">📧 Email: <a href="mailto:amar.noor.work@gmail.com" style="color: #667eea; text-decoration: none; font-weight: 600;">amar.noor.work@gmail.com</a></p>
        <p class="creator-contact">📍 Canada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # Render footer
    render_footer()


# Main execution
if __name__ == "__main__":
    st.set_page_config(
        page_title="About - EmoSense AI",
        page_icon="🎭",
        layout="wide"
    )
    render_about_emosense()
