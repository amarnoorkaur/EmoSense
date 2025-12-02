"""
Brief COPE Onboarding Page for EmoSense
Implements the full 28-item Brief COPE questionnaire with persona mapping.

This is for educational/research purposes (UFV university project).
"""
import sys
import os

# Fix import path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from typing import Dict, List, Optional
from services.cope_assessment_service import (
    get_cope_questions,
    get_response_options,
    get_subscale_info,
    get_persona_info,
    compute_cope_scores,
    assign_persona,
    get_dominant_coping_styles,
    get_coping_profile_summary,
    COPE_QUESTIONS,
    RESPONSE_OPTIONS,
    SUBSCALE_INFO,
    PERSONA_INFO
)
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# ============================================================
# CUSTOM CSS FOR ONBOARDING
# ============================================================

st.markdown("""
<style>
/* Onboarding container */
.onboarding-container {
    max-width: 800px;
    margin: 0 auto;
}

/* Question card */
.question-card {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(138, 92, 246, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.question-card:hover {
    border-color: rgba(138, 92, 246, 0.4);
    background: rgba(17, 24, 39, 0.8);
}

.question-number {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 0.75rem;
}

.question-text {
    color: #E5E7EB;
    font-size: 1rem;
    line-height: 1.5;
}

/* Progress bar */
.progress-container {
    background: rgba(17, 24, 39, 0.6);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(138, 92, 246, 0.2);
}

.progress-bar {
    background: rgba(75, 85, 99, 0.5);
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
}

.progress-fill {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    height: 100%;
    border-radius: 8px;
    transition: width 0.3s ease;
}

.progress-text {
    color: #9CA3AF;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    text-align: center;
}

/* Results card */
.results-card {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(138, 92, 246, 0.3);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.persona-card {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
    border: 2px solid rgba(138, 92, 246, 0.5);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.persona-emoji {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.persona-name {
    color: #FFFFFF;
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.persona-description {
    color: #C4B5FD;
    font-size: 1rem;
    line-height: 1.6;
}

/* Score bar */
.score-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
}

.score-label {
    color: #E5E7EB;
    font-size: 0.875rem;
    width: 180px;
    flex-shrink: 0;
}

.score-bar-bg {
    flex-grow: 1;
    background: rgba(75, 85, 99, 0.3);
    border-radius: 6px;
    height: 8px;
    margin: 0 0.75rem;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 0.5s ease;
}

.score-value {
    color: #9CA3AF;
    font-size: 0.8rem;
    width: 40px;
    text-align: right;
}

/* Intro card */
.intro-card {
    background: rgba(138, 92, 246, 0.1);
    border-left: 4px solid #8A5CF6;
    padding: 1.25rem;
    border-radius: 0 12px 12px 0;
    margin-bottom: 2rem;
}

.intro-card p {
    color: #C4B5FD;
    margin: 0;
    line-height: 1.6;
}

/* Section header */
.section-header {
    color: #FFFFFF;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 1.5rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(138, 92, 246, 0.3);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def init_session_state():
    """Initialize all session state variables for onboarding."""
    if "cope_answers" not in st.session_state:
        st.session_state.cope_answers = {}
    
    if "cope_scores" not in st.session_state:
        st.session_state.cope_scores = None
    
    if "persona" not in st.session_state:
        st.session_state.persona = None
    
    if "persona_info" not in st.session_state:
        st.session_state.persona_info = None
    
    if "onboarding_complete" not in st.session_state:
        st.session_state.onboarding_complete = False
    
    if "show_results" not in st.session_state:
        st.session_state.show_results = False


# ============================================================
# PART 2: UI COMPONENTS
# ============================================================

def render_progress_bar(answered: int, total: int):
    """
    Renders a progress bar showing questionnaire completion.
    
    Args:
        answered: Number of questions answered
        total: Total number of questions
    """
    percentage = (answered / total) * 100
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%;"></div>
        </div>
        <div class="progress-text">
            {answered} of {total} questions answered ({percentage:.0f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_question(question: Dict, index: int) -> Optional[int]:
    """
    Renders a single questionnaire item with radio buttons.
    
    Args:
        question: Question dictionary with id, text, subscale
        index: Question index (1-based)
        
    Returns:
        Selected response value (1-4) or None
    """
    qid = question["id"]
    
    # Get existing answer if any
    existing_answer = st.session_state.cope_answers.get(qid, None)
    
    # Create options list
    options = [None] + list(RESPONSE_OPTIONS.keys())  # None = not answered
    
    # Format function for display
    def format_option(val):
        if val is None:
            return "Select your response..."
        return f"{val} - {RESPONSE_OPTIONS[val]}"
    
    # Determine default index
    if existing_answer is not None:
        default_index = options.index(existing_answer)
    else:
        default_index = 0
    
    # Render question
    st.markdown(f"""
    <div class="question-card">
        <span class="question-number">{index}</span>
        <span class="question-text">{question['text']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Radio selection
    response = st.radio(
        f"Question {index}",
        options=options,
        format_func=format_option,
        index=default_index,
        key=f"cope_{qid}",
        label_visibility="collapsed",
        horizontal=True
    )
    
    # Store answer if valid
    if response is not None:
        st.session_state.cope_answers[qid] = response
    
    return response


def render_questions_by_section():
    """
    Renders all 28 questions organized by subscale sections.
    """
    questions = get_cope_questions()
    
    # Group questions by subscale for better organization
    current_subscale = None
    question_num = 1
    
    for question in questions:
        subscale = question["subscale"]
        subscale_info = SUBSCALE_INFO[subscale]
        
        # Show section header when subscale changes
        if subscale != current_subscale:
            st.markdown(f"""
            <div class="section-header">
                {subscale_info['emoji']} {subscale_info['name']}
            </div>
            """, unsafe_allow_html=True)
            current_subscale = subscale
        
        render_question(question, question_num)
        question_num += 1
        
    spacer("sm")


def render_all_questions():
    """
    Renders all 28 questions in sequential order.
    """
    questions = get_cope_questions()
    
    for i, question in enumerate(questions, 1):
        render_question(question, i)
        
        # Add small spacing every 4 questions
        if i % 4 == 0 and i < len(questions):
            st.markdown("<hr style='border-color: rgba(138, 92, 246, 0.2); margin: 1.5rem 0;'>", 
                       unsafe_allow_html=True)


def validate_answers() -> bool:
    """
    Validates that all questions have been answered.
    
    Returns:
        True if all questions answered, False otherwise
    """
    questions = get_cope_questions()
    answered = len(st.session_state.cope_answers)
    total = len(questions)
    
    return answered == total


def get_unanswered_questions() -> List[int]:
    """
    Returns list of unanswered question numbers.
    
    Returns:
        List of question indices (1-based) that are unanswered
    """
    questions = get_cope_questions()
    unanswered = []
    
    for i, question in enumerate(questions, 1):
        if question["id"] not in st.session_state.cope_answers:
            unanswered.append(i)
    
    return unanswered


# ============================================================
# PART 5: RESULTS SUMMARY PAGE
# ============================================================

def render_score_bar(subscale: str, score: float, color: str = "#8A5CF6"):
    """
    Renders a horizontal score bar for a subscale.
    
    Args:
        subscale: Subscale key
        score: Score value (1.0 - 4.0)
        color: Bar fill color
    """
    info = SUBSCALE_INFO.get(subscale, {"name": subscale, "emoji": "📊"})
    percentage = (score / 4.0) * 100
    
    st.markdown(f"""
    <div class="score-item">
        <span class="score-label">{info['emoji']} {info['name']}</span>
        <div class="score-bar-bg">
            <div class="score-bar-fill" style="width: {percentage}%; background: {color};"></div>
        </div>
        <span class="score-value">{score:.1f}</span>
    </div>
    """, unsafe_allow_html=True)


def cope_results_page():
    """
    Renders the results summary page after questionnaire completion.
    """
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #FFFFFF;">🎉 Your Coping Profile</h1>
        <p style="color: #9CA3AF;">Based on your Brief COPE Assessment responses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get stored data
    scores = st.session_state.cope_scores
    persona = st.session_state.persona
    persona_info = st.session_state.persona_info
    
    if not scores or not persona:
        st.error("❌ Results not found. Please complete the assessment first.")
        if st.button("🔄 Start Assessment"):
            st.session_state.show_results = False
            st.rerun()
        return
    
    # Persona Card
    st.markdown(f"""
    <div class="persona-card">
        <div class="persona-emoji">{persona_info['emoji']}</div>
        <div class="persona-name">{persona}</div>
        <div class="persona-description">{persona_info['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Persona traits
    col1, col2, col3 = st.columns(3)
    for i, trait in enumerate(persona_info.get('traits', [])):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div style="background: rgba(138, 92, 246, 0.15); padding: 0.75rem; 
                        border-radius: 8px; text-align: center; margin-bottom: 0.5rem;">
                <span style="color: #C4B5FD;">✓ {trait}</span>
            </div>
            """, unsafe_allow_html=True)
    
    spacer("md")
    
    # Coping Profile Summary
    profile = get_coping_profile_summary(scores)
    
    st.markdown("""
    <div class="results-card">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Your Coping Style Scores</h3>
    """, unsafe_allow_html=True)
    
    # Categorize and color-code scores
    adaptive = ["active_coping", "planning", "positive_reframing", "acceptance", 
                "emotional_support", "instrumental_support"]
    maladaptive = ["denial", "substance_use", "behavioral_disengagement", "self_blame"]
    neutral = ["self_distraction", "venting", "humor", "religion"]
    
    # Adaptive strategies (green)
    st.markdown("<p style='color: #10B981; font-weight: 600; margin: 1rem 0 0.5rem;'>Adaptive Strategies</p>", 
               unsafe_allow_html=True)
    for subscale in adaptive:
        if subscale in scores:
            render_score_bar(subscale, scores[subscale], "#10B981")
    
    # Neutral strategies (blue)
    st.markdown("<p style='color: #60A5FA; font-weight: 600; margin: 1rem 0 0.5rem;'>Neutral/Situational Strategies</p>", 
               unsafe_allow_html=True)
    for subscale in neutral:
        if subscale in scores:
            render_score_bar(subscale, scores[subscale], "#60A5FA")
    
    # Maladaptive strategies (orange/red)
    st.markdown("<p style='color: #F59E0B; font-weight: 600; margin: 1rem 0 0.5rem;'>Strategies to Monitor</p>", 
               unsafe_allow_html=True)
    for subscale in maladaptive:
        if subscale in scores:
            color = "#EF4444" if scores[subscale] > 3.0 else "#F59E0B"
            render_score_bar(subscale, scores[subscale], color)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Dominant coping styles
    dominant = profile["dominant_styles"]
    
    st.markdown("""
    <div class="results-card">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🏆 Your Top Coping Strategies</h3>
    """, unsafe_allow_html=True)
    
    for i, (subscale, score) in enumerate(dominant, 1):
        info = SUBSCALE_INFO.get(subscale, {"name": subscale, "emoji": "📊", "description": ""})
        medal = ["🥇", "🥈", "🥉"][i-1]
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem; 
                    padding: 0.75rem; background: rgba(138, 92, 246, 0.1); border-radius: 8px;">
            <span style="font-size: 1.5rem; margin-right: 0.75rem;">{medal}</span>
            <div>
                <div style="color: #FFFFFF; font-weight: 600;">{info['emoji']} {info['name']}</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">{info['description']}</div>
            </div>
            <span style="margin-left: auto; color: #C4B5FD; font-weight: 600;">{score:.1f}/4.0</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # How EmoSense will adapt
    st.markdown(f"""
    <div class="results-card">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">💜 How EmoSense Will Support You</h3>
        <p style="color: #C4B5FD; line-height: 1.8;">
            Based on your <strong>{persona}</strong> profile, EmoSense will adapt its conversation style to be:
        </p>
        <div style="background: rgba(138, 92, 246, 0.15); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <p style="color: #E5E7EB; margin: 0; font-style: italic;">
                "{persona_info['chat_style']}"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("md")
    
    # Continue button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Continue to EmoSense Companion", type="primary", key="continue_to_chat"):
            st.session_state.onboarding_complete = True
            st.switch_page("pages/Personal_Chatbot.py")
    
    spacer("sm")
    
    # Option to retake
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Retake Assessment", key="retake_assessment"):
            # Clear all assessment data
            st.session_state.cope_answers = {}
            st.session_state.cope_scores = None
            st.session_state.persona = None
            st.session_state.persona_info = None
            st.session_state.show_results = False
            st.rerun()


# ============================================================
# PART 2 (CONTINUED): MAIN ONBOARDING PAGE
# ============================================================

def cope_onboarding_page():
    """
    Main onboarding page with the Brief COPE questionnaire.
    """
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="color: #FFFFFF;">🧠 Emotional Coping Profile</h1>
        <h3 style="color: #C4B5FD; font-weight: 400;">Brief COPE Assessment</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="intro-card">
        <p>
            <strong>Welcome to EmoSense's Coping Profile Assessment!</strong><br><br>
            This questionnaire is the <strong>Brief COPE</strong> — a validated research instrument 
            that helps us understand how you typically handle stress and difficult emotions.<br><br>
            Your responses will help EmoSense personalize its emotional support to match your 
            natural coping style. There are no right or wrong answers — just choose what best 
            describes how you've been dealing with stress lately.<br><br>
            <em>📋 28 questions • ⏱️ Takes about 5-7 minutes</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    questions = get_cope_questions()
    answered = len(st.session_state.cope_answers)
    render_progress_bar(answered, len(questions))
    
    # Instructions
    st.markdown("""
    <div style="background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.3); 
                padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
        <p style="color: #FCD34D; margin: 0; font-size: 0.9rem;">
            <strong>📝 Instructions:</strong> For each statement, select how much you've been doing 
            what it describes <strong>recently when dealing with stress</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render all questions
    render_all_questions()
    
    spacer("md")
    
    # Submit section
    st.markdown("<hr style='border-color: rgba(138, 92, 246, 0.3);'>", unsafe_allow_html=True)
    
    # Show validation status
    unanswered = get_unanswered_questions()
    
    if unanswered:
        st.warning(f"⚠️ Please answer all questions. Missing: {len(unanswered)} questions (#{', #'.join(map(str, unanswered[:5]))}{'...' if len(unanswered) > 5 else ''})")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_disabled = len(unanswered) > 0
        
        if st.button("✅ Submit Assessment", type="primary", disabled=submit_disabled, 
                    key="submit_cope"):
            # Compute scores
            scores = compute_cope_scores(st.session_state.cope_answers)
            st.session_state.cope_scores = scores
            
            # Assign persona
            persona, persona_info = assign_persona(scores)
            st.session_state.persona = persona
            st.session_state.persona_info = persona_info
            
            # Show results
            st.session_state.show_results = True
            st.rerun()


# ============================================================
# MAIN PAGE LOGIC
# ============================================================

# Initialize session state
init_session_state()

# Main content
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Check if we should show results or questionnaire
    if st.session_state.show_results:
        cope_results_page()
    else:
        cope_onboarding_page()
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
