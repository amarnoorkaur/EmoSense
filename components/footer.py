"""
Global Footer Component for EmoSense AI
Includes newsletter signup, copyright, and dark mode support
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
    """Render the global footer component"""
    
    # Custom CSS for footer
    st.markdown("""
    <style>
    .footer-container {
        border-top: 1px solid rgba(102, 126, 234, 0.15);
        padding: 40px 20px 20px 20px;
        margin-top: 60px;
        text-align: center;
        background: linear-gradient(180deg, transparent 0%, rgba(102, 126, 234, 0.03) 100%);
    }
    
    .footer-newsletter {
        max-width: 500px;
        margin: 0 auto 30px auto;
        padding: 25px;
        background: linear-gradient(135deg, #f8f9ff 0%, #eef2ff 100%);
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.08);
    }
    
    .footer-newsletter h3 {
        color: #667eea;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .footer-newsletter p {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    .footer-copyright {
        color: #94a3b8;
        font-size: 14px;
        padding-top: 20px;
    }
    
    .footer-copyright a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer-copyright a:hover {
        color: #764ba2;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .footer-container {
            border-top-color: rgba(255, 255, 255, 0.1);
            background: linear-gradient(180deg, transparent 0%, rgba(102, 126, 234, 0.05) 100%);
        }
        
        .footer-newsletter {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        }
        
        .footer-newsletter h3 {
            color: #a5b4fc;
        }
        
        .footer-newsletter p {
            color: #cbd5e1;
        }
        
        .footer-copyright {
            color: #cbd5e1;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Footer container
    st.markdown('<div class="footer-container">', unsafe_allow_html=True)
    
    # Newsletter section
    st.markdown("""
    <div class="footer-newsletter">
        <h3>📬 Stay Updated</h3>
        <p>Get the latest EmoSense AI updates and features delivered to your inbox</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Newsletter signup form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("newsletter_form", clear_on_submit=True):
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                label_visibility="collapsed"
            )
            subscribe_button = st.form_submit_button("✨ Subscribe", use_container_width=True)
            
            if subscribe_button:
                if email and "@" in email and "." in email:
                    if save_subscriber(email):
                        st.success("🎉 Thank you for subscribing! You'll hear from us soon.")
                    else:
                        st.info("📧 You're already subscribed!")
                else:
                    st.error("❌ Please enter a valid email address")
    
    # Copyright
    st.markdown("""
    <div class="footer-copyright">
        <p>EmoSense AI © 2025 — Built with ♥ by <a href="mailto:amar.noor.work@gmail.com">Amarnoor</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# Test footer when run directly
if __name__ == "__main__":
    st.set_page_config(page_title="Footer Test", layout="wide")
    st.title("Footer Component Test")
    st.write("This is some page content...")
    st.write("Scroll down to see the footer")
    render_footer()
