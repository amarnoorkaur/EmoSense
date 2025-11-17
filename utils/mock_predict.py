# Mock prediction function for UI testing
# This file simulates emotion prediction without loading actual models

import random
from .labels import EMOTIONS


def predict_emotions(text: str, threshold=0.3):
    """
    Mock emotion prediction for UI testing (no ML models required).
    
    Args:
        text (str): Input text to analyze
        threshold (float): Probability threshold for emotion detection (default: 0.3)
    
    Returns:
        tuple: (predicted_emotions, probabilities)
            - predicted_emotions: list of emotion labels above threshold
            - probabilities: dict mapping all emotion labels to their probabilities
    """
    # Generate fake probabilities for all 28 emotions
    # Make some emotions more likely than others for realistic testing
    fake_probs = []
    for i in range(len(EMOTIONS)):
        if i < 3:
            # First 3 emotions get higher probabilities
            prob = random.uniform(0.4, 0.9)
        elif i < 8:
            # Next 5 emotions get medium probabilities
            prob = random.uniform(0.2, 0.5)
        else:
            # Rest get lower probabilities
            prob = random.uniform(0.05, 0.3)
        fake_probs.append(prob)
    
    # Create probability dictionary
    prob_dict = {emotion: float(prob) for emotion, prob in zip(EMOTIONS, fake_probs)}
    
    # Apply threshold to get predicted emotions
    predicted_emotions = [
        emotion for emotion, prob in prob_dict.items() if prob >= threshold
    ]
    
    return predicted_emotions, prob_dict
