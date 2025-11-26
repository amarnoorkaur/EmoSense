"""
Logistic Regression Emotion Detection Service
Loads and uses the trained LogReg model for emotion prediction
"""
import pickle
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict

class LogRegEmotionService:
    """Service for Logistic Regression emotion detection"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.labels = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained model, vectorizer, and labels"""
        try:
            models_dir = Path(__file__).parent.parent / "models"
            
            # Load model
            with open(models_dir / "emotion_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            
            # Load vectorizer
            with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)
            
            # Load labels
            with open(models_dir / "emotion_labels.pkl", "rb") as f:
                self.labels = pickle.load(f)
            
            print(f"✅ LogReg model loaded successfully with {len(self.labels)} emotion labels")
            
        except Exception as e:
            print(f"❌ Error loading LogReg model: {e}")
            self.model = None
            self.vectorizer = None
            self.labels = None
    
    def predict(self, text: str, threshold: float = 0.3) -> Tuple[List[str], Dict[str, float]]:
        """
        Predict emotions for given text
        
        Args:
            text: Input text to analyze
            threshold: Minimum probability threshold for emotion detection
            
        Returns:
            Tuple of (detected_emotions, all_probabilities)
        """
        if not self.model or not self.vectorizer or not self.labels:
            return [], {}
        
        try:
            # Vectorize the text
            text_vectorized = self.vectorizer.transform([text])
            
            # Get predictions
            if hasattr(self.model, 'predict_proba'):
                # For multi-label classification
                probabilities = self.model.predict_proba(text_vectorized)
                
                # Handle different probability formats
                if isinstance(probabilities, list):
                    # Multiple binary classifiers (one-vs-rest)
                    all_probs = {}
                    detected_emotions = []
                    
                    for idx, label in enumerate(self.labels):
                        prob = probabilities[idx][0][1]  # Probability of positive class
                        all_probs[label] = float(prob)
                        if prob >= threshold:
                            detected_emotions.append(label)
                else:
                    # Single multi-class classifier
                    all_probs = {label: float(prob) for label, prob in zip(self.labels, probabilities[0])}
                    detected_emotions = [label for label, prob in all_probs.items() if prob >= threshold]
            else:
                # For models without predict_proba, use decision function
                decision_scores = self.model.decision_function(text_vectorized)
                
                # Normalize scores to probabilities (sigmoid)
                probabilities = 1 / (1 + np.exp(-decision_scores))
                
                all_probs = {label: float(prob) for label, prob in zip(self.labels, probabilities[0])}
                detected_emotions = [label for label, prob in all_probs.items() if prob >= threshold]
            
            # Sort by probability
            detected_emotions.sort(key=lambda x: all_probs[x], reverse=True)
            
            return detected_emotions, all_probs
            
        except Exception as e:
            print(f"❌ Error in LogReg prediction: {e}")
            return [], {}
    
    def is_available(self) -> bool:
        """Check if the model is loaded and available"""
        return self.model is not None and self.vectorizer is not None and self.labels is not None


# Singleton instance
_logreg_service = None

def get_logreg_service() -> LogRegEmotionService:
    """Get or create the singleton LogReg service instance"""
    global _logreg_service
    if _logreg_service is None:
        _logreg_service = LogRegEmotionService()
    return _logreg_service
