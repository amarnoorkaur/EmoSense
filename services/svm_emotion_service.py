"""
SVM Emotion Detection Service
Loads and uses the trained SVM model for emotion prediction
"""
import pickle
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict


class SVMEmotionService:
    """Service for SVM emotion detection"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.labels = None
        self._load_models()
    
    def _load_models(self):
        """Load the trained SVM model, shared vectorizer, and labels"""
        try:
            models_dir = Path(__file__).parent.parent / "models"
            
            # Suppress warnings
            import warnings
            warnings.filterwarnings('ignore')
            
            print(f"Attempting to load SVM models from: {models_dir}")
            
            # Load labels (shared with LogReg)
            try:
                with open(models_dir / "emotion_labels.pkl", "rb") as f:
                    self.labels = pickle.load(f)
                print(f"✅ SVM Labels loaded: {len(self.labels) if self.labels else 0} emotions")
            except Exception as e:
                try:
                    with open(models_dir / "emotion_labels.pkl", "rb") as f:
                        self.labels = pickle.load(f, encoding='latin1')
                    print(f"✅ SVM Labels loaded with latin1 encoding")
                except Exception as e2:
                    print(f"Failed to load labels for SVM: {e2}")
                    raise
            
            # Load shared TF-IDF vectorizer
            try:
                with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                    self.vectorizer = pickle.load(f)
                print(f"✅ SVM Vectorizer loaded (shared)")
            except Exception as e:
                try:
                    with open(models_dir / "tfidf_vectorizer.pkl", "rb") as f:
                        self.vectorizer = pickle.load(f, encoding='latin1')
                    print(f"✅ SVM Vectorizer loaded with latin1 encoding")
                except Exception as e2:
                    print(f"Failed to load vectorizer for SVM: {e2}")
                    raise
            
            # Load SVM model
            try:
                with open(models_dir / "svm_model.pkl", "rb") as f:
                    self.model = pickle.load(f)
                print(f"✅ SVM Model loaded")
            except Exception as e:
                try:
                    import joblib
                    self.model = joblib.load(models_dir / "svm_model.pkl")
                    print(f"✅ SVM Model loaded with joblib")
                except:
                    try:
                        with open(models_dir / "svm_model.pkl", "rb") as f:
                            self.model = pickle.load(f, encoding='latin1')
                        print(f"✅ SVM Model loaded with latin1 encoding")
                    except Exception as e3:
                        print(f"Failed to load SVM model: {e3}")
                        raise
            
            print(f"✅ All SVM components loaded successfully")
            
        except Exception as e:
            import traceback
            print(f"❌ Error loading SVM model: {e}")
            traceback.print_exc()
            self.model = None
            self.vectorizer = None
            self.labels = None
    
    def predict(self, text: str, threshold: float = 0.3) -> Tuple[List[str], Dict[str, float]]:
        """
        Predict emotions for given text using SVM
        
        Args:
            text: Input text to analyze
            threshold: Minimum probability threshold for emotion detection
            
        Returns:
            Tuple of (detected_emotions, all_probabilities_dict)
        """
        if not self.model or not self.vectorizer or not self.labels:
            return [], {}
        
        try:
            # Vectorize the text using shared TF-IDF
            text_vectorized = self.vectorizer.transform([text])
            
            # Get predictions
            if hasattr(self.model, 'predict_proba'):
                # For SVM with probability=True
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
            
            elif hasattr(self.model, 'decision_function'):
                # For SVM without probability, use decision function
                decision_scores = self.model.decision_function(text_vectorized)
                
                # Handle different decision function outputs
                if len(decision_scores.shape) == 1:
                    scores = decision_scores
                else:
                    scores = decision_scores[0]
                
                # Normalize scores to probabilities using sigmoid
                probabilities = 1 / (1 + np.exp(-scores))
                
                all_probs = {label: float(prob) for label, prob in zip(self.labels, probabilities)}
                detected_emotions = [label for label, prob in all_probs.items() if prob >= threshold]
            
            else:
                # Fallback: just use predict
                predictions = self.model.predict(text_vectorized)
                all_probs = {label: 1.0 if pred else 0.0 for label, pred in zip(self.labels, predictions[0])}
                detected_emotions = [label for label, prob in all_probs.items() if prob >= threshold]
            
            # Sort by probability
            detected_emotions.sort(key=lambda x: all_probs[x], reverse=True)
            
            return detected_emotions, all_probs
            
        except Exception as e:
            print(f"❌ Error in SVM prediction: {e}")
            import traceback
            traceback.print_exc()
            return [], {}
    
    def is_available(self) -> bool:
        """Check if the SVM model is loaded and available"""
        return self.model is not None and self.vectorizer is not None and self.labels is not None
    
    def get_model_info(self) -> Dict[str, str]:
        """Get model information for display"""
        return {
            "type": "Support Vector Machine (TF-IDF)",
            "features": "Term Frequency-Inverse Document Frequency",
            "algorithm": "SVM with RBF/Linear Kernel",
            "training": "Trained on labeled emotion dataset",
            "strengths": "Good generalization, effective in high-dimensional spaces"
        }


# Singleton instance
_svm_service = None


def get_svm_service() -> SVMEmotionService:
    """Get or create the singleton SVM service instance"""
    global _svm_service
    if _svm_service is None:
        _svm_service = SVMEmotionService()
    return _svm_service
