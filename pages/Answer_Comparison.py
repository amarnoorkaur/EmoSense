"""
Answer Comparison Page - EmoSense
Shows side-by-side comparison of Raw ChatGPT vs EmoSense Persona Response
"""
import sys
import os

# Fix import path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from services.persona_engine import (
    get_persona_engine,
    compare_raw_vs_persona,
    get_all_personas,
    get_persona_metadata,
    PERSONA_METADATA
)
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# Custom CSS for comparison page
st.markdown("""
<style>
/* Comparison container */
.comparison-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin: 1.5rem 0;
}

/* Response card */
.response-card {
    background: rgba(17, 24, 39, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    height: 100%;
}

.response-card-raw {
    border: 2px solid rgba(107, 114, 128, 0.5);
}

.response-card-persona {
    border: 2px solid rgba(138, 92, 246, 0.5);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.response-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.response-icon {
    font-size: 1.5rem;
}

.response-title {
    color: #FFFFFF;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0;
}

.response-subtitle {
    color: #9CA3AF;
    font-size: 0.8rem;
    margin: 0;
}

.response-content {
    color: #E5E7EB;
    font-size: 0.95rem;
    line-height: 1.7;
    white-space: pre-wrap;
}

/* Input section */
.input-section {
    background: rgba(17, 24, 39, 0.4);
    border: 1px solid rgba(138, 92, 246, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Persona selector */
.persona-option {
    background: rgba(138, 92, 246, 0.1);
    border: 1px solid rgba(138, 92, 246, 0.3);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.persona-option:hover {
    background: rgba(138, 92, 246, 0.2);
    border-color: rgba(138, 92, 246, 0.5);
}

.persona-option.selected {
    background: rgba(138, 92, 246, 0.3);
    border-color: #8B5CF6;
}

/* Info card */
.info-card {
    background: rgba(59, 130, 246, 0.1);
    border-left: 4px solid #3B82F6;
    padding: 1rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1.5rem;
}

.info-card p {
    color: #93C5FD;
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Loading state */
.loading-placeholder {
    background: rgba(138, 92, 246, 0.1);
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "comparison_input" not in st.session_state:
    st.session_state.comparison_input = ""

if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = None

if "selected_comparison_persona" not in st.session_state:
    st.session_state.selected_comparison_persona = st.session_state.get("persona", "Gentle Sensitive")


def render_persona_selector():
    """Renders the persona selection UI."""
    st.markdown("### 🎭 Select Persona for Comparison")
    
    personas = get_all_personas()
    current_persona = st.session_state.selected_comparison_persona
    
    cols = st.columns(len(personas))
    
    for i, (name, meta) in enumerate(personas.items()):
        with cols[i]:
            is_selected = name == current_persona
            border_color = meta['color'] if is_selected else "rgba(138, 92, 246, 0.3)"
            bg_color = f"{meta['color']}20" if is_selected else "rgba(17, 24, 39, 0.4)"
            
            if st.button(
                f"{meta['emoji']} {name.split()[0]}",
                key=f"persona_btn_{name}",
                help=meta['short_desc']
            ):
                st.session_state.selected_comparison_persona = name
                st.session_state.comparison_results = None  # Clear old results
                st.rerun()
    
    # Show selected persona info
    selected_meta = get_persona_metadata(current_persona)
    st.markdown(f"""
    <div style="background: {selected_meta['color']}15; border: 1px solid {selected_meta['color']}40; 
                border-radius: 8px; padding: 1rem; margin-top: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">{selected_meta['emoji']}</span>
            <div>
                <div style="color: #FFFFFF; font-weight: 600;">{current_persona}</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">{selected_meta['short_desc']}</div>
            </div>
        </div>
        <div style="color: #C4B5FD; font-size: 0.8rem; margin-top: 0.5rem;">
            Based on: {selected_meta['therapy_style']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_comparison_results(raw_response: str, persona_response: str, persona: str):
    """Renders the side-by-side comparison of responses."""
    
    persona_meta = get_persona_metadata(persona)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="response-card response-card-raw">
            <div class="response-header">
                <span class="response-icon">🤖</span>
                <div>
                    <p class="response-title">ChatGPT Default</p>
                    <p class="response-subtitle">No persona • Raw response</p>
                </div>
            </div>
            <div class="response-content">{raw_response}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="response-card response-card-persona" style="border-color: {persona_meta['color']}80;">
            <div class="response-header">
                <span class="response-icon">{persona_meta['emoji']}</span>
                <div>
                    <p class="response-title">EmoSense {persona}</p>
                    <p class="response-subtitle">{persona_meta['therapy_style']}</p>
                </div>
            </div>
            <div class="response-content">{persona_response}</div>
        </div>
        """, unsafe_allow_html=True)


# Main page content
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero section
    gradient_hero(
        "🔬 Answer Comparison",
        "See how EmoSense personas transform AI responses into emotionally intelligent support"
    )
    
    # Info card
    st.markdown("""
    <div class="info-card">
        <p>
            <strong>How it works:</strong> Enter any message and see the difference between a standard 
            ChatGPT response and an EmoSense persona-enhanced response. This demonstrates how our 
            persona prompts transform generic AI into tailored emotional support.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Persona selector
    render_persona_selector()
    
    spacer("md")
    
    # Input section
    st.markdown("### 💬 Enter Your Message")
    
    user_input = st.text_area(
        "Your message",
        value=st.session_state.comparison_input,
        height=120,
        placeholder="Type something you'd say to an emotional support chatbot...\n\nExamples:\n• 'I'm feeling really overwhelmed with work lately'\n• 'I had a fight with my friend and I feel awful'\n• 'I'm anxious about an upcoming presentation'",
        label_visibility="collapsed",
        key="comparison_text_input"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        compare_button = st.button(
            "🔄 Compare Responses",
            type="primary",
            disabled=not user_input.strip(),
            key="compare_btn"
        )
    
    spacer("md")
    
    # Handle comparison
    if compare_button and user_input.strip():
        st.session_state.comparison_input = user_input
        
        with st.spinner("🔄 Generating both responses..."):
            engine = get_persona_engine()
            
            if engine:
                raw_response, persona_response = engine.compare_answers(
                    user_input,
                    st.session_state.selected_comparison_persona
                )
                
                st.session_state.comparison_results = {
                    "raw": raw_response,
                    "persona": persona_response,
                    "persona_name": st.session_state.selected_comparison_persona,
                    "input": user_input
                }
            else:
                st.error("🔑 OpenAI API key not configured. Please set OPENAI_API_KEY.")
    
    # Display results
    if st.session_state.comparison_results:
        results = st.session_state.comparison_results
        
        st.markdown("### 📊 Comparison Results")
        st.markdown(f"""
        <div style="background: rgba(17, 24, 39, 0.4); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <span style="color: #9CA3AF;">Your message:</span>
            <span style="color: #E5E7EB; font-style: italic;"> "{results['input']}"</span>
        </div>
        """, unsafe_allow_html=True)
        
        render_comparison_results(
            results["raw"],
            results["persona"],
            results["persona_name"]
        )
        
        spacer("md")
        
        # Key differences section
        st.markdown("""
        <div style="background: rgba(138, 92, 246, 0.1); border: 1px solid rgba(138, 92, 246, 0.3); 
                    border-radius: 12px; padding: 1.5rem; margin-top: 1rem;">
            <h4 style="color: #FFFFFF; margin: 0 0 1rem;">✨ What Makes the Difference?</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #9CA3AF; font-weight: 600; margin-bottom: 0.5rem;">ChatGPT Default:</p>
                    <ul style="color: #D1D5DB; margin: 0; padding-left: 1.25rem; font-size: 0.9rem;">
                        <li>Generic, one-size-fits-all response</li>
                        <li>No therapeutic framework</li>
                        <li>May jump to advice too quickly</li>
                    </ul>
                </div>
                <div>
                    <p style="color: #C4B5FD; font-weight: 600; margin-bottom: 0.5rem;">EmoSense Persona:</p>
                    <ul style="color: #D1D5DB; margin: 0; padding-left: 1.25rem; font-size: 0.9rem;">
                        <li>Tailored to user's coping style</li>
                        <li>Based on therapeutic principles</li>
                        <li>Emotionally intelligent approach</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Placeholder when no results
        st.markdown("""
        <div class="loading-placeholder">
            <p style="font-size: 1.5rem; margin-bottom: 0.5rem;">👆</p>
            <p>Enter a message above and click "Compare Responses" to see the difference</p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Try different personas section
    st.markdown("### 🎭 Try Different Personas")
    st.markdown("""
    <p style="color: #9CA3AF; margin-bottom: 1rem;">
        Each persona is designed for different emotional support needs. 
        Try the same message with different personas to see how EmoSense adapts.
    </p>
    """, unsafe_allow_html=True)
    
    # Quick persona descriptions
    for name, meta in PERSONA_METADATA.items():
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem; 
                    background: rgba(17, 24, 39, 0.3); border-radius: 8px; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem;">{meta['emoji']}</span>
            <div style="flex-grow: 1;">
                <span style="color: #FFFFFF; font-weight: 500;">{name}</span>
                <span style="color: #9CA3AF;"> — {meta['short_desc']}</span>
            </div>
            <span style="color: #6B7280; font-size: 0.8rem;">{meta['therapy_style']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("lg")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
