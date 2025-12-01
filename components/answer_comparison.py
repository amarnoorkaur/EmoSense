"""
Answer Comparison UI Component for Business Buddy
Shows side-by-side comparison of Raw ChatGPT vs Refined Business Buddy responses
Demonstrates the power of prompt engineering
"""

import streamlit as st
from services.answer_comparison_service import get_comparison_service


# =============================================================================
# CSS STYLES FOR COMPARISON CARDS
# =============================================================================

COMPARISON_STYLES = """
<style>
/* Container for comparison section */
.comparison-container {
    margin: 2rem 0;
}

/* Raw response card - grey theme */
.raw-response-card {
    background: rgba(75, 85, 99, 0.2);
    border: 1px solid rgba(75, 85, 99, 0.4);
    border-radius: 16px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.raw-response-card h4 {
    color: #9CA3AF;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(156, 163, 175, 0.3);
}

.raw-response-card .response-content {
    color: #D1D5DB;
    line-height: 1.7;
    font-size: 0.95rem;
}

/* Refined response card - blue/purple theme */
.refined-response-card {
    background: linear-gradient(135deg, rgba(138, 92, 246, 0.15), rgba(59, 130, 246, 0.15));
    border: 1px solid rgba(138, 92, 246, 0.4);
    border-radius: 16px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 4px 15px rgba(138, 92, 246, 0.2);
}

.refined-response-card h4 {
    color: #A78BFA;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(167, 139, 250, 0.3);
}

.refined-response-card .response-content {
    color: #E5E7EB;
    line-height: 1.7;
    font-size: 0.95rem;
}

/* Badge styles */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 0.5rem;
}

.badge-basic {
    background: rgba(107, 114, 128, 0.3);
    color: #9CA3AF;
}

.badge-enhanced {
    background: rgba(138, 92, 246, 0.3);
    color: #A78BFA;
}

/* Improvements panel */
.improvements-panel {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-top: 1.5rem;
}

.improvements-panel h5 {
    color: #10B981;
    margin-bottom: 0.75rem;
}

.improvement-item {
    color: #6EE7B7;
    padding: 0.25rem 0;
    font-size: 0.9rem;
}

/* Stats comparison */
.stats-row {
    display: flex;
    justify-content: space-around;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #8A5CF6;
}

.stat-label {
    font-size: 0.75rem;
    color: #9CA3AF;
    text-transform: uppercase;
}

/* Example questions */
.example-questions {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 1rem;
}

.example-btn {
    background: rgba(138, 92, 246, 0.2);
    border: 1px solid rgba(138, 92, 246, 0.4);
    color: #A78BFA;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.2s;
}

.example-btn:hover {
    background: rgba(138, 92, 246, 0.4);
}
</style>
"""

# =============================================================================
# EXAMPLE QUESTIONS
# =============================================================================

EXAMPLE_QUESTIONS = [
    "How do I improve customer satisfaction?",
    "What should I do when customers complain about shipping delays?",
    "How can I reduce negative reviews?",
    "What's the best way to handle angry customers?",
    "How do I increase customer retention?"
]


# =============================================================================
# MAIN UI COMPONENT
# =============================================================================

