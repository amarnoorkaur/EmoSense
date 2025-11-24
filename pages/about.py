"""
About EmoSense AI - Technology & Features
"""
import streamlit as st

def render_about_page():
    """Render the about page"""
    
    st.markdown("""
    <style>
    .about-section {
        background: linear-gradient(145deg, #f8f9ff 0%, #ffffff 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .tech-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("About EmoSense AI 🎭")
    
    st.markdown("""
    <div class="about-section">
        <h2>🌟 What is EmoSense AI?</h2>
        <p style="font-size: 18px; line-height: 1.8;">
            EmoSense AI is a cutting-edge emotional intelligence platform that combines multiple AI technologies 
            to understand, analyze, and provide insights on human emotions expressed in text. Whether you're 
            seeking personal emotional awareness or business intelligence from customer feedback, EmoSense delivers 
            deep, actionable insights powered by state-of-the-art machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🤖 Our AI Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tech-card">
            <h3>🧠 BERT Emotion Detection</h3>
            <p><strong>Model:</strong> Amarnoor/emotion-bert-emosense</p>
            <p><strong>Capability:</strong> Detects 28 distinct emotions from the GoEmotions dataset</p>
            <p><strong>Accuracy:</strong> Multi-label classification with confidence scoring</p>
            <ul>
                <li>Joy, Sadness, Anger, Fear</li>
                <li>Love, Surprise, Gratitude</li>
                <li>Pride, Relief, Excitement</li>
                <li>And 18 more nuanced emotions!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tech-card">
            <h3>🔍 Category Classification</h3>
            <p><strong>Model:</strong> facebook/bart-large-mnli</p>
            <p><strong>Capability:</strong> Context-aware content categorization</p>
            <p><strong>Categories:</strong> 9 types</p>
            <ul>
                <li>Product Reviews</li>
                <li>Service Complaints</li>
                <li>Support Queries</li>
                <li>Technical Issues</li>
                <li>Feature Requests</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card">
            <h3>📝 BART Summarization</h3>
            <p><strong>Model:</strong> facebook/bart-large-cnn</p>
            <p><strong>Capability:</strong> Intelligent text summarization</p>
            <p><strong>Use Case:</strong> Condense long feedback into key insights</p>
            <ul>
                <li>Extractive + Abstractive</li>
                <li>Context-preserving</li>
                <li>Emotion-aware summaries</li>
                <li>Fast local inference</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tech-card">
            <h3>🧠 GPT-4 Enhanced Insights</h3>
            <p><strong>Model:</strong> gpt-4o-mini</p>
            <p><strong>Capability:</strong> Context-aware recommendations</p>
            <p><strong>Powered by:</strong> RAG (Retrieval-Augmented Generation)</p>
            <ul>
                <li>Market research integration</li>
                <li>Industry best practices</li>
                <li>Personalized strategies</li>
                <li>Data-driven actions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Key Features")
    
    features = st.tabs(["Personal", "Business", "Technical"])
    
    with features[0]:
        st.markdown("""
        ### 💛 Personal Emotion Companion
        
        - **Safe Space**: Express yourself without judgment
        - **Emotion Tracking**: Monitor your emotional patterns over time
        - **Empathetic AI**: Receives context-appropriate responses
        - **Insights Journal**: Review your emotional journey
        - **Privacy First**: Your conversations stay with you
        
        Perfect for self-reflection, emotional awareness, and mental wellness tracking.
        """)
    
    with features[1]:
        st.markdown("""
        ### 📊 Business Intelligence
        
        - **Sentiment Analysis**: Understand customer emotions at scale
        - **Category Detection**: Automatically classify feedback types
        - **Batch Processing**: Analyze hundreds of comments instantly
        - **Visual Dashboards**: Beautiful charts and metrics
        - **AI Recommendations**: Data-driven business strategies
        - **Export Reports**: Download insights as CSV/JSON
        - **Market Research**: Backed by HubSpot, Zendesk, Forrester data
        
        Transform customer feedback into competitive advantage.
        """)
    
    with features[2]:
        st.markdown("""
        ### ⚙️ Technical Capabilities
        
        **AI Models:**
        - BERT (emotion detection)
        - BART (summarization & classification)
        - GPT-4o-mini (insights generation)
        
        **Vector Database:**
        - ChromaDB for semantic search
        - Sentence-transformers embeddings
        - 6+ research documents indexed
        
        **Performance:**
        - Real-time analysis (<2s per text)
        - Batch processing (100+ texts/minute)
        - Memory-optimized deployment
        - Streamlit Cloud compatible
        
        **Privacy & Security:**
        - No data storage by default
        - Optional OpenAI API usage
        - Local model fallbacks
        - GDPR-friendly architecture
        """)
    
    st.markdown("---")
    st.markdown("""
    <div class="about-section">
        <h2>📈 Use Cases</h2>
        <ul style="font-size: 16px; line-height: 2;">
            <li><strong>Social Media Managers:</strong> Track audience sentiment across campaigns</li>
            <li><strong>Customer Success:</strong> Identify at-risk customers from support tickets</li>
            <li><strong>Product Teams:</strong> Prioritize features based on emotional feedback</li>
            <li><strong>Marketing:</strong> Optimize messaging for emotional resonance</li>
            <li><strong>HR & People Ops:</strong> Gauge employee sentiment anonymously</li>
            <li><strong>Mental Health:</strong> Track personal emotional wellbeing</li>
            <li><strong>Researchers:</strong> Analyze qualitative data at scale</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("AI Models", "4", help="BERT, BART, GPT-4, Sentence-Transformers")
    with col2:
        st.metric("Emotions", "28", help="From GoEmotions dataset")
    with col3:
        st.metric("Categories", "9", help="Content type classification")
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.info("""
    **Built with ❤️ by the EmoSense Team**  
    Powered by Streamlit, Hugging Face Transformers, OpenAI, and ChromaDB
    
    © 2025 EmoSense AI. All rights reserved.
    """)
