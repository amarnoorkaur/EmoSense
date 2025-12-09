"""
Model Comparison - EmoSense AI
Compare BERT vs Logistic Regression predictions in real-time
"""
import sys
import os

# Fix import path for Streamlit Cloud
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer
from utils.predict import predict_emotions
from services.logreg_emotion_service import get_logreg_service
from services.svm_emotion_service import get_svm_service
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

.svm-header {
    color: #10B981;
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

# Initialize SVM service
svm_service = get_svm_service()

# Main container
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "🔬 Model Comparison Lab",
        "Compare BERT vs Logistic Regression vs SVM predictions side-by-side"
    )
    
    spacer("md")
    
    # Introduction
    st.markdown("""
    <div class="glass-card" style="padding: 24px; margin-bottom: 2rem;">
        <p style="color: #E5E7EB; font-size: 1rem; line-height: 1.6; margin: 0;">
            Test all three emotion detection models on the same text and see how their predictions differ. 
            <strong style="color: #8A5CF6;">BERT</strong> uses deep learning transformers, 
            <strong style="color: #4BB8FF;">Logistic Regression</strong> uses TF-IDF features, and
            <strong style="color: #10B981;">SVM</strong> uses Support Vector classification with TF-IDF.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Check if LogReg is available
    if not logreg_service.is_available():
        st.warning("⚠️ Logistic Regression model is not available.")
    
    # Check if SVM is available
    if not svm_service.is_available():
        st.warning("⚠️ SVM model is not available.")
    
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
        compare_button = st.button("🔬 Compare Models", type="primary")
    
    if compare_button and input_text.strip():
        with st.spinner("🤖 Running all three models..."):
            # BERT prediction
            bert_emotions, bert_probs = predict_emotions(input_text, threshold=threshold)
            
            # LogReg prediction
            if logreg_service.is_available():
                logreg_emotions, logreg_probs = logreg_service.predict(input_text, threshold=threshold)
            else:
                logreg_emotions, logreg_probs = [], {}
            
            # SVM prediction
            if svm_service.is_available():
                svm_emotions, svm_probs = svm_service.predict(input_text, threshold=threshold)
            else:
                svm_emotions, svm_probs = [], {}
            
            spacer("md")
            
            # Agreement Analysis
            all_models_available = logreg_service.is_available() and svm_service.is_available()
            if all_models_available:
                all_emotions_set = set(bert_emotions) | set(logreg_emotions) | set(svm_emotions)
                common_all_three = set(bert_emotions) & set(logreg_emotions) & set(svm_emotions)
                bert_logreg_common = set(bert_emotions) & set(logreg_emotions)
                bert_svm_common = set(bert_emotions) & set(svm_emotions)
                logreg_svm_common = set(logreg_emotions) & set(svm_emotions)
                
                agreement_rate = len(common_all_three) / max(len(all_emotions_set), 1) * 100
                
                st.markdown(f"""
                <div class="glass-card" style="padding: 24px; text-align: center;">
                    <h3 style="color: #FFFFFF; margin-bottom: 1rem;">🎯 Model Agreement (All 3 Models)</h3>
                    <div style="font-size: 3rem; font-weight: 700; color: {'#4ADE80' if agreement_rate > 30 else '#F59E0B'}; margin: 1rem 0;">
                        {agreement_rate:.0f}%
                    </div>
                    <p style="color: #A8A9B3; margin: 0;">
                        All 3 models agree on {len(common_all_three)} emotions | 
                        BERT-LogReg: {len(bert_logreg_common)} | 
                        BERT-SVM: {len(bert_svm_common)} | 
                        LogReg-SVM: {len(logreg_svm_common)}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("md")
            
            # Side-by-side comparison (3 columns)
            col_bert, col_logreg, col_svm = st.columns(3)
            
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
                        is_common = all_models_available and emotion in common_all_three
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
                            is_common = all_models_available and emotion in common_all_three
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
            
            with col_svm:
                st.markdown("""
                <div class="comparison-card">
                    <div class="model-header svm-header">⚡ SVM Model</div>
                </div>
                """, unsafe_allow_html=True)
                
                if svm_service.is_available():
                    if svm_emotions:
                        for emotion in svm_emotions[:5]:  # Top 5
                            prob = svm_probs.get(emotion, 0)
                            emoji = EMOJI_MAP.get(emotion, "🎭")
                            is_common = all_models_available and emotion in common_all_three
                            badge_class = "agreement-badge" if is_common else ""
                            
                            st.markdown(f"""
                            <div class="emotion-tag {badge_class}">
                                {emoji} {emotion.capitalize()} ({prob:.2%})
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {prob*100}%; background: linear-gradient(90deg, #10B981, #4BB8FF);"></div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No emotions detected above threshold")
                else:
                    st.warning("Model not available")
            
            spacer("md")
            
            # Detailed comparison table
            if bert_emotions or logreg_emotions or svm_emotions:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Detailed Confidence Scores</h3>
                </div>
                """, unsafe_allow_html=True)
                
                spacer("sm")
                
                # Combine all emotions from all 3 models
                all_emotions = sorted(set(bert_emotions + logreg_emotions + svm_emotions), 
                                    key=lambda e: max(bert_probs.get(e, 0), logreg_probs.get(e, 0), svm_probs.get(e, 0)), 
                                    reverse=True)
                
                comparison_data = []
                for emotion in all_emotions:
                    bert_conf = bert_probs.get(emotion, 0)
                    logreg_conf = logreg_probs.get(emotion, 0)
                    svm_conf = svm_probs.get(emotion, 0)
                    
                    comparison_data.append({
                        "Emotion": f"{EMOJI_MAP.get(emotion, '🎭')} {emotion.capitalize()}",
                        "BERT": f"{bert_conf:.2%}",
                        "LogReg": f"{logreg_conf:.2%}",
                        "SVM": f"{svm_conf:.2%}"
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, hide_index=True)
    
    elif input_text.strip() == "":
        st.info("👆 Enter some text above and click 'Compare Models' to see predictions from all three models")
    
    spacer("lg")
    
    # Expected Performance Metrics Section
    st.markdown("""
    <div class="glass-card" style="padding: 32px;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📈 Expected Model Performance</h3>
        <p style="color: #A8A9B3; margin-bottom: 1.5rem;">Based on evaluation with labeled test datasets:</p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Performance comparison table (3 columns)
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    
    with perf_col1:
        st.markdown("""
        <div class="glass-card" style="padding: 24px; border: 2px solid rgba(138, 92, 246, 0.3);">
            <h4 style="color: #8A5CF6; margin-bottom: 1rem;">🤖 BERT Performance</h4>
            <div style="color: #E5E7EB; line-height: 2;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Macro F1:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.50-0.65</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Micro F1:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.55-0.70</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span><strong>Hamming Loss:</strong></span>
                    <span style="color: #8A5CF6; font-weight: 700;">~0.03-0.05</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with perf_col2:
        st.markdown("""
        <div class="glass-card" style="padding: 24px; border: 2px solid rgba(75, 184, 255, 0.3);">
            <h4 style="color: #4BB8FF; margin-bottom: 1rem;">📊 LogReg Performance</h4>
            <div style="color: #E5E7EB; line-height: 2;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Macro F1:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.30-0.45</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Micro F1:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.35-0.50</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span><strong>Hamming Loss:</strong></span>
                    <span style="color: #4BB8FF; font-weight: 700;">~0.08-0.12</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with perf_col3:
        st.markdown("""
        <div class="glass-card" style="padding: 24px; border: 2px solid rgba(16, 185, 129, 0.3);">
            <h4 style="color: #10B981; margin-bottom: 1rem;">⚡ SVM Performance</h4>
            <div style="color: #E5E7EB; line-height: 2;">
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Macro F1:</strong></span>
                    <span style="color: #10B981; font-weight: 700;">~0.35-0.50</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <span><strong>Micro F1:</strong></span>
                    <span style="color: #10B981; font-weight: 700;">~0.40-0.55</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                    <span><strong>Hamming Loss:</strong></span>
                    <span style="color: #10B981; font-weight: 700;">~0.06-0.10</span>
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
            <p><strong style="color: #FFB84D;">Macro F1 Score:</strong> Average F1 across all emotion classes (treats each emotion equally)</p>
            <p><strong style="color: #FFB84D;">Micro F1 Score:</strong> Global F1 calculated from total true positives, false positives, and false negatives</p>
            <p><strong style="color: #FFB84D;">Hamming Loss:</strong> Fraction of incorrectly predicted labels (lower is better)</p>
            <p style="margin-top: 1rem; padding: 1rem; background: rgba(255, 184, 77, 0.1); border-radius: 8px; border-left: 3px solid #FFB84D;">
                <strong>Why BERT performs best:</strong> BERT understands context through transformer architecture. 
                SVM performs better than LogReg due to its ability to find optimal decision boundaries in high-dimensional TF-IDF space.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
