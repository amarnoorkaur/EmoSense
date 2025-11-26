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

    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        card("""
        <div class="section-subtitle" style="font-size:20px; color:#fff; margin-bottom:12px;">💼 Business Buddy</div>
        <p class="hero-subtitle" style="margin:6px 0 12px;">Deep sentiment analysis for customer feedback, reviews, and social media.</p>
        <div class="card-grid">
            <div class="pill pill-purple">🎯 Viral Signal Detection</div>
            <div class="pill pill-blue">🧠 Root Cause Analysis</div>
            <div class="pill pill-green">📊 Crisis Radar</div>
            <div class="pill pill-pink">✨ Smart Summaries</div>
            <div class="pill pill-purple">📈 Sentiment Dashboard</div>
            <div class="pill pill-blue">🔍 Category Classifier</div>
        </div>
        """)
    
    with feature_cols[1]:
        card("""
        <div class="section-subtitle" style="font-size:20px; color:#fff; margin-bottom:12px;">💜 Personal Companion</div>
        <p class="hero-subtitle" style="margin:6px 0 12px;">Context-aware emotional support with conversation memory and personality modes.</p>
        <div class="card-grid">
            <div class="pill pill-green">🤝 5 Personalities</div>
            <div class="pill pill-pink">💬 5 Conversation Modes</div>
            <div class="pill pill-purple">🧠 Memory & Trends</div>
            <div class="pill pill-blue">🆘 Crisis Detection</div>
            <div class="pill pill-green">😊 28 Emotions</div>
            <div class="pill pill-pink">🎭 Natural AI Chat</div>
        </div>
        """)

    spacer("md")

    # Personal Chatbot Features Details
    st.markdown('<div class="section-title">Personal Companion: Choose Your Style</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">5 personalities × 5 modes = 25 ways to connect authentically</p>', unsafe_allow_html=True)

    personality_cols = st.columns(5)
    personalities = [
        ("🤝 Friendly", "Warm & approachable"),
        ("🧘 Calm", "Tranquil & grounding"),
        ("👩‍👧 Big Sister", "Caring & protective"),
        ("😄 Funny", "Lighthearted humor"),
        ("🤔 Deep Thinker", "Philosophical")
    ]
    for col, (title, desc) in zip(personality_cols, personalities):
        with col:
            card(f"""
            <div class="hero-subtitle" style="font-size:16px; color:#C4B5FD; margin-bottom:6px;">{title}</div>
            <p style="margin:0; color:#9CA3AF; font-size:13px;">{desc}</p>
            """)

    spacer("sm")

    mode_cols = st.columns(5)
    modes = [
        ("💬 Casual Chat", "Natural flow"),
        ("🤗 Comfort Me", "Gentle support"),
        ("🤔 Reflect", "Deep questions"),
        ("🔥 Hype Me Up", "Energizing"),
        ("👂 Just Listen", "Minimal replies")
    ]
    for col, (title, desc) in zip(mode_cols, modes):
        with col:
            card(f"""
            <div class="hero-subtitle" style="font-size:16px; color:#A5B4FC; margin-bottom:6px;">{title}</div>
            <p style="margin:0; color:#9CA3AF; font-size:13px;">{desc}</p>
            """)

    spacer("lg")

    # Business Chatbot Features Details
    st.markdown('<div class="section-title">Business Buddy: Predict What Goes Viral</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">6 signals analyzed in real-time to identify content with viral potential</p>', unsafe_allow_html=True)

    viral_cols = st.columns(3)
    viral_signals = [
        ("🔥 Emotional Intensity", "Strong joy, surprise, or anger amplifies shares"),
        ("📢 Repetition Detection", "Similar phrases = organic movement"),
        ("⚡ Urgency Signals", "Time-sensitive language drives action"),
        ("🎯 Question Patterns", "Curiosity triggers engagement"),
        ("💬 Conversation Starters", "Debate & discussion potential"),
        ("🌊 Emotional Diversity", "Multi-emotion content spreads wider")
    ]
    for col, (title, desc) in zip(viral_cols, viral_signals[:3]):
        with col:
            card(f"""
            <div class="section-subtitle" style="font-size:16px; color:#fff; margin-bottom:8px;">{title}</div>
            <p class="hero-subtitle" style="margin:0;">{desc}</p>
            """)

    spacer("sm")

    viral_cols2 = st.columns(3)
    for col, (title, desc) in zip(viral_cols2, viral_signals[3:]):
        with col:
            card(f"""
            <div class="section-subtitle" style="font-size:16px; color:#fff; margin-bottom:8px;">{title}</div>
            <p class="hero-subtitle" style="margin:0;">{desc}</p>
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
