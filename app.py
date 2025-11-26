"""
EmoSense AI - Premium Landing Page (Revamp)
Soft gradients, glass cards, and calm two-column layout
"""
import streamlit as st
from components.layout import (
    set_page_config,
    inject_global_styles,
    page_container,
    spacer,
    page_header,
    card,
    gradient_button,
    render_header,
)
from components.footer import render_footer

# Configure page with custom title
st.set_page_config(
    page_title="Home - EmoSense AI",
    page_icon="?",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_global_styles()
render_header()

with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    page_header(
        "EmoSense AI",
        "An emotion-aware copilot for humans and brands?calm, clear, and always on.",
        primary_cta=("Try Business Chatbot", "/business_chatbot"),
        secondary_cta=("Try Personal Chatbot", "/personal_chatbot")
    )

    spacer("sm")

    col1, col2 = st.columns([1.05, 0.95])
    with col1:
        card("""
        <div class="section-title">Calm intelligence for every conversation</div>
        <p class="section-subtitle">Ultra-clear insights from feedback, chats, and journals?delivered in a friendly tone.</p>
        <div class="stat-row">
            <div class="stat-chip">28 emotions detected</div>
            <div class="stat-chip">9 content categories</div>
            <div class="stat-chip">Research-backed RAG</div>
        </div>
        <div class="divider"></div>
        <div class="card-grid">
            <div class="pill pill-purple">Emotion radar</div>
            <div class="pill pill-blue">Crisis detection</div>
            <div class="pill pill-green">Strengths & wins</div>
            <div class="pill pill-pink">Summaries & actions</div>
        </div>
        """)

    with col2:
        card("""
        <div class="section-title" style="font-size:30px;">See signal in seconds</div>
        <p class="section-subtitle">Upload a thread or CSV and get a clean emotional report, ready for execs.</p>
        <div class="card-grid">
            <div class="premium-card" style="padding:16px;">
                <div class="section-subtitle" style="margin:0;">Upload CSV</div>
                <div class="hero-subtitle" style="margin:4px 0 10px;">Auto-detect comment columns & clean text</div>
            </div>
            <div class="premium-card" style="padding:16px;">
                <div class="section-subtitle" style="margin:0;">Run analysis</div>
                <div class="hero-subtitle" style="margin:4px 0 10px;">BERT + BART + GPT stack with RAG</div>
            </div>
            <div class="premium-card" style="padding:16px;">
                <div class="section-subtitle" style="margin:0;">Share</div>
                <div class="hero-subtitle" style="margin:4px 0 10px;">Concise stories for leadership & clients</div>
            </div>
        </div>
        """)

    spacer("lg")

    st.markdown('<div class="section-title">Designed for both sides of you</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Business Buddy for teams. Personal Companion for your own emotional clarity.</p>', unsafe_allow_html=True)

    feature_cols = st.columns(3)
    features = [
        ("Business Buddy", "Deep sentiment, crisis radar, viral signal detection, root-cause clustering."),
        ("Personal Companion", "Journaling insights, mood trends, and supportive reflections."),
        ("Smart Summaries", "Executive-ready briefs with emotion highlights and recommended actions."),
    ]
    for col, (title, body) in zip(feature_cols, features):
        with col:
            card(f"""
            <div class="section-subtitle" style="font-size:18px; color:#fff;">{title}</div>
            <p class="hero-subtitle" style="margin:6px 0 0;">{body}</p>
            """)

    spacer("lg")

    st.markdown('<div class="section-title">A calmer chat experience</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Rounded bubbles, soft gradients, and emotion badges keep chats human.</p>', unsafe_allow_html=True)

    chat_col1, chat_col2 = st.columns([1,1])
    with chat_col1:
        card("""
        <div class="chat-shell">
            <div class="chat-bubble chat-user">I need to know why customers churned last month.</div>
            <div class="chat-meta">You ? just now</div>
            <div class="chat-bubble chat-ai">Top emotions: frustration, confusion. Root causes: onboarding gaps and slow support handoffs. Recommend: guided checklists and proactive nudges.</div>
            <div class="chat-meta">EmoSense ? a moment ago</div>
        </div>
        """)
    with chat_col2:
        card("""
        <div class="chat-shell">
            <div class="chat-bubble chat-user">Feeling anxious after back-to-back meetings.</div>
            <div class="chat-meta">You ? just now</div>
            <div class="chat-bubble chat-ai">I hear you. Your stress keywords are spiking. Try a 5-minute reset and capture the triggers. Want a short breathing prompt?</div>
            <div class="chat-meta">Companion ? a moment ago</div>
        </div>
        """)

    spacer("lg")

    st.markdown('<div style="display:flex; gap:16px; flex-wrap:wrap; align-items:center;">' + gradient_button('Launch Business Buddy', '/business_chatbot') + '<a class="btn-ghost" href="/personal_chatbot">Open Personal Companion</a>' + '</div>', unsafe_allow_html=True)

    spacer("xl")
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
