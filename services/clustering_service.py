"""
Pain Point Clustering Service
Automatically clusters customer comments into meaningful business themes using embeddings + clustering
"""
from typing import List, Dict, Any, Optional
import numpy as np
from collections import Counter
import re

# Sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# Clustering algorithms
try:
    from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import hdbscan
    HDBSCAN_AVAILABLE = True
except ImportError:
    HDBSCAN_AVAILABLE = False


def extract_cluster_keywords(comments: List[str], top_n: int = 5) -> List[str]:
    """
    Extract top keywords from a cluster of comments using TF-IDF
    
    Args:
        comments: List of comments in the cluster
        top_n: Number of top keywords to extract
        
    Returns:
        List of top keywords
    """
    if not comments or not SKLEARN_AVAILABLE:
        return []
    
    try:
        # Remove stopwords and extract keywords
        vectorizer = TfidfVectorizer(
            max_features=50,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform(comments)
        feature_names = vectorizer.get_feature_names_out()
        
        # Sum TF-IDF scores across all comments
        scores = np.asarray(tfidf_matrix.sum(axis=0)).flatten()
        
        # Get top keywords
        top_indices = scores.argsort()[-top_n:][::-1]
        keywords = [feature_names[i] for i in top_indices]
        
        return keywords
    
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []


def compute_cluster_sentiment(emotions_list: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Compute sentiment summary for a cluster
    
    Args:
        emotions_list: List of emotion dictionaries for comments in cluster
        
    Returns:
        Sentiment summary dictionary
    """
    if not emotions_list:
        return {"positive": 0, "negative": 0, "neutral": 0, "status": "Unknown"}
    
    positive_emotions = ["joy", "love", "gratitude", "admiration", "excitement", "optimism", "pride", "relief"]
    negative_emotions = ["anger", "sadness", "fear", "disappointment", "disgust", "annoyance", "disapproval", "embarrassment", "confusion", "frustration"]
    
    total_positive = 0
    total_negative = 0
    
    for emotions in emotions_list:
        pos_score = sum([emotions.get(e, 0) for e in positive_emotions])
        neg_score = sum([emotions.get(e, 0) for e in negative_emotions])
        total_positive += pos_score
        total_negative += neg_score
    
    # Normalize
    total = total_positive + total_negative
    if total > 0:
        positive_pct = total_positive / total
        negative_pct = total_negative / total
    else:
        positive_pct = 0
        negative_pct = 0
    
    neutral_pct = max(0, 1.0 - positive_pct - negative_pct)
    
    if positive_pct > negative_pct:
        status = "Positive"
    elif negative_pct > positive_pct:
        status = "Negative"
    else:
        status = "Neutral"
    
    return {
        "positive": positive_pct,
        "negative": negative_pct,
        "neutral": neutral_pct,
        "status": status
    }


def aggregate_cluster_emotions(emotions_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Aggregate emotions across a cluster
    
    Args:
        emotions_list: List of emotion dictionaries
        
    Returns:
        Aggregated emotion dictionary
    """
    if not emotions_list:
        return {}
    
    # Sum all emotions
    emotion_sums = {}
    for emotions in emotions_list:
        for emotion, score in emotions.items():
            emotion_sums[emotion] = emotion_sums.get(emotion, 0) + score
    
    # Average
    num_comments = len(emotions_list)
    emotion_averages = {e: s / num_comments for e, s in emotion_sums.items()}
    
    # Return top 5
    top_emotions = sorted(emotion_averages.items(), key=lambda x: x[1], reverse=True)[:5]
    return dict(top_emotions)


def cluster_comments(
    comments: List[str],
    emotions_per_comment: Optional[List[Dict[str, float]]] = None,
    min_cluster_size: int = 2,
    max_clusters: int = 8
) -> Dict[str, Any]:
    """
    Cluster customer comments into meaningful business themes
    
    Args:
        comments: List of customer comments
        emotions_per_comment: Optional list of emotion dicts for each comment
        min_cluster_size: Minimum size for a cluster
        max_clusters: Maximum number of clusters
        
    Returns:
        Dictionary with cluster information
    """
    if not comments or len(comments) < 2:
        return {
            "clusters": [],
            "error": "Not enough comments to cluster (minimum 2 required)"
        }
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE or not SKLEARN_AVAILABLE:
        return {
            "clusters": [],
            "error": "Required libraries not available (sentence-transformers, scikit-learn)"
        }
    
    try:
        # 1. Compute embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(comments)
        
        # 2. Determine number of clusters
        n_comments = len(comments)
        
        if n_comments < 10:
            # Small dataset: use agglomerative clustering
            n_clusters = min(3, max(2, n_comments // 3))
            clusterer = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='ward')
            labels = clusterer.fit_predict(embeddings)
        
        elif n_comments < 30:
            # Medium dataset: use KMeans
            n_clusters = min(5, max(2, n_comments // 5))
            clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            labels = clusterer.fit_predict(embeddings)
        
        else:
            # Large dataset: try HDBSCAN first, fallback to KMeans
            if HDBSCAN_AVAILABLE:
                clusterer = hdbscan.HDBSCAN(
                    min_cluster_size=max(min_cluster_size, n_comments // 10),
                    min_samples=2,
                    metric='euclidean'
                )
                labels = clusterer.fit_predict(embeddings)
                
                # If HDBSCAN produces too many noise points, fallback to KMeans
                if (labels == -1).sum() > n_comments * 0.3:  # More than 30% noise
                    n_clusters = min(max_clusters, max(3, n_comments // 8))
                    clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    labels = clusterer.fit_predict(embeddings)
            else:
                n_clusters = min(max_clusters, max(3, n_comments // 8))
                clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                labels = clusterer.fit_predict(embeddings)
        
        # 3. Build cluster information
        unique_labels = set(labels)
        if -1 in unique_labels:
            unique_labels.remove(-1)  # Remove noise cluster
        
        clusters = []
        
        for cluster_id in sorted(unique_labels):
            # Get comments in this cluster
            cluster_indices = [i for i, label in enumerate(labels) if label == cluster_id]
            cluster_comments = [comments[i] for i in cluster_indices]
            
            # Skip if cluster is too small
            if len(cluster_comments) < min_cluster_size:
                continue
            
            # Extract keywords
            keywords = extract_cluster_keywords(cluster_comments, top_n=5)
            
            # Get emotions for this cluster
            cluster_emotions_list = []
            if emotions_per_comment:
                cluster_emotions_list = [emotions_per_comment[i] for i in cluster_indices if i < len(emotions_per_comment)]
            
            # Compute emotion distribution
            emotion_distribution = aggregate_cluster_emotions(cluster_emotions_list) if cluster_emotions_list else {}
            
            # Compute sentiment
            sentiment_summary = compute_cluster_sentiment(cluster_emotions_list) if cluster_emotions_list else {
                "positive": 0, "negative": 0, "neutral": 0, "status": "Unknown"
            }
            
            # Determine cluster theme name based on keywords and sentiment
            theme_name = generate_theme_name(keywords, sentiment_summary['status'])
            
            clusters.append({
                "cluster_id": int(cluster_id),
                "theme_name": theme_name,
                "theme_keywords": keywords,
                "comment_examples": cluster_comments[:5],  # First 5 examples
                "emotion_distribution": emotion_distribution,
                "sentiment_summary": sentiment_summary,
                "size": len(cluster_comments),
                "percentage": (len(cluster_comments) / n_comments) * 100
            })
        
        # Sort by size (largest first)
        clusters.sort(key=lambda x: x['size'], reverse=True)
        
        return {
            "clusters": clusters,
            "total_comments": n_comments,
            "num_clusters": len(clusters),
            "clustering_method": type(clusterer).__name__
        }
    
    except Exception as e:
        return {
            "clusters": [],
            "error": f"Clustering failed: {str(e)}"
        }


def generate_theme_name(keywords: List[str], sentiment: str) -> str:
    """
    Generate a human-readable theme name based on keywords and sentiment
    
    Args:
        keywords: List of keywords
        sentiment: Sentiment status
        
    Returns:
        Theme name string
    """
    if not keywords:
        return f"{sentiment} Feedback"
    
    # Common patterns
    if any(word in keywords for word in ['price', 'expensive', 'cost', 'pricing', 'cheap', 'money']):
        return "Pricing Concerns" if sentiment == "Negative" else "Pricing Feedback"
    
    elif any(word in keywords for word in ['feature', 'add', 'want', 'need', 'request', 'wish']):
        return "Feature Requests"
    
    elif any(word in keywords for word in ['bug', 'crash', 'error', 'broken', 'not working', 'issue', 'problem']):
        return "Technical Issues"
    
    elif any(word in keywords for word in ['ui', 'ux', 'design', 'interface', 'confusing', 'hard', 'difficult']):
        return "UX/Design Feedback"
    
    elif any(word in keywords for word in ['ship', 'delivery', 'shipping', 'arrived', 'delay']):
        return "Shipping & Delivery"
    
    elif any(word in keywords for word in ['support', 'help', 'customer service', 'response', 'reply']):
        return "Customer Support"
    
    elif any(word in keywords for word in ['quality', 'product', 'material', 'build']):
        return "Product Quality"
    
    elif any(word in keywords for word in ['love', 'amazing', 'great', 'excellent', 'best', 'perfect']):
        return "Customer Praise"
    
    elif any(word in keywords for word in ['dark mode', 'theme', 'customization', 'customize']):
        return "Customization Requests"
    
    else:
        # Use top keyword
        return f"{keywords[0].capitalize()} Discussion"