def render_answer_comparison():
    """
    Render the complete Answer Comparison UI component
    Shows Raw vs Refined response comparison
    """
    # Inject custom styles
    st.markdown(COMPARISON_STYLES, unsafe_allow_html=True)
    
    # Section header
    st.markdown("""
    <div class="glass-card" style="padding: 24px; margin-bottom: 2rem; text-align: center;">
        <h2 style="color: #FFFFFF; margin-bottom: 0.5rem;">🔬 Raw vs Refined Answer Comparison</h2>
        <p style="color: #A8A9B3; margin: 0;">
            See how <strong style="color: #8A5CF6;">prompt engineering</strong> transforms generic AI responses 
            into structured, actionable business insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get comparison service
    comparison_service = get_comparison_service()
    
    if not comparison_service:
        st.error("⚠️ Comparison service is not available. Please check your OpenAI API key.")
        return
    
    # Example questions section
    st.markdown("""
    <div class="example-questions">
        <p style="color: #9CA3AF; margin-bottom: 0.5rem; font-size: 0.9rem;">
            💡 <strong>Try an example question:</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Example question buttons
    example_cols = st.columns(len(EXAMPLE_QUESTIONS))
    selected_example = None
    
    for i, (col, question) in enumerate(zip(example_cols, EXAMPLE_QUESTIONS)):
        with col:
            if st.button(f"📌 {i+1}", key=f"example_{i}", help=question, use_container_width=True):
                selected_example = question
    
    # Show which example was selected
    if selected_example:
        st.session_state.comparison_question = selected_example
    
    # Input section
    st.markdown("---")
    
    # Text input for question
    default_value = st.session_state.get("comparison_question", "")
    question = st.text_input(
        "🎯 Ask a business-related question:",
        value=default_value,
        placeholder="e.g., How do I improve customer satisfaction?",
        key="business_question_input"
    )
    
    # Update session state if user types
    if question != default_value:
        st.session_state.comparison_question = question
    
    # Compare button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        compare_clicked = st.button(
            "🔍 Compare Responses", 
            type="primary", 
            use_container_width=True,
            disabled=not question.strip()
        )
    
    # Show differences toggle
    show_analysis = st.checkbox("📊 Show detailed analysis", value=True)
    
    # Generate and display comparison
    if compare_clicked and question.strip():
        with st.spinner("🤖 Generating both responses... This may take a moment."):
            # Get both responses
            raw_result, refined_result = comparison_service.get_comparison(question)
        
        # Check for errors
        if not raw_result["success"]:
            st.error(f"❌ Raw response failed: {raw_result['response']}")
            return
        
        if not refined_result["success"]:
            st.error(f"❌ Refined response failed: {refined_result['response']}")
            return
        
        st.markdown("---")
        
        # Display comparison in two columns
        col_raw, col_refined = st.columns(2)
        
        # RAW RESPONSE CARD
        with col_raw:
            st.markdown(f"""
            <div class="raw-response-card">
                <h4>🤖 Raw ChatGPT Response <span class="badge badge-basic">Basic</span></h4>
                <div class="response-content">
                    {raw_result['response'].replace(chr(10), '<br>')}
                </div>
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-value" style="color: #9CA3AF;">{len(raw_result['response'].split())}</div>
                        <div class="stat-label">Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" style="color: #9CA3AF;">{raw_result['tokens_used'] or 'N/A'}</div>
                        <div class="stat-label">Tokens</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # REFINED RESPONSE CARD
        with col_refined:
            st.markdown(f"""
            <div class="refined-response-card">
                <h4>✨ Business Buddy Response <span class="badge badge-enhanced">Enhanced</span></h4>
                <div class="response-content">
                    {refined_result['response'].replace(chr(10), '<br>')}
                </div>
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-value">{len(refined_result['response'].split())}</div>
                        <div class="stat-label">Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{refined_result['tokens_used'] or 'N/A'}</div>
                        <div class="stat-label">Tokens</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ANALYSIS SECTION
        if show_analysis:
            st.markdown("---")
            
            # Analyze differences
            analysis = comparison_service.analyze_differences(
                raw_result['response'], 
                refined_result['response']
            )
            
            # Improvements panel
            improvements = [imp for imp in analysis['improvements'] if imp]
            
            st.markdown("""
            <div class="glass-card" style="padding: 24px; margin-top: 1rem;">
                <h3 style="color: #10B981; margin-bottom: 1rem;">📈 Why Business Buddy is Better</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics comparison
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric(
                    "📝 Sections", 
                    analysis['structure_improvement']['refined_sections'],
                    delta=analysis['structure_improvement']['refined_sections'] - analysis['structure_improvement']['raw_sections']
                )
            
            with metric_cols[1]:
                st.metric(
                    "📌 Bullet Points",
                    analysis['structure_improvement']['refined_bullets'],
                    delta=analysis['structure_improvement']['refined_bullets'] - analysis['structure_improvement']['raw_bullets']
                )
            
            with metric_cols[2]:
                st.metric(
                    "🔢 Numbered Lists",
                    analysis['structure_improvement']['refined_numbered_lists'],
                    delta=analysis['structure_improvement']['refined_numbered_lists'] - analysis['structure_improvement']['raw_numbered_lists']
                )
            
            with metric_cols[3]:
                st.metric(
                    "📊 Word Count",
                    analysis['length']['refined_words'],
                    delta=analysis['length']['difference']
                )
            
            # Improvements list
            if improvements:
                st.markdown("""
                <div class="improvements-panel">
                    <h5>✅ Key Improvements</h5>
                </div>
                """, unsafe_allow_html=True)
                
                for imp in improvements:
                    st.markdown(f"<div class='improvement-item'>{imp}</div>", unsafe_allow_html=True)
            
            # Explanation
            st.markdown("""
            <div class="glass-card" style="padding: 20px; margin-top: 1.5rem; background: rgba(138, 92, 246, 0.05);">
                <h4 style="color: #8A5CF6; margin-bottom: 0.75rem;">🎯 How Prompt Engineering Made This Difference</h4>
                <div style="color: #E5E7EB; line-height: 1.8; font-size: 0.9rem;">
                    <p><strong>Raw ChatGPT</strong> received only: <code>"Answer the user's question directly."</code></p>
                    <p><strong>Business Buddy</strong> received a custom system prompt with:</p>
                    <ul style="margin-left: 1.5rem; color: #A8A9B3;">
                        <li>Role definition (customer feedback specialist)</li>
                        <li>Response format requirements (structure, bullets, sections)</li>
                        <li>Tone guidelines (emotion-aware, professional)</li>
                        <li>Output template (Quick Answer → Insights → Recommendations → Summary)</li>
                    </ul>
                    <p style="margin-top: 1rem; padding: 0.75rem; background: rgba(255, 184, 77, 0.1); border-radius: 8px; border-left: 3px solid #FFB84D;">
                        <strong>Result:</strong> Same AI model, dramatically different output quality through prompt engineering!
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Store results in session state for potential export
        st.session_state.last_comparison = {
            "question": question,
            "raw": raw_result,
            "refined": refined_result,
            "analysis": analysis if show_analysis else None
        }


def render_comparison_section_compact():
    """
    Render a compact version of the comparison for embedding in other pages
    """
    st.markdown(COMPARISON_STYLES, unsafe_allow_html=True)
    
    with st.expander("🔬 **Try: Raw vs Refined Answer Comparison**", expanded=False):
        render_answer_comparison()


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="Answer Comparison Test", layout="wide")
    render_answer_comparison()
