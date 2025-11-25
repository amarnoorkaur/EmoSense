"""
EmoSense AI - Premium Landing Page
Modern glassmorphic design with animations and premium AI startup aesthetics
Version: 2.0
"""
import streamlit as st
from components.layout import set_page_config, inject_global_styles, page_container, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# Custom CSS for premium landing page
st.markdown("""
<style>
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(138, 92, 246, 0.4); }
    50% { box-shadow: 0 0 40px rgba(138, 92, 246, 0.8); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

.premium-hero {
    position: relative;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 32px;
    padding: 5rem 2rem;
    text-align: center;
    margin-bottom: 3rem;
    overflow: hidden;
    animation: fadeInUp 1s ease-out;
}

.premium-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}

.premium-hero h1 {
    font-size: 4.5rem;
    font-weight: 900;
    color: #FFFFFF;
    margin-bottom: 1rem;
    position: relative;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    letter-spacing: -2px;
}

.premium-hero p {
    font-size: 1.5rem;
    color: rgba(255,255,255,0.95);
    margin-bottom: 2.5rem;
    position: relative;
    font-weight: 400;
}

.cta-container {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    position: relative;
    margin-top: 2rem;
}

.cta-btn {
    padding: 1rem 2.5rem;
    border-radius: 50px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.cta-primary {
    background: rgba(255,255,255,0.95);
    color: #667eea;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.cta-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.cta-secondary {
    background: rgba(255,255,255,0.15);
    color: #FFFFFF;
    border: 2px solid rgba(255,255,255,0.4);
    backdrop-filter: blur(10px);
}

.cta-secondary:hover {
    background: rgba(255,255,255,0.25);
    transform: translateY(-3px);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
    animation: fadeInUp 1s ease-out 0.2s both;
}

.feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    transition: all 0.3s ease;
    backdrop-filter: blur(20px);
}

.feature-card:hover {
    transform: scale(1.03) translateY(-5px);
    box-shadow: 0 20px 60px rgba(138, 92, 246, 0.3);
    border-color: rgba(138, 92, 246, 0.3);
}

.feature-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    box-shadow: 0 10px 30px rgba(138, 92, 246, 0.4);
}

.feature-card h3 {
    color: #FFFFFF;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.feature-card p {
    color: #A8A9B3;
    line-height: 1.7;
    font-size: 1rem;
}

.pipeline-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 3rem 2rem;
    margin: 3rem 0;
    animation: fadeInUp 1s ease-out 0.4s both;
}

.pipeline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.pipeline-step {
    flex: 1;
    min-width: 120px;
    background: rgba(138, 92, 246, 0.1);
    border: 2px solid rgba(138, 92, 246, 0.3);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
}

.pipeline-step:hover {
    background: rgba(138, 92, 246, 0.2);
    border-color: rgba(138, 92, 246, 0.6);
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(138, 92, 246, 0.4);
}

.pipeline-step::after {
    content: '→';
    position: absolute;
    right: -1.5rem;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(138, 92, 246, 0.5);
    font-size: 1.5rem;
}

.pipeline-step:last-child::after {
    content: '';
}

.pipeline-step h4 {
    color: #FFFFFF;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0;
}

.testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
    animation: fadeInUp 1s ease-out 0.6s both;
}

.testimonial-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2rem;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
}

.testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(138, 92, 246, 0.2);
}

.testimonial-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.testimonial-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.testimonial-info h4 {
    color: #FFFFFF;
    font-size: 1rem;
    margin: 0 0 0.25rem 0;
}

.testimonial-info p {
    color: #A8A9B3;
    font-size: 0.85rem;
    margin: 0;
}

.stars {
    color: #FFD700;
    font-size: 1.2rem;
    margin-bottom: 1rem;
}

.testimonial-text {
    color: #C4C5D0;
    line-height: 1.7;
    font-style: italic;
}

.final-cta {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 32px;
    padding: 5rem 2rem;
    text-align: center;
    margin: 4rem 0 2rem 0;
    animation: fadeInUp 1s ease-out 0.8s both;
}

.final-cta h2 {
    font-size: 3rem;
    color: #FFFFFF;
    margin-bottom: 2rem;
    font-weight: 800;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    color: #FFFFFF;
    margin: 4rem 0 2rem 0;
    font-weight: 800;
    animation: fadeInUp 1s ease-out;
}

.carousel-container {
    overflow-x: auto;
    display: flex;
    gap: 2rem;
    padding: 2rem 0;
    margin: 2rem 0;
    animation: fadeInUp 1s ease-out 0.5s both;
}

.carousel-item {
    min-width: 400px;
    height: 250px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
    backdrop-filter: blur(10px);
}

.carousel-item:hover {
    transform: scale(1.03);
    box-shadow: 0 15px 50px rgba(138, 92, 246, 0.3);
}

.carousel-item-icon {
    font-size: 4rem;
}

.carousel-item-title {
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 600;
}

@media (max-width: 768px) {
    .premium-hero h1 { font-size: 2.5rem; }
    .premium-hero p { font-size: 1.1rem; }
    .pipeline { flex-direction: column; }
    .pipeline-step::after { content: '↓'; right: 50%; top: auto; bottom: -1.5rem; }
    .carousel-item { min-width: 300px; height: 200px; }
}
</style>
""", unsafe_allow_html=True)

