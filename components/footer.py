"""
Global Footer Component for EmoSense AI
Includes contact info, links, and newsletter signup
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
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Load existing subscribers
        if os.path.exists(SUBSCRIBERS_FILE):
            with open(SUBSCRIBERS_FILE, 'r') as f:
                subscribers = json.load(f)
        else:
            subscribers = []
        
        # Check if email already exists
        if email in [sub.get('email') for sub in subscribers]:
            return False
        
        # Add new subscriber
        subscribers.append({
            "email": email,
            "subscribed_at": datetime.now().isoformat()
        })
        
        # Save back to file
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving subscriber: {str(e)}")
        return False


def render_footer():
    """Render the redesigned global footer component"""
    
    # Divider
    st.markdown("---", unsafe_allow_html=True)
    
    # Footer layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**EmoSense AI** · Emotion-aware insights for humans & brands.")
        st.markdown("Built with ❤️ by **Amarnoor Kaur**.")
    
    with col2:
        st.markdown("**Contact**")
        st.markdown("[Email](mailto:amar.noor.work@gmail.com)")
        # Placeholder link for LinkedIn
        st.markdown("[LinkedIn](https://www.linkedin.com)")
        
        # Newsletter signup
        email = st.text_input(
            "Get updates (newsletter):", 
            key='footer_newsletter', 
            label_visibility="collapsed", 
            placeholder="Enter your email"
        )
        if st.button("Notify me", key='footer_notify'):
            # Acknowledge subscription
            if email and "@" in email and "." in email:
                if save_subscriber(email):
                    st.success("Thanks! We'll keep you posted.")
                else:
                    st.info("You're already subscribed!")
            else:
                st.warning("Please enter an email address.")


# Test footer when run directly
if __name__ == "__main__":
    st.set_page_config(page_title="Footer Test", layout="wide")
    st.title("Footer Component Test")
    st.write("This is some page content...")
    st.write("Scroll down to see the footer")
    render_footer()
