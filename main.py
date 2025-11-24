"""
EmoSense AI - Main Application with Routing
Version 4.0 - Multi-page architecture with Terms & Conditions
"""
import streamlit as st

# Import page renderers
from landing_page import render_landing_page
from pages.personal_chatbot import render_personal_chatbot
from pages.business_chatbot import render_business_chatbot
from pages.About_EmoSense import render_about_emosense
from pages.Terms_and_Conditions import render_terms_and_conditions

# Page configuration
st.set_page_config(
    page_title="EmoSense AI - Emotional Intelligence Platform",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for page routing
if "page" not in st.session_state:
    st.session_state.page = "home"

# Custom CSS for navigation
st.markdown("""
<style>
.nav-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px 30px;
    border-radius: 10px;
    margin-bottom: 30px;
}

.nav-button {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    padding: 10px 20px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: 0 5px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.nav-button:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.nav-button-active {
    background: white;
    color: #667eea;
}
</style>
""", unsafe_allow_html=True)

# Navigation Bar
col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 1.5, 1])

with col1:
    st.markdown("### 🎭")

with col2:
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
        st.session_state.page = "home"
        st.rerun()

with col3:
    if st.button("💛 Personal Chatbot", use_container_width=True, type="primary" if st.session_state.page == "personal_chatbot" else "secondary"):
        st.session_state.page = "personal_chatbot"
        st.rerun()

with col4:
    if st.button("📊 Business Insights", use_container_width=True, type="primary" if st.session_state.page == "business_chatbot" else "secondary"):
        st.session_state.page = "business_chatbot"
        st.rerun()

with col5:
    if st.button("ℹ️ About", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
        st.session_state.page = "about"
        st.rerun()

with col6:
    if st.button("📜 Terms", use_container_width=True, type="primary" if st.session_state.page == "terms" else "secondary"):
        st.session_state.page = "terms"
        st.rerun()

st.markdown("---")

# Route to appropriate page
if st.session_state.page == "home":
    render_landing_page()
elif st.session_state.page == "personal_chatbot":
    render_personal_chatbot()
elif st.session_state.page == "business_chatbot":
    render_business_chatbot()
elif st.session_state.page == "about":
    render_about_emosense()
elif st.session_state.page == "terms":
    render_terms_and_conditions()
else:
    # Default to home
    render_landing_page()