# Main container
with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # PREMIUM HERO SECTION
    st.markdown("""
    <div class="premium-hero">
        <h1>EmoSense AI</h1>
        <p>Emotion-aware AI for humans and brands.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        btn_col1, btn_col2, btn_col3 = st.columns(3, gap="medium")
        
        with btn_col1:
            if st.button("💛 Personal Companion", use_container_width=True, type="primary"):
                st.switch_page("pages/Personal_Chatbot.py")
        
        with btn_col2:
            if st.button("🤝 Business Buddy", use_container_width=True, type="primary"):
                st.switch_page("pages/Business_Chatbot.py")
                
        with btn_col3:
            if st.button("🎯 Try Demo", use_container_width=True, type="secondary"):
                st.switch_page("pages/Business_Chatbot.py")
    
    spacer("lg")
    spacer("lg")
    
    # FEATURES SECTION
    st.markdown('<h2 class="section-title">Powerful Features</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3>Emotion Detection</h3>
            <p>Advanced BERT model identifies 28 distinct emotions with high accuracy from any text input.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3>Viral Signal Prediction</h3>
            <p>Detect content with viral potential using our proprietary signal detection algorithms.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Root Cause Reasoning</h3>
            <p>Uncover the underlying reasons behind customer emotions and pain points automatically.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <h3>Smart Business Insights</h3>
            <p>Get actionable recommendations powered by GPT-4 and research-backed strategies.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Sentiment Dashboard</h3>
            <p>Beautiful visualizations showing emotion breakdowns, trends, and key metrics.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">💛</div>
            <h3>Personal Emotion Journey</h3>
            <p>Track your emotional patterns over time with gentle AI-powered guidance.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # HOW IT WORKS - VISUAL PIPELINE
    st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline">
            <div class="pipeline-step">
                <h4>Emotion Detection</h4>
            </div>
            <div class="pipeline-step">
                <h4>Summaries</h4>
            </div>
            <div class="pipeline-step">
                <h4>Sentiment Analysis</h4>
            </div>
            <div class="pipeline-step">
                <h4>RAG Insights</h4>
            </div>
            <div class="pipeline-step">
                <h4>Recommendations</h4>
            </div>
            <div class="pipeline-step">
                <h4>Crisis Detection</h4>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # PRODUCT SCREENSHOTS CAROUSEL
    st.markdown('<h2 class="section-title">Product Showcase</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="carousel-container">
        <div class="carousel-item">
            <div class="carousel-item-icon">🤝</div>
            <div class="carousel-item-title">Business Buddy Dashboard</div>
        </div>
        <div class="carousel-item">
            <div class="carousel-item-icon">💛</div>
            <div class="carousel-item-title">Personal Companion UI</div>
        </div>
        <div class="carousel-item">
            <div class="carousel-item-icon">📈</div>
            <div class="carousel-item-title">Emotion Charts</div>
        </div>
        <div class="carousel-item">
            <div class="carousel-item-icon">🚀</div>
            <div class="carousel-item-title">Viral Signal UI</div>
        </div>
        <div class="carousel-item">
            <div class="carousel-item-icon">🔍</div>
            <div class="carousel-item-title">Root Cause Clustering</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # TESTIMONIALS
    st.markdown('<h2 class="section-title">What People Say</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="testimonial-grid">
        <div class="testimonial-card">
            <div class="testimonial-header">
                <div class="testimonial-avatar">👨</div>
                <div class="testimonial-info">
                    <h4>Alex Chen</h4>
                    <p>Product Manager</p>
                </div>
            </div>
            <div class="stars">★★★★★</div>
            <p class="testimonial-text">
                "EmoSense transformed how we understand customer feedback. The emotion detection is incredibly accurate and the insights are actionable."
            </p>
        </div>
        
        <div class="testimonial-card">
            <div class="testimonial-header">
                <div class="testimonial-avatar">👩</div>
                <div class="testimonial-info">
                    <h4>Sarah Johnson</h4>
                    <p>Marketing Director</p>
                </div>
            </div>
            <div class="stars">★★★★★</div>
            <p class="testimonial-text">
                "The viral signal detection helped us identify and amplify content that resonates. Our engagement increased by 300%."
            </p>
        </div>
        
        <div class="testimonial-card">
            <div class="testimonial-header">
                <div class="testimonial-avatar">🧑</div>
                <div class="testimonial-info">
                    <h4>Michael Rodriguez</h4>
                    <p>Startup Founder</p>
                </div>
            </div>
            <div class="stars">★★★★★</div>
            <p class="testimonial-text">
                "Finally, an AI tool that truly understands emotions. The personal companion helped me understand my stress patterns better."
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    spacer("lg")
    
    # FINAL CTA SECTION
    st.markdown("""
    <div class="final-cta">
        <h2>Experience Emotion-Aware AI</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Final CTA Button
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, type="primary", key="final_cta"):
            st.switch_page("pages/Business_Chatbot.py")
    
    spacer("lg")
    
    # Technology Showcase
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 2.5rem; margin-top: 3rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; backdrop-filter: blur(20px);">
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
