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
        
        ### ✨ Key Features
        
        - **28 Emotion Detection** - Fine-grained emotion analysis powered by BERT
        - **Smart Summarization** - Condense long feedback using BART/PEGASUS
        - **Category Detection** - Automatically classify content into 9 categories
        - **AI-Powered Insights** - Get actionable recommendations via GPT-4
        - **Bulk Analysis** - Process thousands of comments at scale
        - **RAG Integration** - Context-aware suggestions from market research
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
    
    # Card 3: How the Technology Works
    def card3_content():
        st.markdown("""
        EmoSense combines cutting-edge NLP models in a powerful AI pipeline:
        
        ### 🤖 BERT Emotion Detection
        
        **Model:** `j-hartmann/emotion-english-distilroberta-base`  
        **Trained on:** 28 fine-grained emotion labels  
        **Capability:** Detects joy, sadness, anger, fear, love, surprise, and 22+ nuanced emotions
        
        Our emotion detection uses a transformer-based model fine-tuned specifically for emotional 
        classification. It analyzes text at a deep semantic level, understanding context and subtle 
        emotional cues.
        
        ### 📝 BART/PEGASUS Summarization
        
        **Models:** `facebook/bart-large-cnn`, `google/pegasus-xsum`  
        **Purpose:** Condense long text while preserving emotional essence  
        **Use Case:** Summarize hundreds of comments into actionable insights
        
        Summarization helps businesses process large volumes of feedback efficiently, extracting 
        the core emotional narrative without losing critical details.
        
        ### 🎯 BART-MNLI Category Detection
        
        **Model:** `facebook/bart-large-mnli`  
        **Categories:** Product Reviews, Customer Support, Social Media, Marketing, HR, etc.  
        **Accuracy:** Zero-shot classification with high confidence
        
        Category detection routes feedback to appropriate teams and enables category-specific 
        emotional analysis.
        
        ### 🧠 GPT-4 + RAG Recommendations
        
        **Model:** `gpt-4o-mini` via OpenAI API  
        **Enhanced with:** ChromaDB vector database containing market research  
        **Output:** Context-aware, actionable recommendations tailored to your industry
        
        Our RAG (Retrieval-Augmented Generation) system queries a proprietary knowledge base of 
        emotional intelligence best practices, delivering personalized strategies for improvement.
        
        ### 🔗 Integration Architecture
        
        ```
        User Input
            ↓
        [BERT] → Emotion Detection → 28 emotion probabilities
            ↓
        [BART-MNLI] → Category Classification → Content type
            ↓
        [BART/PEGASUS] → Summarization → Condensed insights
            ↓
        [ChromaDB] → Knowledge Retrieval → Relevant research
            ↓
        [GPT-4] → Recommendation Generation → Actionable strategies
            ↓
        Beautiful Dashboard
        ```
        
        ### 🔒 Privacy & Security
        
        - **No data storage**: Your input is processed in real-time and not saved
        - **Local models**: BERT and BART run on our secure infrastructure
        - **API encryption**: All API calls use HTTPS with key authentication
        - **Optional AI**: Enhanced features (GPT-4) are opt-in
        """, unsafe_allow_html=True)
    
    section_card("🛠️ How the Technology Works", "⚙️", card3_content)
    
    spacer("md")
    
    # Card 4: Built by Amarnoor Kaur
    def card4_content():
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
    
    section_card("🖤 Built with Purpose", "💝", card4_content)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
