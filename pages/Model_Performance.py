"""
Model Performance - EmoSense AI
Display performance metrics for all three ML models
"""
import streamlit as st
import pandas as pd
from components.layout import set_page_config, inject_global_styles, page_container, gradient_hero, spacer
from components.footer import render_footer

# Configure page
set_page_config()
inject_global_styles()

# Custom CSS for metric cards
st.markdown("""
<style>
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    backdrop-filter: blur(10px);
}

.metric-row {
    display: flex;
    gap: 20px;
    margin: 16px 0;
    flex-wrap: wrap;
}

.metric-box {
    background: rgba(138, 92, 246, 0.15);
    border: 1px solid rgba(138, 92, 246, 0.3);
    border-radius: 12px;
    padding: 16px 20px;
    flex: 1;
    min-width: 150px;
    text-align: center;
}

.metric-label {
    color: #A8A9B3;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 1.8rem;
    font-weight: 700;
}

.model-title {
    color: #8A5CF6;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Placeholder metrics - replace these with your actual metrics
logreg_metrics = {
    "micro_f1": 0.43,
    "macro_f1": 0.34,
    "hamming_loss": 0.095,
    "classification_report": {
        "admiration": {"precision": 0.45, "recall": 0.38, "f1-score": 0.41, "support": 504},
        "amusement": {"precision": 0.52, "recall": 0.48, "f1-score": 0.50, "support": 284},
        "anger": {"precision": 0.38, "recall": 0.42, "f1-score": 0.40, "support": 198},
        "annoyance": {"precision": 0.28, "recall": 0.31, "f1-score": 0.29, "support": 320},
        "approval": {"precision": 0.35, "recall": 0.29, "f1-score": 0.32, "support": 351},
        "caring": {"precision": 0.41, "recall": 0.36, "f1-score": 0.38, "support": 135},
        "confusion": {"precision": 0.39, "recall": 0.33, "f1-score": 0.36, "support": 153},
        "curiosity": {"precision": 0.47, "recall": 0.41, "f1-score": 0.44, "support": 284},
        "desire": {"precision": 0.44, "recall": 0.38, "f1-score": 0.41, "support": 83},
        "disappointment": {"precision": 0.31, "recall": 0.28, "f1-score": 0.29, "support": 151},
        "disapproval": {"precision": 0.33, "recall": 0.37, "f1-score": 0.35, "support": 267},
        "disgust": {"precision": 0.42, "recall": 0.38, "f1-score": 0.40, "support": 123},
        "embarrassment": {"precision": 0.48, "recall": 0.41, "f1-score": 0.44, "support": 37},
        "excitement": {"precision": 0.46, "recall": 0.39, "f1-score": 0.42, "support": 103},
        "fear": {"precision": 0.52, "recall": 0.47, "f1-score": 0.49, "support": 78},
        "gratitude": {"precision": 0.68, "recall": 0.61, "f1-score": 0.64, "support": 352},
        "grief": {"precision": 0.51, "recall": 0.43, "f1-score": 0.47, "support": 6},
        "joy": {"precision": 0.49, "recall": 0.43, "f1-score": 0.46, "support": 161},
        "love": {"precipitation": 0.55, "recall": 0.48, "f1-score": 0.51, "support": 238},
        "nervousness": {"precision": 0.47, "recall": 0.39, "f1-score": 0.43, "support": 23},
        "optimism": {"precision": 0.42, "recall": 0.36, "f1-score": 0.39, "support": 186},
        "pride": {"precision": 0.53, "recall": 0.44, "f1-score": 0.48, "support": 16},
        "realization": {"precision": 0.31, "recall": 0.27, "f1-score": 0.29, "support": 145},
        "relief": {"precision": 0.49, "recall": 0.41, "f1-score": 0.45, "support": 11},
        "remorse": {"precision": 0.51, "recall": 0.43, "f1-score": 0.47, "support": 56},
        "sadness": {"precision": 0.44, "recall": 0.39, "f1-score": 0.41, "support": 156},
        "surprise": {"precision": 0.46, "recall": 0.41, "f1-score": 0.43, "support": 141},
        "neutral": {"precision": 0.32, "recall": 0.38, "f1-score": 0.35, "support": 1787}
    }
}

svm_metrics = {
    "micro_f1": 0.47,
    "macro_f1": 0.37,
    "hamming_loss": 0.089,
    "classification_report": {
        "admiration": {"precision": 0.49, "recall": 0.42, "f1-score": 0.45, "support": 504},
        "amusement": {"precision": 0.56, "recall": 0.51, "f1-score": 0.53, "support": 284},
        "anger": {"precision": 0.42, "recall": 0.46, "f1-score": 0.44, "support": 198},
        "annoyance": {"precision": 0.31, "recall": 0.35, "f1-score": 0.33, "support": 320},
        "approval": {"precision": 0.38, "recall": 0.33, "f1-score": 0.35, "support": 351},
        "caring": {"precision": 0.44, "recall": 0.39, "f1-score": 0.41, "support": 135},
        "confusion": {"precision": 0.42, "recall": 0.37, "f1-score": 0.39, "support": 153},
        "curiosity": {"precision": 0.51, "recall": 0.45, "f1-score": 0.48, "support": 284},
        "desire": {"precision": 0.47, "recall": 0.42, "f1-score": 0.44, "support": 83},
        "disappointment": {"precision": 0.34, "recall": 0.31, "f1-score": 0.32, "support": 151},
        "disapproval": {"precision": 0.36, "recall": 0.41, "f1-score": 0.38, "support": 267},
        "disgust": {"precision": 0.46, "recall": 0.42, "f1-score": 0.44, "support": 123},
        "embarrassment": {"precision": 0.52, "recall": 0.45, "f1-score": 0.48, "support": 37},
        "excitement": {"precision": 0.49, "recall": 0.43, "f1-score": 0.46, "support": 103},
        "fear": {"precision": 0.56, "recall": 0.51, "f1-score": 0.53, "support": 78},
        "gratitude": {"precision": 0.72, "recall": 0.65, "f1-score": 0.68, "support": 352},
        "grief": {"precision": 0.55, "recall": 0.47, "f1-score": 0.51, "support": 6},
        "joy": {"precision": 0.52, "recall": 0.47, "f1-score": 0.49, "support": 161},
        "love": {"precision": 0.58, "recall": 0.52, "f1-score": 0.55, "support": 238},
        "nervousness": {"precision": 0.51, "recall": 0.43, "f1-score": 0.47, "support": 23},
        "optimism": {"precision": 0.45, "recall": 0.40, "f1-score": 0.42, "support": 186},
        "pride": {"precision": 0.57, "recall": 0.48, "f1-score": 0.52, "support": 16},
        "realization": {"precision": 0.34, "recall": 0.30, "f1-score": 0.32, "support": 145},
        "relief": {"precision": 0.53, "recall": 0.45, "f1-score": 0.49, "support": 11},
        "remorse": {"precision": 0.54, "recall": 0.47, "f1-score": 0.50, "support": 56},
        "sadness": {"precision": 0.47, "recall": 0.43, "f1-score": 0.45, "support": 156},
        "surprise": {"precision": 0.49, "recall": 0.45, "f1-score": 0.47, "support": 141},
        "neutral": {"precision": 0.35, "recall": 0.42, "f1-score": 0.38, "support": 1787}
    }
}

bert_metrics = {
    "micro_f1": 0.61,
    "macro_f1": 0.50,
    "hamming_loss": 0.033,
    "classification_report": {
        "admiration": {"precision": 0.68, "recall": 0.59, "f1-score": 0.63, "support": 504},
        "amusement": {"precision": 0.74, "recall": 0.68, "f1-score": 0.71, "support": 284},
        "anger": {"precision": 0.58, "recall": 0.62, "f1-score": 0.60, "support": 198},
        "annoyance": {"precision": 0.45, "recall": 0.49, "f1-score": 0.47, "support": 320},
        "approval": {"precision": 0.52, "recall": 0.47, "f1-score": 0.49, "support": 351},
        "caring": {"precision": 0.59, "recall": 0.53, "f1-score": 0.56, "support": 135},
        "confusion": {"precision": 0.56, "recall": 0.51, "f1-score": 0.53, "support": 153},
        "curiosity": {"precision": 0.65, "recall": 0.59, "f1-score": 0.62, "support": 284},
        "desire": {"precision": 0.62, "recall": 0.56, "f1-score": 0.59, "support": 83},
        "disappointment": {"precision": 0.48, "recall": 0.43, "f1-score": 0.45, "support": 151},
        "disapproval": {"precision": 0.50, "recall": 0.55, "f1-score": 0.52, "support": 267},
        "disgust": {"precision": 0.60, "recall": 0.56, "f1-score": 0.58, "support": 123},
        "embarrassment": {"precision": 0.66, "recall": 0.59, "f1-score": 0.62, "support": 37},
        "excitement": {"precision": 0.63, "recall": 0.57, "f1-score": 0.60, "support": 103},
        "fear": {"precision": 0.70, "recall": 0.65, "f1-score": 0.67, "support": 78},
        "gratitude": {"precision": 0.86, "recall": 0.79, "f1-score": 0.82, "support": 352},
        "grief": {"precision": 0.69, "recall": 0.61, "f1-score": 0.65, "support": 6},
        "joy": {"precision": 0.66, "recall": 0.61, "f1-score": 0.63, "support": 161},
        "love": {"precision": 0.72, "recall": 0.66, "f1-score": 0.69, "support": 238},
        "nervousness": {"precision": 0.65, "recall": 0.57, "f1-score": 0.61, "support": 23},
        "optimism": {"precision": 0.59, "recall": 0.54, "f1-score": 0.56, "support": 186},
        "pride": {"precision": 0.71, "recall": 0.62, "f1-score": 0.66, "support": 16},
        "realization": {"precision": 0.48, "recall": 0.42, "f1-score": 0.45, "support": 145},
        "relief": {"precision": 0.67, "recall": 0.59, "f1-score": 0.63, "support": 11},
        "remorse": {"precision": 0.68, "recall": 0.61, "f1-score": 0.64, "support": 56},
        "sadness": {"precision": 0.61, "recall": 0.57, "f1-score": 0.59, "support": 156},
        "surprise": {"precision": 0.63, "recall": 0.59, "f1-score": 0.61, "support": 141},
        "neutral": {"precision": 0.49, "recall": 0.56, "f1-score": 0.52, "support": 1787}
    }
}

# Main container
with page_container():
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    
    # Hero
    gradient_hero(
        "📊 Model Performance",
        "Evaluation metrics for emotion detection models"
    )
    
    spacer("md")
    
    # Introduction
    st.markdown("""
    <div class="glass-card" style="padding: 24px; margin-bottom: 2rem;">
        <p style="color: #E5E7EB; font-size: 1rem; line-height: 1.6; margin: 0;">
            This page displays the performance metrics of three machine learning models trained for 
            multi-label emotion classification on the GoEmotions dataset. Each model is evaluated using 
            Micro F1, Macro F1, and Hamming Loss metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Model 1: Logistic Regression
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="model-title">🔹 Logistic Regression</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Micro F1 Score</div>
            <div class="metric-value">{logreg_metrics['micro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Macro F1 Score</div>
            <div class="metric-value">{logreg_metrics['macro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Hamming Loss</div>
            <div class="metric-value">{logreg_metrics['hamming_loss']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 View Classification Report"):
        st.json(logreg_metrics['classification_report'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("md")
    
    # Model 2: SVM
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="model-title">🔹 SVM (Support Vector Machine)</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Micro F1 Score</div>
            <div class="metric-value">{svm_metrics['micro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Macro F1 Score</div>
            <div class="metric-value">{svm_metrics['macro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Hamming Loss</div>
            <div class="metric-value">{svm_metrics['hamming_loss']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 View Classification Report"):
        st.json(svm_metrics['classification_report'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("md")
    
    # Model 3: DistilBERT
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="model-title">🔹 DistilBERT (Fine-Tuned)</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box" style="background: rgba(138, 92, 246, 0.25);">
            <div class="metric-label">Micro F1 Score</div>
            <div class="metric-value">{bert_metrics['micro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background: rgba(138, 92, 246, 0.25);">
            <div class="metric-label">Macro F1 Score</div>
            <div class="metric-value">{bert_metrics['macro_f1']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box" style="background: rgba(138, 92, 246, 0.25);">
            <div class="metric-label">Hamming Loss</div>
            <div class="metric-value">{bert_metrics['hamming_loss']:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 View Classification Report"):
        st.json(bert_metrics['classification_report'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    spacer("lg")
    
    # Comparison Chart
    st.markdown("""
    <div class="glass-card" style="padding: 32px;">
        <h3 style="color: #FFFFFF; margin-bottom: 1rem;">📈 Model Comparison</h3>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("sm")
    
    # Create comparison dataframe
    chart_data = pd.DataFrame({
        "Model": ["Logistic Regression", "SVM", "DistilBERT"],
        "Macro F1 Score": [
            logreg_metrics["macro_f1"],
            svm_metrics["macro_f1"],
            bert_metrics["macro_f1"]
        ]
    })
    
    st.bar_chart(chart_data, x="Model", y="Macro F1 Score", color="#8A5CF6")
    
    spacer("md")
    
    # Additional comparison metrics
    comparison_df = pd.DataFrame({
        "Model": ["Logistic Regression", "SVM", "DistilBERT"],
        "Micro F1": [logreg_metrics["micro_f1"], svm_metrics["micro_f1"], bert_metrics["micro_f1"]],
        "Macro F1": [logreg_metrics["macro_f1"], svm_metrics["macro_f1"], bert_metrics["macro_f1"]],
        "Hamming Loss": [logreg_metrics["hamming_loss"], svm_metrics["hamming_loss"], bert_metrics["hamming_loss"]]
    })
    
    st.markdown("""
    <div class="glass-card" style="padding: 24px;">
        <h4 style="color: #FFFFFF; margin-bottom: 1rem;">📊 Detailed Comparison Table</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )
    
    spacer("md")
    
    # Key Insights
    st.markdown("""
    <div class="glass-card" style="padding: 24px;">
        <h4 style="color: #8A5CF6; margin-bottom: 1rem;">💡 Key Insights</h4>
        <ul style="color: #E5E7EB; line-height: 1.8;">
            <li><strong>DistilBERT</strong> significantly outperforms traditional ML models with a <strong>50% Macro F1</strong> score and lowest Hamming Loss.</li>
            <li><strong>SVM</strong> shows moderate improvement over Logistic Regression with better precision on minority classes.</li>
            <li><strong>Logistic Regression</strong> provides a fast baseline but struggles with complex emotional nuances.</li>
            <li>The <strong>Hamming Loss</strong> reduction from 0.095 (LogReg) to 0.033 (BERT) demonstrates BERT's superior multi-label classification capability.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    spacer("lg")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()
