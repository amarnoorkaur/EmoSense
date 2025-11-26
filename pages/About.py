"""
About EmoSense AI - Glassmorphic Design
Four clean cards explaining mission, audience, technology, and creator
"""
import streamlit as st
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, section_card, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# Main container
with page_container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "About EmoSense AI",
        "Understanding emotions through artificial intelligence. Building empathy at scale."
    )
    
    spacer("lg")
    
    # Card 1: What is EmoSense?
    def card1_content():
        st.markdown("""
        **EmoSense AI** is an advanced emotion analysis platform that helps individuals and businesses 
        understand emotional patterns in text using state-of-the-art machine learning.
        
        ### 🎯 Our Mission
        
        To make emotional intelligence accessible through AI, enabling better self-awareness, 
        deeper customer insights, and more empathetic communication.
        
        ### ✨ Personal Companion Features
        
        - **5 Unique Personalities** - Choose from Friendly, Calm, Big Sister, Funny, or Deep Thinker
        - **5 Conversation Modes** - Casual Chat, Comfort Me, Help Me Reflect, Hype Me Up, Just Listen
        - **Continuous Conversations** - Chat naturally with memory of past exchanges
        - **Emotional Trend Analysis** - Track your emotional patterns over time
        - **Crisis Detection** - Immediate support with grounding techniques when needed
        - **28 Emotion Analysis** - Fine-grained emotion detection powered by BERT
        - **Selective Analysis** - Emotion analysis when you need it, not on every message
        
        ### 💼 Business Buddy Features
        
        - **Virality Predictor** - Detect viral potential with 6 emotional signals
        - **Crisis Radar** - Spot urgent issues before they escalate
        - **Root Cause Analysis** - Uncover the "why" behind sentiment patterns
        - **Smart Summaries** - Condense thousands of comments instantly
        - **Sentiment Dashboard** - Real-time emotion breakdown with charts
        - **Category Classifier** - Auto-sort feedback into 9 business categories
        - **Bulk Analysis** - Process thousands of comments at scale
        - **AI-Powered Insights** - Get actionable recommendations via GPT-4
        """, unsafe_allow_html=True)
    
    section_card("🧠 What is EmoSense?", "🎭", card1_content)
    
    spacer("md")
    
    # Card 2: Who is it for?
    def card2_content():
        st.markdown("""
        EmoSense AI serves diverse audiences seeking to understand emotional data:
        
        ### 🧘 Individuals
        - Track personal emotional patterns over time
        - Gain self-awareness through journaling analysis
        - Reflect on feelings with AI guidance
        
        ### 🎨 Content Creators & Influencers
        - Understand audience reactions to posts
        - Optimize content based on emotional engagement
        - Track sentiment across platforms
        
        ### 🏢 Brands & Marketers
        - Analyze customer sentiment at scale
        - Monitor brand health through social listening
        - Identify emotional triggers in campaigns
        
        ### 📞 Customer Experience Teams
        - Detect patterns in support conversations
        - Prioritize urgent emotional issues
        - Improve response strategies
        
        ### 🔬 Researchers & Analysts
        - Study emotional trends in text data
        - Generate insights from qualitative feedback
        - Export structured emotion data
        
        ### 💼 HR & People Ops
        - Understand employee sentiment in surveys
        - Detect early signs of burnout or dissatisfaction
        - Foster empathetic workplace culture
        """, unsafe_allow_html=True)
    
    section_card("🎯 Who is it for?", "👥", card2_content)
    
    spacer("md")
    
    # Card 3: Built by Amarnoor Kaur
    def card3_content():
        st.markdown("""
        EmoSense AI was created by **Amarnoor Kaur**, a passionate AI engineer and emotional 
        intelligence advocate.
        
        ### 💜 Vision
        
        "I believe technology should help us understand ourselves and others better. EmoSense bridges 
        the gap between cold data and warm human emotion, making AI a tool for empathy."
        
        ### 🎓 Background
        
        Amarnoor specializes in Natural Language Processing and transformer models, with a focus on 
        emotion AI and human-centered design. This project combines technical expertise with a deep 
        commitment to mental health awareness.
        
        ### 📬 Get in Touch
        
        - **Email:** [amarnoorkaur@example.com](mailto:amarnoorkaur@example.com)
        - **LinkedIn:** [linkedin.com/in/amarnoorkaur](https://linkedin.com/in/amarnoorkaur)
        - **GitHub:** [github.com/amarnoorkaur](https://github.com/amarnoorkaur)
        
        ### 🤝 Collaboration
        
        Interested in custom emotion AI solutions, partnerships, or contributing to EmoSense? 
        Let's connect!
        
        ---
        
        **Special Thanks:**  
        To the open-source ML community, Hugging Face for model hosting, and everyone who believes 
        technology can be a force for emotional well-being. 💛
        """, unsafe_allow_html=True)
    
    section_card("🖤 Built with Purpose", "💝", card3_content)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
