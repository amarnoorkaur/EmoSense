"""
Terms & Conditions - EmoSense AI
Glassmorphic design with organized expanders
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
    
    # Hero
    gradient_hero(
        "📜 Terms & Conditions",
        "Please read these terms carefully before using EmoSense AI."
    )
    
    spacer("md")
    
    st.markdown("""
    <div class="glass-card">
        <p style="color: #A8A9B3; line-height: 1.8;">
            <strong style="color: #FFFFFF;">Last Updated:</strong> December 2024<br/>
            By accessing or using EmoSense AI, you agree to be bound by these Terms and Conditions. 
            If you do not agree with any part of these terms, please do not use our service.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("md")
    
    # Expander 1: Use of Platform
    with st.expander("⚖️ Use of Platform", expanded=False):
        st.markdown("""
        ### Permitted Use
        
        EmoSense AI is provided for personal, educational, and commercial emotion analysis purposes. You may:
        
        - Analyze text for emotion detection and sentiment insights
        - Use bulk analysis features for business intelligence
        - Download reports and analytics for internal use
        - Integrate insights into your decision-making processes
        
        ### Prohibited Activities
        
        You must NOT:
        
        - Use the platform to analyze private communications without consent
        - Attempt to reverse-engineer or copy our AI models
        - Overload the system with automated requests (rate limiting applies)
        - Use outputs to harm, discriminate, or manipulate individuals
        - Violate any applicable laws or regulations
        
        ### Account Responsibility
        
        If you create an account:
        - You are responsible for maintaining the confidentiality of your credentials
        - You agree to notify us immediately of any unauthorized access
        - You are liable for all activities under your account
        """, unsafe_allow_html=True)
    
    # Expander 2: Privacy & Data Handling
    with st.expander("🛡️ Privacy & Data Handling", expanded=False):
        st.markdown("""
        ### Data Processing
        
        **What We Process:**
        - Text input you provide for emotion analysis
        - Uploaded CSV files for bulk analysis
        - API usage statistics (anonymous)
        
        **What We DON'T Store:**
        - Your actual text input (processed in real-time only)
        - Personal identifiable information unless explicitly provided (e.g., newsletter signup)
        - Emotion analysis results after session ends
        
        ### Third-Party Services
        
        EmoSense uses the following third-party services:
        
        - **Hugging Face API** - For BERT emotion detection and BART summarization
        - **OpenAI API** - For GPT-4 recommendations (optional, opt-in only)
        - **ChromaDB** - For RAG knowledge retrieval (on our secure servers)
        
        Your data is transmitted securely via HTTPS. Third-party APIs have their own privacy policies, 
        which we encourage you to review.
        
        ### Cookies & Analytics
        
        We may use cookies to:
        - Remember your preferences (e.g., threshold settings)
        - Improve user experience
        - Gather anonymous usage statistics
        
        You can disable cookies in your browser settings, though some features may not function properly.
        
        ### GDPR & CCPA Compliance
        
        If you are located in the EU or California:
        - You have the right to access, delete, or export your data
        - You can opt-out of newsletter communications at any time
        - Contact us at privacy@emosense.ai for data requests
        """, unsafe_allow_html=True)
    
    # Expander 3: AI Output Limitations
    with st.expander("🤖 AI Output Limitations", expanded=False):
        st.markdown("""
        ### Nature of AI Predictions
        
        EmoSense AI uses machine learning models that provide **probabilistic predictions**, not absolute truths. 
        
        **Important Disclaimers:**
        
        - **Not Medical Advice**: EmoSense is NOT a mental health diagnostic tool. It does not replace 
          professional psychological evaluation or therapy.
        - **Accuracy Limitations**: While our models are state-of-the-art, they may misinterpret sarcasm, 
          cultural nuances, or context-specific language.
        - **Bias Awareness**: AI models can reflect biases present in training data. We strive for fairness 
          but cannot guarantee perfect neutrality.
        - **No Guarantees**: We do not guarantee specific accuracy rates or outcomes from using our platform.
        
        ### Responsible Use
        
        - Use EmoSense as ONE input among many in decision-making
        - Do not make critical decisions (hiring, medical, legal) based solely on emotion analysis
        - Verify AI suggestions with human judgment and domain expertise
        - For mental health concerns, consult licensed professionals
        
        ### Model Updates
        
        We may update our AI models to improve performance. This may result in:
        - Different emotion labels or probabilities for the same text
        - Changes in summarization or recommendation outputs
        - New features or categories
        
        We will notify users of major model changes via the platform.
        """, unsafe_allow_html=True)
    
    # Expander 4: Prohibited Activities
    with st.expander("⛔ Prohibited Activities", expanded=False):
        st.markdown("""
        ### Strictly Forbidden
        
        You may NOT use EmoSense AI to:
        
        1. **Harm or Manipulate**
           - Psychologically manipulate individuals based on detected emotions
           - Target vulnerable populations with predatory content
           - Use emotion data for discriminatory purposes
        
        2. **Violate Privacy**
           - Analyze private messages without explicit consent
           - Scrape or harvest user data from platforms without authorization
           - Share emotion analysis results that violate privacy laws
        
        3. **Abuse the System**
           - Launch denial-of-service attacks or excessive automated requests
           - Attempt to extract, copy, or replicate our AI models
           - Circumvent rate limits or security measures
        
        4. **Illegal Activities**
           - Use the platform for fraud, harassment, or illegal surveillance
           - Violate intellectual property rights
           - Engage in any activity prohibited by local, state, or federal law
        
        ### Consequences
        
        Violation of these terms may result in:
        - Immediate suspension or termination of your account
        - Legal action if applicable
        - Reporting to relevant authorities for criminal activities
        """, unsafe_allow_html=True)
    
    # Expander 5: Liability
    with st.expander("📉 Limitation of Liability", expanded=False):
        st.markdown("""
        ### Service Provided "As Is"
        
        EmoSense AI is provided on an **"AS IS" and "AS AVAILABLE"** basis, without warranties of any kind, 
        either express or implied.
        
        ### No Warranty
        
        We do not warrant that:
        - The service will be uninterrupted, secure, or error-free
        - Results will be accurate, reliable, or complete
        - Defects will be corrected promptly
        - The platform is free from viruses or harmful components
        
        ### Limitation of Damages
        
        To the maximum extent permitted by law:
        
        - We are NOT liable for any indirect, incidental, or consequential damages arising from your use 
          of EmoSense AI
        - We are NOT liable for loss of data, revenue, profits, or business opportunities
        - Our total liability shall not exceed the amount you paid for the service (if any) in the 
          past 12 months
        
        ### Indemnification
        
        You agree to indemnify and hold harmless EmoSense AI, its creators, and affiliates from any claims, 
        damages, or expenses arising from:
        - Your violation of these Terms
        - Your misuse of the platform
        - Your violation of any third-party rights
        
        ### Force Majeure
        
        We are not liable for delays or failures caused by circumstances beyond our control, including:
        - Natural disasters, pandemics, or acts of God
        - Government actions or regulations
        - Third-party service outages (Hugging Face, OpenAI, etc.)
        - Internet infrastructure failures
        """, unsafe_allow_html=True)
    
    # Expander 6: Modifications
    with st.expander("📝 Modifications to Terms", expanded=False):
        st.markdown("""
        ### Right to Modify
        
        We reserve the right to modify these Terms and Conditions at any time. Changes may include:
        - Updates to reflect new features or services
        - Clarifications based on user feedback
        - Legal or regulatory compliance updates
        
        ### Notification
        
        When we make material changes:
        - We will update the "Last Updated" date at the top of this page
        - We may notify you via email (if subscribed to our newsletter)
        - We may display a prominent notice on the platform
        
        ### Acceptance of Changes
        
        By continuing to use EmoSense AI after changes are posted, you agree to the updated Terms. 
        If you do not agree with the changes, you must stop using the platform.
        
        ### Version History
        
        Previous versions of Terms and Conditions are available upon request at legal@emosense.ai.
        """, unsafe_allow_html=True)
    
    # Expander 7: Contact
    with st.expander("✉️ Contact & Dispute Resolution", expanded=False):
        st.markdown("""
        ### Contact Information
        
        For questions, concerns, or requests regarding these Terms:
        
        - **Email:** legal@emosense.ai
        - **Support:** support@emosense.ai
        - **Data Requests:** privacy@emosense.ai
        
        We aim to respond to all inquiries within 5 business days.
        
        ### Dispute Resolution
        
        If you have a dispute with EmoSense AI:
        
        1. **Informal Resolution**: Contact us first to resolve the issue amicably
        2. **Mediation**: If informal resolution fails, we encourage mediation through a mutually 
           agreed-upon neutral third party
        3. **Arbitration**: Any unresolved disputes will be settled through binding arbitration in 
           accordance with the rules of the American Arbitration Association
        
        ### Governing Law
        
        These Terms are governed by the laws of [Your Jurisdiction], without regard to conflict of law principles.
        
        ### Severability
        
        If any provision of these Terms is found to be invalid or unenforceable, the remaining provisions 
        will continue in full force and effect.
        
        ### Entire Agreement
        
        These Terms constitute the entire agreement between you and EmoSense AI regarding the use of our 
        platform, superseding any prior agreements or communications.
        """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Acknowledgment
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 2rem;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">Thank You for Using EmoSense AI</h3>
        <p style="color: #A8A9B3; line-height: 1.8;">
            We are committed to providing a safe, ethical, and valuable emotion analysis platform. 
            Your trust and responsible use are essential to our mission.
        </p>
        <p style="color: #8A5CF6; margin-top: 1rem;">
            💜 If you have feedback or questions, we'd love to hear from you!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
