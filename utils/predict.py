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
        trust_remote_code=True,
        use_safetensors=True,   # <-- IMPORTANT FIX
        revision="main"         # <-- ensures correct branch
    )

    # CPU execution
    device = torch.device("cpu")
    model.to(device)
    model.eval()

    print(f"Model loaded successfully on {device}")

    # Verify labels
    assert len(EMOTIONS) == model.config.num_labels, (
        f"Mismatch: EMOTIONS has {len(EMOTIONS)} labels but model expects "
        f"{model.config.num_labels} labels"
    )
    print(f"Validated: Model has {model.config.num_labels} output labels matching EMOTIONS list")

except Exception as e:
    raise RuntimeError(
        f"Failed to load HuggingFace model from {MODEL_ID}. "
        f"Ensure the model exists on HuggingFace Hub and contains safetensors weights. "
        f"Error: {str(e)}"
    )


def predict_emotions(text: str, threshold=0.3):
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
