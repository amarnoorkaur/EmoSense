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
        "An emotion-aware copilot for humans and brands — calm, clear, and always learning you.",
        primary_cta=("Try Business Buddy", "/Business_Chatbot"),
        secondary_cta=("Try Personal Companion", "/Personal_Chatbot")
    )

    spacer("sm")

    col1, col2 = st.columns([1.05, 0.95])
    with col1:
        card("""
        <div class="section-title">Calm intelligence for every conversation</div>
        <p class="section-subtitle">Ultra-clear insights from feedback, chats, and journals — delivered in a friendly tone.</p>
        <div class="stat-row">
            <div class="stat-chip">28 emotions detected</div>
            <div class="stat-chip">9 content categories</div>
            <div class="stat-chip">4-layer adaptive AI</div>
        </div>
        <div class="divider"></div>
        <div class="card-grid">
            <div class="pill pill-purple">Big Five + COPE</div>
            <div class="pill pill-blue">Crisis detection</div>
            <div class="pill pill-green">Style matching</div>
            <div class="pill pill-pink">Voice chat</div>
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
                <div class="hero-subtitle" style="margin:4px 0 10px;">BERT + BART + GPT-4o-mini with RAG</div>
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
        <p class="hero-subtitle" style="margin:6px 0 12px;">4-layer adaptive AI that learns your personality, coping style, and speaking patterns.</p>
        <div class="card-grid">
            <div class="pill pill-purple">🧠 Big Five Personality</div>
            <div class="pill pill-blue">🎭 COPE Coping Styles</div>
            <div class="pill pill-green">🪞 Linguistic Style Matching</div>
            <div class="pill pill-pink">🎙️ Voice Chat</div>
            <div class="pill pill-purple">😊 28 Emotions</div>
            <div class="pill pill-blue">🆘 Crisis Detection</div>
        </div>
        """)

    spacer("md")

    # Personal Chatbot Features Details - NEW 4-LAYER SYSTEM
    st.markdown('<div class="section-title">Personal Companion: 4-Layer Adaptive Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">The more you share, the more it understands — fully personalized to YOU</p>', unsafe_allow_html=True)

    layer_cols = st.columns(4)
    layers = [
        ("🧠 Big Five", "Personality Assessment", "Mini-IPIP-20 maps your Openness, Conscientiousness, Extraversion, Agreeableness & Neuroticism"),
        ("🎭 COPE", "Coping Style Analysis", "Brief COPE identifies your natural coping strategies across 14 dimensions"),
        ("🪞 LSM", "Linguistic Style Matching", "Mirrors your sentence length, formality, emoji use & punctuation patterns"),
        ("❤️ Emotion", "Real-Time Detection", "BERT classifies 28 emotions to adapt tone & suggestions in context")
    ]
    for col, (icon, title, desc) in zip(layer_cols, layers):
        with col:
            card(f"""
            <div style="text-align:center;">
                <div style="font-size:32px; margin-bottom:8px;">{icon}</div>
                <div class="hero-subtitle" style="font-size:15px; color:#C4B5FD; margin-bottom:6px; font-weight:600;">{title}</div>
                <p style="margin:0; color:#9CA3AF; font-size:12px; line-height:1.5;">{desc}</p>
            </div>
            """)

    spacer("md")

    # Personalization Flow
    st.markdown('<div class="section-title">Choose Your Experience</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Full personalization takes 5-8 minutes — or skip straight to chat</p>', unsafe_allow_html=True)

    flow_cols = st.columns(2)
    with flow_cols[0]:
        card("""
        <div style="text-align:center;">
            <div style="font-size:40px; margin-bottom:12px;">🧠 + 🎭</div>
            <div class="section-subtitle" style="font-size:18px; color:#C4B5FD; margin-bottom:8px;">Full Personalization</div>
            <p class="hero-subtitle" style="margin:0 0 12px;">Complete both assessments for the most personalized experience</p>
            <div style="text-align:left; padding:0 1rem;">
                <p style="color:#93C5FD; font-size:13px; margin:4px 0;">✓ Step 1: Big Five Personality (20 questions)</p>
                <p style="color:#C4B5FD; font-size:13px; margin:4px 0;">✓ Step 2: COPE Coping Style (28 questions)</p>
                <p style="color:#6EE7B7; font-size:13px; margin:4px 0;">✓ Result: AI adapts tone, suggestions & responses</p>
            </div>
        </div>
        """)
    
    with flow_cols[1]:
        card("""
        <div style="text-align:center;">
            <div style="font-size:40px; margin-bottom:12px;">💬</div>
            <div class="section-subtitle" style="font-size:18px; color:#A5B4FC; margin-bottom:8px;">General Chat</div>
            <p class="hero-subtitle" style="margin:0 0 12px;">Start chatting immediately with manual personality selection</p>
            <div style="text-align:left; padding:0 1rem;">
                <p style="color:#9CA3AF; font-size:13px; margin:4px 0;">✓ 5 Conversation Modes</p>
                <p style="color:#9CA3AF; font-size:13px; margin:4px 0;">✓ 5 Companion Personalities</p>
                <p style="color:#9CA3AF; font-size:13px; margin:4px 0;">✓ Real-time emotion detection still active</p>
            </div>
        </div>
        """)

    spacer("md")

    # Conversation Modes
    st.markdown('<div class="section-title">5 Conversation Modes</div>', unsafe_allow_html=True)
    
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

    st.markdown('<div class="section-title">A calmer, personalized chat experience</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Rounded bubbles, soft gradients, and AI that adapts to your unique personality.</p>', unsafe_allow_html=True)

    chat_col1, chat_col2 = st.columns([1,1])
    with chat_col1:
        card("""
        <div class="chat-shell">
            <div class="chat-bubble chat-user">I need to know why customers churned last month.</div>
            <div class="chat-meta">You • just now</div>
            <div class="chat-bubble chat-ai">Top emotions: frustration, confusion. Root causes: onboarding gaps and slow support handoffs. Recommend: guided checklists and proactive nudges.</div>
            <div class="chat-meta">Business Buddy • a moment ago</div>
        </div>
        """)
    with chat_col2:
        card("""
        <div class="chat-shell">
            <div class="chat-bubble chat-user">Feeling anxious after back-to-back meetings.</div>
            <div class="chat-meta">You • just now</div>
            <div class="chat-bubble chat-ai">I hear you — that sounds draining. 💜 Based on your profile, taking a few minutes to step away often helps you reset. Want to try a quick breathing exercise or just talk it through?</div>
            <div class="chat-meta">Personal Companion • adapting to your style</div>
        </div>
        """)

    spacer("lg")

    st.markdown('<div style="display:flex; gap:16px; flex-wrap:wrap; align-items:center;">' + gradient_button('Launch Business Buddy', '/Business_Chatbot') + '<a class="btn-ghost" href="/Personal_Chatbot">Open Personal Companion</a>' + '</div>', unsafe_allow_html=True)

    spacer("xl")
    st.markdown('</div>', unsafe_allow_html=True)

render_footer()
