"""
Terms & Conditions - EmoSense AI
Clean, organized with expanders for better readability
"""
import streamlit as st
from components.layout import set_page_config, page_container, hero_section, spacer
from components.footer import render_footer

# Configure page
set_page_config()

# Main container
with page_container():
    # Hero Section
    hero_section(
        title="📜 Terms & Conditions",
        subtitle="Please read this carefully before using EmoSense AI.",
        detail="Last Updated: January 2025"
    )
    
    spacer("md")
    
    # Section 1: Use of the Platform
    with st.expander("**1. Use of the Platform**", expanded=False):
        st.markdown("""
        By accessing and using EmoSense AI, you agree to comply with these Terms and Conditions. 
        EmoSense AI is an emotion analytics platform designed for personal and business use.
        
        **You may use this platform to:**
        - Analyze emotional content from text inputs
        - Generate AI-powered summaries and insights
        - Access personal emotion companion features
        - Upload and analyze bulk customer feedback (Business tier)
        
        **You must not** use this platform for any illegal, harmful, or malicious purposes.
        """)
    
    # Section 2: User Content
    with st.expander("**2. User Content**", expanded=False):
        st.markdown("""
        All text, comments, and data you upload to EmoSense AI remain your property. 
        However, by using the platform, you grant us a limited license to process, analyze, 
        and store your content for the purpose of providing our services.
        
        - We do not sell or share your data with third parties
        - Your content is processed using AI models (BERT, BART, GPT-4o-mini)
        - You are responsible for ensuring you have rights to upload any content
        - We reserve the right to remove content that violates our policies
        """)
    
    # Section 3: Data & Privacy
    with st.expander("**3. Data & Privacy**", expanded=False):
        st.markdown("""
        Your privacy is important to us. We collect and process data in accordance with 
        applicable privacy laws.
        
        **Data Collection:**  
        We collect text inputs, emotion analysis results, and usage analytics.
        
        **Data Storage:**  
        Data is stored securely using industry-standard encryption.
        
        **Data Retention:**  
        We retain data only as long as necessary to provide services.
        
        **Third-Party Services:**  
        We use OpenAI API (GPT-4o-mini) for AI recommendations — their privacy policy applies.
        
        **Your Rights:**  
        You may request data deletion at any time by contacting us at amar.noor.work@gmail.com.
        """)
    
    # Section 4: AI-Generated Output
    with st.expander("**4. AI-Generated Output**", expanded=False):
        st.markdown("""
        EmoSense AI uses artificial intelligence models to generate insights, summaries, 
        and recommendations. Please note:
        
        - AI outputs are generated automatically and may contain errors or inaccuracies
        - Outputs should be used as guidance, not absolute truth
        - We do not guarantee the accuracy, completeness, or reliability of AI outputs
        - Users are responsible for verifying critical information before making decisions
        - AI models may reflect biases present in training data
        
        **Important:** EmoSense is NOT a replacement for professional medical, psychological, 
        or legal advice.
        """)
    
    # Section 5: Limitation of Liability
    with st.expander("**5. Limitation of Liability**", expanded=False):
        st.markdown("""
        EmoSense AI is provided "as is" without warranties of any kind. To the fullest extent 
        permitted by law:
        
        - We are not liable for any direct, indirect, or consequential damages arising from your use
        - We do not guarantee uninterrupted or error-free service
        - We are not responsible for decisions made based on AI-generated insights
        - Maximum liability is limited to the amount paid for services (if applicable)
        
        **This platform is not a substitute for professional mental health support, medical advice, 
        or therapy.** If you're experiencing a crisis, please contact a mental health professional 
        or crisis hotline immediately.
        """)
    
    # Section 6: Prohibited Activities
    with st.expander("**6. Prohibited Activities**", expanded=False):
        st.markdown("""
        You agree not to:
        
        - Use the platform for illegal or harmful purposes
        - Upload hateful, violent, or discriminatory content
        - Attempt to reverse-engineer, hack, or exploit the platform
        - Scrape or automate data collection without permission
        - Impersonate others or provide false information
        - Violate intellectual property rights
        - Overload our systems with excessive requests
        - Use the platform to harm, harass, or threaten others
        
        **Violation may result in account suspension or legal action.**
        """)
    
    # Section 7: Modifications
    with st.expander("**7. Modifications to Terms**", expanded=False):
        st.markdown("""
        We reserve the right to update or modify these Terms & Conditions at any time. 
        Changes will be effective immediately upon posting.
        
        Your continued use of the platform after changes constitutes acceptance of the updated terms.
        
        We recommend reviewing this page periodically to stay informed about any updates.
        """)
    
    # Section 8: Contact
    with st.expander("**8. Contact Information**", expanded=False):
        st.markdown("""
        If you have any questions, concerns, or requests regarding these Terms & Conditions, 
        please contact us:
        
        **Email:** amar.noor.work@gmail.com  
        **Creator:** Amarnoor Kaur  
        **Location:** Canada
        
        We aim to respond to all inquiries within 48 hours.
        """)
    
    spacer("lg")
    
    # Additional note
    st.info("""
    💡 **Note:** These terms are designed to protect both users and the platform. 
    By using EmoSense AI, you acknowledge that you have read, understood, and agree 
    to be bound by these Terms & Conditions.
    """)
    
    spacer("md")

# Footer
render_footer()
