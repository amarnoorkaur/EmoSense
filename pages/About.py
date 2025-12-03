"""
About EmoSense AI - Glassmorphic Design
Explains mission, technology, assessments (COPE & Mini-IPIP), and creator
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
        
        - **4-Layer Adaptive AI** — Big Five personality, COPE coping styles, linguistic style matching, real-time emotion detection
        - **Full Personalization Flow** — Complete Big Five + COPE assessments for deeply personalized support
        - **Voice Chat** — Speak naturally with your AI companion
        - **5 Conversation Modes** — Casual Chat, Comfort Me, Help Me Reflect, Hype Me Up, Just Listen
        - **Crisis Detection** — Immediate support with grounding techniques when needed
        - **28 Emotion Analysis** — Fine-grained emotion detection powered by BERT
        - **Linguistic Style Matching (LSM)** — AI mirrors your communication patterns for natural conversations
        
        ### 💼 Business Buddy Features
        
        - **Virality Predictor** — Detect viral potential with 6 emotional signals
        - **Crisis Radar** — Spot urgent issues before they escalate
        - **Root Cause Analysis** — Uncover the "why" behind sentiment patterns
        - **Smart Summaries** — Condense thousands of comments instantly
        - **Sentiment Dashboard** — Real-time emotion breakdown with charts
        - **Category Classifier** — Auto-sort feedback into 9 business categories
        - **Bulk Analysis** — Process thousands of comments at scale
        - **AI-Powered Insights** — Get actionable recommendations via GPT-4o-mini
        """, unsafe_allow_html=True)
    
    section_card("🧠 What is EmoSense?", "🎭", card1_content)
    
    spacer("md")
    
    # Card 2: Scientific Foundations - Big Five (Mini-IPIP)
    def card2_content():
        st.markdown("""
        EmoSense uses the **Mini-IPIP** (Mini International Personality Item Pool) to assess your 
        Big Five personality traits. This 20-item questionnaire is a scientifically validated 
        short-form measure of the Five-Factor Model of personality.
        
        ### 🧬 The Big Five Personality Traits
        
        | Trait | High Score | Low Score |
        |-------|-----------|-----------|
        | **Openness** | Creative, curious, imaginative | Practical, conventional, routine-oriented |
        | **Conscientiousness** | Organized, disciplined, goal-driven | Flexible, spontaneous, easy-going |
        | **Extraversion** | Outgoing, energetic, talkative | Reserved, reflective, independent |
        | **Agreeableness** | Cooperative, trusting, helpful | Competitive, skeptical, challenging |
        | **Neuroticism** | Emotionally sensitive, stress-prone | Calm, resilient, emotionally stable |
        
        ### 📊 How EmoSense Uses Your Big Five Profile
        
        Your personality scores directly influence how EmoSense communicates with you:
        
        - **High Openness** → More creative metaphors and exploratory conversations
        - **High Conscientiousness** → Structured responses with clear action steps
        - **High Extraversion** → Energetic, enthusiastic tone with more exclamations
        - **High Agreeableness** → Warmer, more validating language
        - **High Neuroticism** → Gentler approach, more reassurance and grounding
        
        ### 📚 Academic References
        
        > **Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006).** The Mini-IPIP scales: 
        > Tiny-yet-effective measures of the Big Five factors of personality. *Psychological Assessment, 
        > 18*(2), 192–203. https://doi.org/10.1037/1040-3590.18.2.192
        
        > **Goldberg, L. R. (1999).** A broad-bandwidth, public domain, personality inventory measuring 
        > the lower-level facets of several five-factor models. In I. Mervielde, I. Deary, F. De Fruyt, 
        > & F. Ostendorf (Eds.), *Personality Psychology in Europe* (Vol. 7, pp. 7–28). Tilburg University Press.
        
        > **Costa, P. T., & McCrae, R. R. (1992).** *Revised NEO Personality Inventory (NEO-PI-R) and 
        > NEO Five-Factor Inventory (NEO-FFI) professional manual.* Psychological Assessment Resources.
        """, unsafe_allow_html=True)
    
    section_card("🧠 Big Five Personality (Mini-IPIP)", "📊", card2_content)
    
    spacer("md")
    
    # Card 3: Scientific Foundations - Brief COPE
    def card3_content():
        st.markdown("""
        EmoSense uses the **Brief COPE** inventory to understand your natural coping strategies. 
        This 28-item questionnaire measures 14 different coping dimensions and is one of the most 
        widely used coping assessment tools in psychological research.
        
        ### 🎭 The 14 COPE Coping Strategies
        
        **Adaptive Strategies (Generally Helpful):**
        - 🎯 **Active Coping** — Taking action to improve the situation
        - 📋 **Planning** — Thinking about steps to handle the problem
        - 🌈 **Positive Reframing** — Finding the silver lining
        - ✅ **Acceptance** — Accepting the reality of the situation
        - 💬 **Emotional Support** — Getting comfort from others
        - 🤝 **Instrumental Support** — Seeking advice or help
        
        **Neutral/Situational Strategies:**
        - 🎮 **Self-Distraction** — Turning to other activities
        - 💭 **Venting** — Expressing negative feelings
        - 😄 **Humor** — Making jokes about the situation
        - 🙏 **Religion** — Finding comfort in spiritual beliefs
        
        **Strategies to Monitor:**
        - 🙈 **Denial** — Refusing to believe what's happening
        - 🍷 **Substance Use** — Using substances to feel better
        - 😔 **Behavioral Disengagement** — Giving up on goals
        - 😞 **Self-Blame** — Criticizing oneself
        
        ### 🤖 How EmoSense Uses Your COPE Profile
        
        Based on your dominant coping strategies, EmoSense assigns you one of 5 adaptive personas:
        
        | Persona | Primary Coping Style | AI Adaptation |
        |---------|---------------------|---------------|
        | 🛡️ **The Resilient Solver** | Active coping, planning | Action-oriented suggestions |
        | 🌱 **The Thoughtful Reframer** | Positive reframing, acceptance | Growth perspectives |
        | 🤝 **The Connected Supporter** | Emotional & instrumental support | Validation and connection |
        | 🌊 **The Mindful Observer** | Acceptance, self-distraction | Grounding and presence |
        | 🔥 **The Expressive Processor** | Venting, humor | Space for expression |
        
        ### 📚 Academic References
        
        > **Carver, C. S. (1997).** You want to measure coping but your protocol's too long: Consider 
        > the Brief COPE. *International Journal of Behavioral Medicine, 4*(1), 92–100. 
        > https://doi.org/10.1207/s15327558ijbm0401_6
        
        > **Carver, C. S., Scheier, M. F., & Weintraub, J. K. (1989).** Assessing coping strategies: 
        > A theoretically based approach. *Journal of Personality and Social Psychology, 56*(2), 267–283. 
        > https://doi.org/10.1037/0022-3514.56.2.267
        
        > **Lazarus, R. S., & Folkman, S. (1984).** *Stress, Appraisal, and Coping.* Springer Publishing Company.
        
        ---
        
        *Note: EmoSense's use of these assessments is for educational and personalization purposes only. 
        These questionnaires are not diagnostic tools and should not replace professional psychological assessment.*
        """, unsafe_allow_html=True)
    
    section_card("🎭 Brief COPE Assessment", "🧘", card3_content)
    
    spacer("md")
    
    # Card 4: Who is it for?
    def card4_content():
        st.markdown("""
        EmoSense AI serves diverse audiences seeking to understand emotional data:
        
        ### 🧘 Individuals
        - Complete personality + coping assessments for personalized AI support
        - Track personal emotional patterns over time
        - Gain self-awareness through guided conversations
        
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
        """, unsafe_allow_html=True)
    
    section_card("🎯 Who is it for?", "👥", card4_content)
    
    spacer("md")
    
    # Card 5: Built by Amarnoor Kaur
    def card5_content():
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
    
    section_card("🖤 Built with Purpose", "💝", card5_content)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
