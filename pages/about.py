"""
About EmoSense AI - Complete Information Page
Redesigned with section cards and modern layout
"""
import streamlit as st
from components.layout import set_page_config, page_container, hero_section, section_card, spacer
from components.footer import render_footer

# Configure page
set_page_config()

# Main container
with page_container():
    # Hero Section
    hero_section(
        title="About EmoSense AI",
        subtitle="Emotion understanding made intelligent, empathetic, and actionable.",
        detail=""
    )
    
    spacer("md")
    
    # Welcome Section
    def welcome_content():
        st.markdown("""
        EmoSense AI is an advanced emotional-intelligence analytics platform designed to help 
        individuals and businesses understand human emotion at scale.
        
        <ul class="feature-list">
            <li>Deep emotional insights powered by state-of-the-art AI</li>
            <li>Context-aware summarization for meaningful understanding</li>
            <li>Business-ready intelligence for actionable strategies</li>
            <li>Real-time personal emotional guidance and reflection</li>
        </ul>
        
        <p style="color: #a5b4fc; font-weight: 600; margin-top: 1.5rem;">
            Our mission is to make emotional understanding accessible, intelligent, and useful.
        </p>
        """, unsafe_allow_html=True)
    
    section_card("Welcome to EmoSense AI", "🧠", welcome_content)
    
    spacer("sm")
    
    # Who is EmoSense for?
    def audience_content():
        st.markdown("""
        <ul class="feature-list">
            <li><strong>Individuals</strong> seeking emotional awareness and personal growth</li>
            <li><strong>Content Creators</strong> wanting to understand audience sentiment</li>
            <li><strong>Brands & Marketers</strong> analyzing customer feedback at scale</li>
            <li><strong>CX Teams</strong> improving customer experience through emotion insights</li>
            <li><strong>Researchers</strong> studying emotional patterns in text data</li>
            <li><strong>Mental Health Advocates</strong> (as a complementary reflection tool)</li>
        </ul>
        """, unsafe_allow_html=True)
    
    section_card("Who is EmoSense For?", "🎯", audience_content)
    
    spacer("sm")
    
    # How the Tech Works
    def tech_content():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🤖 Emotion Detection (BERT)**  
            Recognizes 28 nuanced emotions using Google's BERT model trained on the GoEmotions dataset.
            
            **📝 Summarization (BART/PEGASUS)**  
            Produces context-aware summaries that capture the essence of emotional content.
            
            **🏷️ Category Detection (BART-MNLI)**  
            Classifies content into 9 categories for deeper contextual understanding.
            """)
        
        with col2:
            st.markdown("""
            **🧠 Smart Analytics (GPT-4o-mini + RAG)**  
            Hybrid recommendation engine combining GPT-4 with Retrieval-Augmented Generation.
            
            **💾 Knowledge Base (ChromaDB)**  
            Vector database storing real market research and best practices.
            
            **🔍 Semantic Search (sentence-transformers)**  
            Finds relevant context using advanced embedding models.
            """)
        
        spacer("sm")
        st.info("💡 **All models run efficiently** with memory optimization for cloud deployment.")
    
    section_card("How the Tech Works", "🛠️", tech_content)
    
    spacer("sm")
    
    # Built By Section
    def creator_content():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">👩‍💻</div>
                <h3 style="color: #a5b4fc; margin-bottom: 0.5rem;">Amarnoor Kaur</h3>
                <p style="color: #cbd5e1; margin-bottom: 1rem;">Founder & Lead Developer</p>
                <p style="color: #94a3b8;">
                    📧 <a href="mailto:amar.noor.work@gmail.com">amar.noor.work@gmail.com</a><br/>
                    📍 Canada
                </p>
                <div style="margin-top: 1.5rem;">
                    <a href="https://www.linkedin.com" style="color: #667eea; text-decoration: none; font-weight: 600;">
                        🔗 Connect on LinkedIn
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    section_card("Built By", "🖤", creator_content)
    
    spacer("lg")

# Footer
render_footer()
