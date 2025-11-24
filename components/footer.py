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
    """Render the glassmorphic global footer"""
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card" style="margin-top: 3rem; padding: 2rem;">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="margin-top: -3rem;">
            <h3 style="color: #FFFFFF; margin-bottom: 0.5rem;">EmoSense AI</h3>
            <p style="color: #A8A9B3; margin-bottom: 0.5rem;">
                Emotion-aware insights for humans & brands.
            </p>
            <p style="color: #A8A9B3; font-size: 0.875rem;">
                Built with ❤️ by <strong style="color: #8A5CF6;">Amarnoor Kaur</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="margin-top: -3rem;">
            <p style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.75rem;">Contact</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="color: #A8A9B3; font-size: 0.875rem; margin-bottom: 0.5rem;">
            📧 <a href="mailto:amar.noor.work@gmail.com" style="color: #8A5CF6; text-decoration: none;">Email</a>
        </p>
        <p style="color: #A8A9B3; font-size: 0.875rem; margin-bottom: 1rem;">
            🔗 <a href="https://www.linkedin.com" style="color: #8A5CF6; text-decoration: none;">LinkedIn</a>
        </p>
        """, unsafe_allow_html=True)
        
        # Newsletter signup
        email = st.text_input(
            "Get updates (newsletter):",
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
