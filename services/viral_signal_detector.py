"""
🔥 Viral Content Signal Detector
Predicts whether comment threads contain linguistic, emotional, and thematic signals
that commonly correlate with viral social media content.
"""
import os
from typing import List, Dict, Any, Optional
from collections import Counter
import re
from openai import OpenAI

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False


# Viral signal keyword sets
NOVELTY_KEYWORDS = [
    "omg", "wow", "insane", "never seen", "obsessed", "crazy", "unreal", 
    "amazing", "iconic", "mind blown", "can't believe", "no way", "shocked"
]

HUMOR_KEYWORDS = [
    "lmao", "lol", "😂", "🤣", "💀", "i'm crying", "broooo", "haha", 
    "hilarious", "dead", "screaming", "stooop", "im weak"
]

ENGAGEMENT_KEYWORDS = [
    "saving", "bookmarking", "sending this", "sharing this", "forwarding this",
    "sending to", "tagging", "showing this to", "need this", "where can i get"
]

TREND_KEYWORDS = [
    "trend", "tiktok", "audio", "sounds like", "everywhere", "viral",
    "fyp", "algorithm", "recommended", "explore page", "trending"
]


class ViralSignalDetector:
    """Detects viral potential in customer comments"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize detector with OpenAI client"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o-mini"
        
        # Load embedding model if available
        self.embeddings_model = None
        if EMBEDDINGS_AVAILABLE:
            try:
                self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"⚠️ Could not load embedding model: {e}")
    
    def analyze_viral_signals(
        self,
        raw_comments: List[str],
        emotions: Dict[str, float],
        emotion_counts: Optional[Dict[str, int]] = None,
        timestamps: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze viral content signals in comments
        
        Args:
            raw_comments: List of actual customer comments
            emotions: Aggregated emotion probabilities
            emotion_counts: Count of each emotion across comments
            timestamps: Optional timestamps for temporal analysis
            
        Returns:
            Dictionary with viral score, level, signals, and explanation
        """
        if not raw_comments or len(raw_comments) == 0:
            return self._empty_result()
        
        total_comments = len(raw_comments)
        
        # A. Emotion-Based Indicators
        positivity_index = self._calculate_positivity_index(emotions)
        negativity_index = self._calculate_negativity_index(emotions)
        
        # B. Novelty / "WOW" Signals
        novelty_score = self._calculate_novelty_score(raw_comments, total_comments)
        
        # C. Humor Signals
        humor_score = self._calculate_humor_score(raw_comments, total_comments)
        
        # D. Engagement Intent
        engagement_score = self._calculate_engagement_score(raw_comments, total_comments)
        
        # E. Trend Alignment
        trend_score = self._calculate_trend_score(raw_comments, total_comments)
        
        # F. Echo Clustering (Repetition)
        repetition_score = self._calculate_repetition_score(raw_comments)
        
        # G. Calculate Viral Score
        viral_score = (
            0.3 * positivity_index +
            0.2 * novelty_score +
            0.15 * humor_score +
            0.15 * engagement_score +
            0.1 * repetition_score +
            0.1 * trend_score
        ) * 100
        
        # H. Classify Viral Level
        viral_level = self._classify_viral_level(viral_score)
        
        # I. Collect all signals
        signals_detected = {
            "positivity_index": round(positivity_index, 3),
            "negativity_index": round(negativity_index, 3),
            "novelty_score": round(novelty_score, 3),
            "humor_score": round(humor_score, 3),
            "engagement_intent_score": round(engagement_score, 3),
            "trend_alignment_score": round(trend_score, 3),
            "repetition_score": round(repetition_score, 3),
            "total_comments": total_comments
        }
        
        # J. Generate AI explanation
        explanation = self._generate_explanation(
            raw_comments, 
            viral_score, 
            viral_level, 
            signals_detected
        )
        
        return {
            "viral_score": round(viral_score, 1),
            "viral_level": viral_level,
            "signals_detected": signals_detected,
            "explanation": explanation,
            "top_viral_comments": self._extract_top_viral_comments(raw_comments, 5)
        }
    
    def _calculate_positivity_index(self, emotions: Dict[str, float]) -> float:
        """Calculate positivity based on positive emotions"""
        positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
        total = sum([emotions.get(e, 0.0) for e in positive_emotions])
        return min(total, 1.0)
    
    def _calculate_negativity_index(self, emotions: Dict[str, float]) -> float:
        """Calculate negativity based on negative emotions"""
        negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance"]
        total = sum([emotions.get(e, 0.0) for e in negative_emotions])
        return min(total, 1.0)
    
    def _calculate_novelty_score(self, comments: List[str], total: int) -> float:
        """Detect novelty/wow signals"""
        novelty_count = 0
        for comment in comments:
            comment_lower = comment.lower()
            if any(keyword in comment_lower for keyword in NOVELTY_KEYWORDS):
                novelty_count += 1
        return novelty_count / total if total > 0 else 0.0
    
    def _calculate_humor_score(self, comments: List[str], total: int) -> float:
        """Detect humor signals"""
        humor_count = 0
        for comment in comments:
            comment_lower = comment.lower()
            # Check text keywords and emojis
            if any(keyword in comment_lower for keyword in HUMOR_KEYWORDS):
                humor_count += 1
            elif any(emoji in comment for emoji in ["😂", "🤣", "💀"]):
                humor_count += 1
        return humor_count / total if total > 0 else 0.0
    
    def _calculate_engagement_score(self, comments: List[str], total: int) -> float:
        """Detect engagement intent signals"""
        engagement_count = 0
        for comment in comments:
            comment_lower = comment.lower()
            if any(keyword in comment_lower for keyword in ENGAGEMENT_KEYWORDS):
                engagement_count += 1
        return engagement_count / total if total > 0 else 0.0
    
    def _calculate_trend_score(self, comments: List[str], total: int) -> float:
        """Detect trend alignment signals"""
        trend_count = 0
        for comment in comments:
            comment_lower = comment.lower()
            if any(keyword in comment_lower for keyword in TREND_KEYWORDS):
                trend_count += 1
        return trend_count / total if total > 0 else 0.0
    
    def _calculate_repetition_score(self, comments: List[str]) -> float:
        """Detect repeated phrases using embeddings or simple matching"""
        if len(comments) < 3:
            return 0.0
        
        if EMBEDDINGS_AVAILABLE and self.embeddings_model:
            try:
                # Use embeddings for semantic similarity
                embeddings = self.embeddings_model.encode(comments)
                similarity_matrix = cosine_similarity(embeddings)
                
                # Count pairs with similarity > 0.85 (excluding self-similarity)
                high_similarity_count = 0
                for i in range(len(similarity_matrix)):
                    for j in range(i + 1, len(similarity_matrix)):
                        if similarity_matrix[i][j] > 0.85:
                            high_similarity_count += 1
                
                # Normalize by possible pairs
                total_pairs = (len(comments) * (len(comments) - 1)) / 2
                return high_similarity_count / total_pairs if total_pairs > 0 else 0.0
            
            except Exception as e:
                print(f"⚠️ Embedding similarity failed: {e}")
                return self._simple_repetition_score(comments)
        else:
            return self._simple_repetition_score(comments)
    
    def _simple_repetition_score(self, comments: List[str]) -> float:
        """Fallback: Simple exact phrase matching"""
        # Normalize and count exact matches
        normalized = [c.lower().strip() for c in comments]
        counter = Counter(normalized)
        
        # Count comments that appear more than once
        repeated = sum(1 for count in counter.values() if count > 1)
        
        return repeated / len(comments) if len(comments) > 0 else 0.0
    
    def _classify_viral_level(self, score: float) -> str:
        """Classify viral potential level"""
        if score < 40:
            return "Low"
        elif score < 65:
            return "Moderate"
        elif score < 85:
            return "High"
        else:
            return "Extremely High"
    
    def _extract_top_viral_comments(self, comments: List[str], n: int = 5) -> List[str]:
        """Extract most viral-signal-rich comments"""
        scored_comments = []
        
        for comment in comments:
            score = 0
            comment_lower = comment.lower()
            
            # Score each comment based on signal keywords
            if any(k in comment_lower for k in NOVELTY_KEYWORDS):
                score += 3
            if any(k in comment_lower for k in HUMOR_KEYWORDS):
                score += 2
            if any(k in comment_lower for k in ENGAGEMENT_KEYWORDS):
                score += 2
            if any(k in comment_lower for k in TREND_KEYWORDS):
                score += 1
            
            scored_comments.append((score, comment))
        
        # Sort by score and return top N
        scored_comments.sort(reverse=True, key=lambda x: x[0])
        return [comment for score, comment in scored_comments[:n] if score > 0]
    
    def _generate_explanation(
        self,
        comments: List[str],
        viral_score: float,
        viral_level: str,
        signals: Dict[str, Any]
    ) -> str:
        """Generate AI explanation of viral potential"""
        if not self.client:
            return self._fallback_explanation(viral_score, viral_level, signals)
        
        try:
            # Build prompt with context
            prompt = self._build_explanation_prompt(comments, viral_score, viral_level, signals)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral content analyst. Explain why content has viral potential by referencing specific comments and signals. Be specific, not generic."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"⚠️ Explanation generation failed: {e}")
            return self._fallback_explanation(viral_score, viral_level, signals)
    
    def _build_explanation_prompt(
        self,
        comments: List[str],
        viral_score: float,
        viral_level: str,
        signals: Dict[str, Any]
    ) -> str:
        """Build prompt for explanation generation"""
        sample_comments = comments[:10]
        comments_text = "\n".join([f'- "{c}"' for c in sample_comments])
        
        return f"""
Viral Score: {viral_score:.1f}/100 ({viral_level})

Detected Signals:
- Positivity Index: {signals['positivity_index']:.2f}
- Novelty Score: {signals['novelty_score']:.2f}
- Humor Score: {signals['humor_score']:.2f}
- Engagement Intent: {signals['engagement_intent_score']:.2f}
- Trend Alignment: {signals['trend_alignment_score']:.2f}
- Repetition: {signals['repetition_score']:.2f}

Sample Comments:
{comments_text}

Explain WHY these comments indicate {viral_level.lower()} viral potential. Reference specific signals and quote actual comments. Be concise (2-3 sentences).
"""
    
    def _fallback_explanation(self, viral_score: float, viral_level: str, signals: Dict) -> str:
        """Fallback explanation when AI unavailable"""
        explanations = []
        
        if signals['humor_score'] > 0.2:
            explanations.append(f"High humor content ({signals['humor_score']:.0%} of comments)")
        
        if signals['novelty_score'] > 0.3:
            explanations.append(f"Strong novelty signals ({signals['novelty_score']:.0%})")
        
        if signals['engagement_intent_score'] > 0.15:
            explanations.append(f"Active sharing intent detected ({signals['engagement_intent_score']:.0%})")
        
        if signals['positivity_index'] > 0.6:
            explanations.append(f"Highly positive emotional tone ({signals['positivity_index']:.0%})")
        
        if not explanations:
            return f"Viral score of {viral_score:.1f} indicates {viral_level.lower()} viral potential based on linguistic and emotional patterns."
        
        return f"{viral_level} viral potential due to: " + ", ".join(explanations) + "."
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result when no comments"""
        return {
            "viral_score": 0.0,
            "viral_level": "Low",
            "signals_detected": {},
            "explanation": "No comments to analyze.",
            "top_viral_comments": []
        }


# Cached instance getter
_detector_instance = None

def get_viral_detector() -> ViralSignalDetector:
    """Get cached viral signal detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = ViralSignalDetector()
    return _detector_instance
