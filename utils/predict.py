# Model loading and prediction functions
# This file handles loading the AI model from HuggingFace Hub

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .labels import EMOTIONS
import os
import streamlit as st
import gc

# Load model from HuggingFace Hub
MODEL_ID = "Amarnoor/emotion-bert-emosense"

# Use Streamlit caching to avoid reloading model on every page
@st.cache_resource(show_spinner="Loading emotion detection model...")
def load_model():
    """Load and cache the BERT emotion model"""
    try:
        print(f"Loading tokenizer from HuggingFace Hub: {MODEL_ID}...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

        print(f"Loading model from HuggingFace Hub: {MODEL_ID}...")
        _model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_ID,
            trust_remote_code=True,
            low_cpu_mem_usage=True  # Memory optimization
        )

        # CPU execution
        _device = torch.device("cpu")
        _model.to(_device)
        _model.eval()
        
        # Free up memory
        gc.collect()

        print(f"✅ Model loaded successfully from HuggingFace Hub on {_device}")

        # Verify labels
        assert len(EMOTIONS) == _model.config.num_labels, (
            f"Mismatch: EMOTIONS has {len(EMOTIONS)} labels but model expects "
            f"{_model.config.num_labels} labels"
        )
        print(f"✅ Validated: Model has {_model.config.num_labels} output labels matching EMOTIONS list")
        
        return _tokenizer, _model, _device, False  # USE_MOCK = False

    except Exception as e:
        print(f"⚠️ Warning: Could not load model from HuggingFace Hub: {str(e)}")
        print(f"⚠️ Falling back to mock predictions for demo purposes")
        gc.collect()
        return None, None, torch.device("cpu"), True  # USE_MOCK = True

# Load model (cached)
tokenizer, model, device, USE_MOCK = load_model()


def predict_emotions(text: str, threshold=0.3):
    """
    Predict emotions from input text.
    
    Args:
        text (str): Input text to analyze
        threshold (float): Probability threshold for emotion detection (default: 0.3)
    
    Returns:
        tuple: (predicted_emotions, probabilities)
    """
    if USE_MOCK:
        # Mock predictions for demo
        import random
        probs = [random.uniform(0.05, 0.9) if i < 5 else random.uniform(0.01, 0.3) 
                 for i in range(len(EMOTIONS))]
        prob_dict = {emotion: float(prob) for emotion, prob in zip(EMOTIONS, probs)}
        
        predicted_emotions = [emotion for emotion, prob in prob_dict.items() if prob >= threshold]
        return predicted_emotions, prob_dict
    
    # Real model prediction
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probabilities = torch.sigmoid(logits)
    probs = probabilities[0].cpu().numpy().tolist()

    prob_dict = {emotion: float(prob) for emotion, prob in zip(EMOTIONS, probs)}
    
    predicted_emotions = [emotion for emotion, prob in prob_dict.items() if prob >= threshold]

    return predicted_emotions, prob_dict
