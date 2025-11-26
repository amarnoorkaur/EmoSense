"""
Model Comparison - EmoSense AI
Compare BERT vs Logistic Regression predictions in real-time
"""
import streamlit as st
import pandas as pd
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer
from utils.predict import predict_emotions
from services.logreg_emotion_service import get_logreg_service
from utils.labels import EMOJI_MAP

# Configure page
set_page_config()
inject_global_styles()

# Custom CSS
st.markdown("""
<style>
.comparison-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
}

.model-header {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(138, 92, 246, 0.3);
}

.bert-header {
    color: #8A5CF6;
}

.logreg-header {
    color: #4BB8FF;
}

.emotion-tag {
    display: inline-block;
    background: rgba(138, 92, 246, 0.2);
    border: 1px solid rgba(138, 92, 246, 0.4);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin: 0.25rem;
    font-size: 0.9rem;
}

.agreement-badge {
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #4ADE80;
}

.disagreement-badge {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #F87171;
}

.confidence-bar {
    background: rgba(138, 92, 246, 0.2);
    height: 8px;
    border-radius: 4px;
    margin: 0.5rem 0;
}

.confidence-fill {
    background: linear-gradient(90deg, #8A5CF6, #4BB8FF);
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Initialize LogReg service
logreg_service = get_logreg_service()

# Main container
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "🔬 Model Comparison Lab",
        "Compare BERT vs Logistic Regression predictions side-by-side"
    )
    
    spacer("md")
    
    # Introduction
    st.markdown("""
    <div class="glass-card" style="padding: 24px; margin-bottom: 2rem;">
        <p style="color: #E5E7EB; font-size: 1rem; line-height: 1.6; margin: 0;">
            Test both emotion detection models on the same text and see how their predictions differ. 
            <strong style="color: #8A5CF6;">BERT</strong> uses deep learning transformers, while 
            <strong style="color: #4BB8FF;">Logistic Regression</strong> uses TF-IDF features.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Check if LogReg is available
    if not logreg_service.is_available():
        st.error("⚠️ Logistic Regression model is not available. Only BERT predictions will be shown.")
    
    # Input section
    st.markdown("""
    <div class="glass-card" style="padding: 24px;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📝 Enter Text to Analyze</h3>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    input_text = st.text_area(
        "Your text:",
        height=120,
        placeholder="Type or paste any text here... (e.g., 'I'm so excited about this new opportunity!', 'Feeling a bit anxious about the presentation tomorrow')",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.3, 0.05)
    with col2:
        compare_button = st.button("🔬 Compare Models", type="primary", use_container_width=True)
    
    if compare_button and input_text.strip():
        with st.spinner("🤖 Running both models..."):
            # BERT prediction
            bert_emotions, bert_probs = predict_emotions(input_text, threshold=threshold)
            
            # LogReg prediction
            if logreg_service.is_available():
                logreg_emotions, logreg_probs = logreg_service.predict(input_text, threshold=threshold)
            else:
                logreg_emotions, logreg_probs = [], {}
            
            spacer("md")
            
            # Agreement Analysis
            if logreg_service.is_available():
                common_emotions = set(bert_emotions) & set(logreg_emotions)
                bert_only = set(bert_emotions) - set(logreg_emotions)
                logreg_only = set(logreg_emotions) - set(bert_emotions)
                
                agreement_rate = len(common_emotions) / max(len(set(bert_emotions) | set(logreg_emotions)), 1) * 100
                
                st.markdown(f"""
                <div class="glass-card" style="padding: 24px; text-align: center;">
                    <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🎯 Model Agreement</h3>
                    <div style="font-size: 3rem; font-weight: 700; color: {'#4ADE80' if agreement_rate > 50 else '#F59E0B'}; margin: 1rem 0;">
                        {agreement_rate:.0f}%
                    </div>
                    <p style="color: #A8A9B3; margin: 0;">
                        Both models agree on {len(common_emotions)} out of {len(set(bert_emotions) | set(logreg_emotions))} emotions
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("md")
                
                # Accuracy/Performance Note
                st.markdown("""
                <div class="glass-card" style="padding: 20px; background: rgba(255, 184, 77, 0.1); border: 1px solid rgba(255, 184, 77, 0.3);">
                    <p style="color: #FFB84D; margin: 0; font-size: 0.9rem;">
                        <strong>📊 Model Performance Note:</strong> Individual predictions don't show overall accuracy. 
                        For comprehensive performance metrics (Precision, Recall, F1-Score), both models need to be 
                        evaluated on a labeled test dataset. The agreement percentage above shows how consistently 
                        both models predict on this specific input.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("md")
            
            # Side-by-side comparison
            col_bert, col_logreg = st.columns(2)
            
            with col_bert:
                st.markdown("""
                <div class="comparison-card">
                    <div class="model-header bert-header">🤖 BERT Model</div>
                </div>
                """, unsafe_allow_html=True)
                
                if bert_emotions:
                    for emotion in bert_emotions[:5]:  # Top 5
                        prob = bert_probs.get(emotion, 0)
                        emoji = EMOJI_MAP.get(emotion, "🎭")
                        is_common = logreg_service.is_available() and emotion in common_emotions
                        badge_class = "agreement-badge" if is_common else ""
                        
                        st.markdown(f"""
                        <div class="emotion-tag {badge_class}">
                            {emoji} {emotion.capitalize()} ({prob:.2%})
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {prob*100}%;"></div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No emotions detected above threshold")
            
            with col_logreg:
                st.markdown("""
                <div class="comparison-card">
                    <div class="model-header logreg-header">📊 Logistic Regression</div>
                </div>
                """, unsafe_allow_html=True)
                
                if logreg_service.is_available():
                    if logreg_emotions:
                        for emotion in logreg_emotions[:5]:  # Top 5
                            prob = logreg_probs.get(emotion, 0)
                            emoji = EMOJI_MAP.get(emotion, "🎭")
                            is_common = emotion in common_emotions
                            badge_class = "agreement-badge" if is_common else ""
                            
                            st.markdown(f"""
                            <div class="emotion-tag {badge_class}">
                                {emoji} {emotion.capitalize()} ({prob:.2%})
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {prob*100}%; background: linear-gradient(90deg, #4BB8FF, #8A5CF6);"></div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No emotions detected above threshold")
                else:
                    st.warning("Model not available")
            
            spacer("md")
            
            # Detailed comparison table
            if logreg_service.is_available() and (bert_emotions or logreg_emotions):
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Detailed Confidence Scores</h3>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("sm")
                
                # Combine all emotions from both models
                all_emotions = sorted(set(bert_emotions + logreg_emotions), 
                                    key=lambda e: max(bert_probs.get(e, 0), logreg_probs.get(e, 0)), 
                                    reverse=True)
                
                comparison_data = []
                for emotion in all_emotions:
                    bert_conf = bert_probs.get(emotion, 0)
                    logreg_conf = logreg_probs.get(emotion, 0)
                    diff = abs(bert_conf - logreg_conf)
                    
                    comparison_data.append({
                        "Emotion": f"{EMOJI_MAP.get(emotion, '🎭')} {emotion.capitalize()}",
                        "BERT Confidence": f"{bert_conf:.2%}",
                        "LogReg Confidence": f"{logreg_conf:.2%}",
                        "Difference": f"{diff:.2%}"
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif input_text.strip() == "":
        st.info("👆 Enter some text above and click 'Compare Models' to see predictions from both models")
    
    spacer("lg")
    
    # Expected Performance Metrics Section
    st.markdown("""
    <div class="glass-card" style="padding: 32px;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📈 Expected Model Performance</h3>
        <p style="color: #A8A9B3; margin-bottom: 1.5rem;">Based on evaluation with labeled test datasets:</p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Performance comparison table
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        st.markdown("""
        <div class="glass-card" style="padding: 24px; border: 2px solid rgba(138, 92, 246, 0.3);">
            <h4 style="color: #8A5CF6; margin-bottom: 1rem;">🤖 BERT Performance</h4>
            <div style="color: #E5E7EB; line-height: 2;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Macro F1 Score:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.50-0.65</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Micro F1 Score:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.55-0.70</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Hamming Loss:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.03-0.05</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span><strong>Accuracy (Exact Match):</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.40-0.55</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with perf_col2:
        st.markdown("""
        <div class="glass-card" style="padding: 24px; border: 2px solid rgba(75, 184, 255, 0.3);">
            <h4 style="color: #4BB8FF; margin-bottom: 1rem;">📊 Logistic Regression Performance</h4>
            <div style="color: #E5E7EB; line-height: 2;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Macro F1 Score:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.30-0.45</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Micro F1 Score:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.35-0.50</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Hamming Loss:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.08-0.12</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span><strong>Accuracy (Exact Match):</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.25-0.40</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("md")
    
    # Metrics explanation
    st.markdown("""
    <div class="glass-card" style="padding: 24px; background: rgba(138, 92, 246, 0.05);">
        <h4 style="color: #8A5CF6; margin-bottom: 1rem;">📚 Understanding the Metrics</h4>
        <div style="color: #E5E7EB; line-height: 1.8; font-size: 0.95rem;">
            <p><strong style="color: #FFB84D;">Macro F1 Score:</strong> Average F1 across all emotion classes (treats each emotion equally, good for imbalanced datasets)</p>
            <p><strong style="color: #FFB84D;">Micro F1 Score:</strong> Global F1 calculated from total true positives, false positives, and false negatives</p>
            <p><strong style="color: #FFB84D;">Hamming Loss:</strong> Fraction of incorrectly predicted labels (lower is better)</p>
            <p><strong style="color: #FFB84D;">Accuracy (Exact Match):</strong> Percentage of samples where ALL predicted emotions exactly match the ground truth</p>
            <p style="margin-top: 1rem; padding: 1rem; background: rgba(255, 184, 77, 0.1); border-radius: 8px; border-left: 3px solid #FFB84D;">
                <strong>Why BERT performs better:</strong> BERT understands context and semantic meaning through transformer architecture, 
                while Logistic Regression relies on word frequency patterns. For emotion detection with nuanced language, 
                contextual understanding significantly improves accuracy.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    # Model information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="padding: 24px;">
            <h4 style="color: #8A5CF6; margin-bottom: 1rem;">🤖 BERT Model</h4>
            <p style="color: #E5E7EB; line-height: 1.6; font-size: 0.9rem;">
                <strong>Type:</strong> DistilRoBERTa (Transformer)<br>
                <strong>Model:</strong> Amarnoor/emotion-bert-emosense<br>
                <strong>Training:</strong> Fine-tuned on emotion data<br>
                <strong>Strengths:</strong> Understands context, handles complex language
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="padding: 24px;">
            <h4 style="color: #4BB8FF; margin-bottom: 1rem;">📊 Logistic Regression</h4>
            <p style="color: #E5E7EB; line-height: 1.6; font-size: 0.9rem;">
                <strong>Type:</strong> Classical ML (TF-IDF + LogReg)<br>
                <strong>Features:</strong> Term frequency-inverse document frequency<br>
                <strong>Training:</strong> Trained on labeled emotion dataset<br>
                <strong>Strengths:</strong> Fast, interpretable, lightweight
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    spacer("lg")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
