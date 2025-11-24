"""
Terms and Conditions Page for EmoSense AI
Clean, scrollable design with all legal sections
"""
import streamlit as st
from components.footer import render_footer

def render_terms_and_conditions():
    """Render the Terms & Conditions page"""
    
    # Custom CSS
    st.markdown("""
    <style>
    .terms-hero {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .terms-hero h1 {
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
    }
    
    .terms-hero p {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .terms-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        max-width: 900px;
        margin: 0 auto;
    }
    
    .terms-section {
        margin-bottom: 35px;
        padding-bottom: 25px;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .terms-section:last-child {
        border-bottom: none;
    }
    
    .terms-section h2 {
        font-size: 24px;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 15px;
    }
    
    .terms-section p, .terms-section li {
        font-size: 15px;
        line-height: 1.8;
        color: #475569;
    }
    
    .terms-section ul {
        margin-left: 20px;
        margin-top: 10px;
    }
    
    .terms-section li {
        margin-bottom: 8px;
    }
    
    .last-updated {
        text-align: center;
        color: #94a3b8;
        font-size: 14px;
        font-style: italic;
        margin-bottom: 30px;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .terms-container {
            background: #1e293b;
        }
        
        .terms-section h2 {
            color: #a5b4fc;
        }
        
        .terms-section p, .terms-section li {
            color: #cbd5e1;
        }
        
        .last-updated {
            color: #94a3b8;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="terms-hero">
        <h1>📜 Terms & Conditions</h1>
        <p>Please read these terms carefully before using EmoSense AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Last updated
    st.markdown("""
    <p class="last-updated">Last Updated: January 2025</p>
    """, unsafe_allow_html=True)
    
    # Terms container
    st.markdown('<div class="terms-container">', unsafe_allow_html=True)
    
    # Section 1: Use of Platform
    st.markdown("""
    <div class="terms-section">
        <h2>1. Use of Platform</h2>
        <p>
            By accessing and using EmoSense AI, you agree to comply with these Terms and Conditions. 
            EmoSense AI is an emotion analytics platform designed for personal and business use. 
            You may use this platform to:
        </p>
        <ul>
            <li>Analyze emotional content from text inputs</li>
            <li>Generate AI-powered summaries and insights</li>
            <li>Access personal emotion companion features</li>
            <li>Upload and analyze bulk customer feedback (Business tier)</li>
        </ul>
        <p>
            You must not use this platform for any illegal, harmful, or malicious purposes.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 2: User Content
    st.markdown("""
    <div class="terms-section">
        <h2>2. User Content</h2>
        <p>
            All text, comments, and data you upload to EmoSense AI remain your property. 
            However, by using the platform, you grant us a limited license to process, analyze, 
            and store your content for the purpose of providing our services.
        </p>
        <ul>
            <li>We do not sell or share your data with third parties</li>
            <li>Your content is processed using AI models (BERT, BART, GPT-4o-mini)</li>
            <li>You are responsible for ensuring you have rights to upload any content</li>
            <li>We reserve the right to remove content that violates our policies</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3: Data Privacy
    st.markdown("""
    <div class="terms-section">
        <h2>3. Data Privacy</h2>
        <p>
            Your privacy is important to us. We collect and process data in accordance with 
            applicable privacy laws:
        </p>
        <ul>
            <li><strong>Data Collection:</strong> We collect text inputs, emotion analysis results, and usage analytics</li>
            <li><strong>Data Storage:</strong> Data is stored securely using industry-standard encryption</li>
            <li><strong>Data Retention:</strong> We retain data only as long as necessary to provide services</li>
            <li><strong>Third-Party Services:</strong> We use OpenAI API (GPT-4o-mini) for AI recommendations — their privacy policy applies</li>
            <li><strong>Your Rights:</strong> You may request data deletion at any time by contacting us</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 4: AI-Generated Output
    st.markdown("""
    <div class="terms-section">
        <h2>4. AI-Generated Output</h2>
        <p>
            EmoSense AI uses artificial intelligence models to generate insights, summaries, 
            and recommendations. Please note:
        </p>
        <ul>
            <li>AI outputs are generated automatically and may contain errors or inaccuracies</li>
            <li>Outputs should be used as guidance, not absolute truth</li>
            <li>We do not guarantee the accuracy, completeness, or reliability of AI outputs</li>
            <li>Users are responsible for verifying critical information before making decisions</li>
            <li>AI models may reflect biases present in training data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 5: Limitation of Liability
    st.markdown("""
    <div class="terms-section">
        <h2>5. Limitation of Liability</h2>
        <p>
            EmoSense AI is provided "as is" without warranties of any kind. To the fullest extent 
            permitted by law:
        </p>
        <ul>
            <li>We are not liable for any direct, indirect, or consequential damages arising from your use of the platform</li>
            <li>We do not guarantee uninterrupted or error-free service</li>
            <li>We are not responsible for decisions made based on AI-generated insights</li>
            <li>Maximum liability is limited to the amount paid for services (if applicable)</li>
        </ul>
        <p>
            This platform is not a substitute for professional medical, psychological, or legal advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 6: Prohibited Activities
    st.markdown("""
    <div class="terms-section">
        <h2>6. Prohibited Activities</h2>
        <p>You agree not to:</p>
        <ul>
            <li>Use the platform for illegal or harmful purposes</li>
            <li>Upload hateful, violent, or discriminatory content</li>
            <li>Attempt to reverse-engineer, hack, or exploit the platform</li>
            <li>Scrape or automate data collection without permission</li>
            <li>Impersonate others or provide false information</li>
            <li>Violate intellectual property rights</li>
            <li>Overload our systems with excessive requests</li>
        </ul>
        <p>Violation may result in account suspension or legal action.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 7: Modifications
    st.markdown("""
    <div class="terms-section">
        <h2>7. Modifications to Terms</h2>
        <p>
            We reserve the right to update or modify these Terms & Conditions at any time. 
            Changes will be effective immediately upon posting. Your continued use of the 
            platform after changes constitutes acceptance of the updated terms.
        </p>
        <p>
            We recommend reviewing this page periodically to stay informed about any updates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 8: Contact
    st.markdown("""
    <div class="terms-section">
        <h2>8. Contact Information</h2>
        <p>
            If you have any questions, concerns, or requests regarding these Terms & Conditions, 
            please contact us:
        </p>
        <ul>
            <li><strong>Email:</strong> <a href="mailto:amar.noor.work@gmail.com" style="color: #667eea; text-decoration: none;">amar.noor.work@gmail.com</a></li>
            <li><strong>Creator:</strong> Amarnoor Kaur</li>
            <li><strong>Location:</strong> Canada</li>
        </ul>
        <p>We aim to respond to all inquiries within 48 hours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    # Render footer
    render_footer()


# Main execution
if __name__ == "__main__":
    st.set_page_config(
        page_title="Terms & Conditions - EmoSense AI",
        page_icon="📜",
        layout="wide"
    )
    render_terms_and_conditions()
