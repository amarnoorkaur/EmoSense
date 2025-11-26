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
            
            # Suppress warnings
            import warnings
            warnings.filterwarnings('ignore')
            
            # Try different loading strategies
            print(f"Attempting to load LogReg models from: {models_dir}")
            
            # Strategy 1: Standard pickle load
            try:
                with open(models_dir / "emotion_labels.pkl", "rb") as f:
                    self.labels = pickle.load(f)
                print(f"✅ Labels loaded: {len(self.labels) if self.labels else 0} emotions")
            except Exception as e:
                print(f"Strategy 1 failed for labels: {e}")
                # Strategy 2: Try with encoding
                try:
                    with open(models_dir / "emotion_labels.pkl", "rb") as f:
                        self.labels = pickle.load(f, encoding='latin1')
                    print(f"✅ Labels loaded with latin1 encoding")
                except Exception as e2:
                    print(f"Strategy 2 failed for labels: {e2}")
                    raise
            
            # Load vectorizer
            try:
                with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                    self.vectorizer = pickle.load(f)
                print(f"✅ Vectorizer loaded")
            except Exception as e:
                try:
                    with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                        self.vectorizer = pickle.load(f, encoding='latin1')
                    print(f"✅ Vectorizer loaded with latin1 encoding")
                except Exception as e2:
                    print(f"Failed to load vectorizer: {e2}")
                    raise
            
            # Load model
            try:
                with open(models_dir / "emotion_model.pkl", "rb") as f:
                    self.model = pickle.load(f)
                print(f"✅ Model loaded")
            except Exception as e:
                try:
                    with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                        import joblib
                        self.model = joblib.load(f)
                    print(f"✅ Model loaded with joblib")
                except:
                    try:
                        with open(models_dir / "emotion_model.pkl", "rb") as f:
                            self.model = pickle.load(f, encoding='latin1')
                        print(f"✅ Model loaded with latin1 encoding")
                    except Exception as e3:
                        print(f"Failed to load model: {e3}")
                        raise
            
            print(f"✅ All LogReg components loaded successfully")
            
        except Exception as e:
            import traceback
            print(f"❌ Error loading LogReg model: {e}")
            print(f"Full error details:")
            traceback.print_exc()
            print(f"\n⚠️ Please ensure the pickle files were saved with:")
            print(f"   - pickle.dump() or joblib.dump()")
            print(f"   - Compatible Python version (3.8+)")
            print(f"   - Compatible scikit-learn version")
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
            Tuple of (detected_emotions, all_probabilities_dict)
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
    
    def get_model_info(self) -> Dict[str, str]:
        """Get model information for display"""
        return {
            "type": "Logistic Regression (TF-IDF)",
            "features": "Term Frequency-Inverse Document Frequency",
            "algorithm": "One-vs-Rest Multi-label Classification",
            "training": "Trained on labeled emotion dataset",
            "strengths": "Fast inference, interpretable, lightweight",
            "accuracy_note": "Accuracy is calculated as exact match ratio (all emotions must match)"
        }


# Singleton instance
_logreg_service = None

def get_logreg_service() -> LogRegEmotionService:
    """Get or create the singleton LogReg service instance"""
    global _logreg_service
    if _logreg_service is None:
        _logreg_service = LogRegEmotionService()
    return _logreg_service
