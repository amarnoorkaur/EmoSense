# Model loading and prediction functions
# This file handles loading the AI model from HuggingFace Hub

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .labels import EMOTIONS

# Load model from HuggingFace Hub
MODEL_ID = "Amarnoor/emotion-bert-emosense"

try:
    print(f"Loading tokenizer from HuggingFace Hub: {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    print(f"Loading model from HuggingFace Hub: {MODEL_ID}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID,
        trust_remote_code=True
    )
    
    # Ensure model runs on CPU (do NOT use CUDA)
    device = torch.device("cpu")
    model.to(device)
    model.eval()
    
    print(f"Model loaded successfully on {device}")
    
    # Validate that number of emotions matches model output labels
    assert len(EMOTIONS) == model.config.num_labels, (
        f"Mismatch: EMOTIONS list has {len(EMOTIONS)} labels but model expects "
        f"{model.config.num_labels} labels"
    )
    print(f"Validated: Model has {model.config.num_labels} output labels matching EMOTIONS list")
    
except Exception as e:
    raise RuntimeError(
        f"Failed to load HuggingFace model from {MODEL_ID}. "
        f"Ensure the model exists on HuggingFace Hub and you have internet connection. Error: {str(e)}"
    )


def predict_emotions(text: str, threshold=0.3):
    """
    Predict emotions from input text using the fine-tuned BERT model.
    
    Args:
        text (str): Input text to analyze
        threshold (float): Probability threshold for emotion detection (default: 0.3)
    
    Returns:
        tuple: (predicted_emotions, probabilities)
            - predicted_emotions: list of emotion labels above threshold
            - probabilities: dict mapping all emotion labels to their probabilities
    """
    # Tokenize input text
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )
    
    # Move inputs to CPU device
    inputs = {key: val.to(device) for key, val in inputs.items()}
    
    # Run model inference (no gradient computation needed)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    # Debug: Print logits shape
    print(f"[DEBUG] Logits shape: {logits.shape}")
    
    # Apply sigmoid activation to convert logits to probabilities
    probabilities = torch.sigmoid(logits)
    
    # Convert to numpy array and then to Python list
    probs = probabilities[0].cpu().numpy().tolist()
    
    # Debug: Print first 5 probabilities
    print(f"[DEBUG] First 5 probabilities: {probs[:5]}")
    print(f"[DEBUG] First 5 emotions: {EMOTIONS[:5]}")
    
    # Create probability dictionary aligned with EMOTIONS list
    prob_dict = {emotion: float(prob) for emotion, prob in zip(EMOTIONS, probs)}
    
    # Apply threshold to get predicted emotions
    predicted_emotions = [
        emotion for emotion, prob in prob_dict.items() if prob >= threshold
    ]
    
    return predicted_emotions, prob_dict
