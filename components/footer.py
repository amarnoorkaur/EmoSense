"""
Global Footer Component - EmoSense AI
Glassmorphic design with newsletter signup
"""
import streamlit as st
import json
import os
from datetime import datetime

# Path to store newsletter subscribers
SUBSCRIBERS_FILE = "data/newsletter_subscribers.json"


def save_subscriber(email: str):
    """Save newsletter subscriber email"""
    try:
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(SUBSCRIBERS_FILE):
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
        else:
            subscribers = []
        
        if email in [sub.get('email') for sub in subscribers]:
            return False
        
        subscribers.append({
            "email": email,
            "subscribed_at": datetime.now().isoformat()
        })
        
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving subscriber: {str(e)}")
        return False


def render_footer():
    """Render the glassmorphic global footer with improved design"""
    
    # Inject enhanced footer CSS targeting Streamlit columns
    footer_css = """
    <style>
    /* Footer Wrapper */
    .footer-wrapper {
        width: 100%;
        padding: 3rem 0 2rem 0;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
    }

    /* Footer column container */
    .footer-wrapper div[data-testid="column"] {
        padding: 1rem;
    }

    /* Left Column Content */
    .footer-left h2 {
        font-size: 1.6rem;
        margin: 0 0 0.8rem 0;
        font-weight: 700;
        background: linear-gradient(135deg, #8A5CF6, #C06CFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .footer-left p {
        margin: 0.5rem 0;
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .footer-left a {
        color: #A78BFA;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .footer-left a:hover {
        color: #C4B5FD;
        text-decoration: underline;
    }

    /* Right Column Content */
    .footer-right h3 {
        margin: 0 0 0.7rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        color: #FFFFFF;
    }

    .footer-links {
        margin-bottom: 1.5rem;
    }

    .footer-links a {
        display: block;
        margin-bottom: 0.5rem;
        color: rgba(255,255,255,0.8);
        text-decoration: none;
        font-size: 0.95rem;
        transition: color 0.2s ease;
    }

    .footer-links a:hover {
        color: #C4B5FD;
    }

    /* Newsletter Section */
    .footer-right .newsletter-section h4 {
        margin: 1.5rem 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
        color: #FFFFFF;
    }

    /* Streamlit widgets styling in footer */
    .footer-wrapper .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
    }

    .footer-wrapper .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.5) !important;
    }

    .footer-wrapper .stTextInput > div > div > input:focus {
        border-color: rgba(138, 92, 246, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(138, 92, 246, 0.3) !important;
    }

    .footer-wrapper .stButton > button {
        width: 100% !important;
        padding: 0.75rem !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #8A5CF6, #C06CFF) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 12px rgba(138,92,246,0.35) !important;
        margin-top: 0.5rem !important;
    }

    .footer-wrapper .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 18px rgba(138,92,246,0.55) !important;
    }

    /* Hide labels */
    .footer-wrapper .stTextInput label {
        display: none !important;
    }
    </style>
    """
    
    st.markdown(footer_css, unsafe_allow_html=True)
    
    # Container wrapper
    st.markdown('<div class="footer-wrapper">', unsafe_allow_html=True)
    
    # Create two-column layout using Streamlit native columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="footer-left">
            <h2>EmoSense AI</h2>
            <p>Emotion-aware insights for humans & brands.</p>
            <p>Built with ❤️ by <a href="https://www.linkedin.com/in/amarnoor-kaur-455379249/" target="_blank">Amarnoor Kaur</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="footer-right">
            <h3>Contact</h3>
            <div class="footer-links">
                <a href="mailto:amar.noor.work@gmail.com">📧 Email</a>
                <a href="https://www.linkedin.com/in/amarnoor-kaur-455379249/" target="_blank">🔗 LinkedIn</a>
            </div>
            <div class="newsletter-section">
                <h4>Newsletter</h4>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Newsletter signup widgets
        email = st.text_input(
            "Email",
            key='footer_newsletter',
            placeholder="your@email.com",
            label_visibility="collapsed"
        )
        
        if st.button("✨ Notify Me", key='footer_notify', use_container_width=True):
            if email and "@" in email and "." in email:
                if save_subscriber(email):
                    st.success("Thanks! We'll keep you posted. 🎉")
                else:
                    st.info("You're already subscribed! ✅")
            else:
                st.warning("Please enter a valid email address.")
    
    st.markdown('</div>', unsafe_allow_html=True)
