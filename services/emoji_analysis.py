"""
Emoji Emotion Analysis Service
Maps emojis to emotions and boosts confidence when signals align
"""
import re
from typing import Dict, List, Tuple
from collections import defaultdict


# Comprehensive emoji-to-emotion mapping based on Unicode Emoji standard
# and emotion research (Novak et al., 2015; AI4D EmoTweet research)
EMOJI_EMOTION_MAP = {
    # JOY / HAPPINESS
    "😀": "joy", "😁": "joy", "😂": "joy", "🤣": "joy", "😃": "joy",
    "😄": "joy", "😆": "joy", "😊": "joy", "☺️": "joy", "🙂": "joy",
    "🤗": "joy", "🥳": "joy", "🎉": "joy", "🎊": "joy", "✨": "joy",
    "⭐": "joy", "🌟": "joy", "💫": "joy", "🎈": "joy",
    
    # LOVE / AFFECTION
    "😍": "love", "🥰": "love", "😘": "love", "😗": "love", "😙": "love",
    "😚": "love", "❤️": "love", "🧡": "love", "💛": "love", "💚": "love",
    "💙": "love", "💜": "love", "🤎": "love", "🖤": "love", "🤍": "love",
    "💕": "love", "💞": "love", "💓": "love", "💗": "love", "💖": "love",
    "💘": "love", "💝": "love", "💌": "love", "💋": "love", "👄": "love",
    "🫶": "love", "❣️": "love", "💑": "love", "💏": "love",
    
    # GRATITUDE / APPRECIATION
    "🙏": "gratitude", "🤲": "gratitude", "👏": "gratitude", "🙌": "gratitude",
    
    # ADMIRATION / IMPRESSED
    "😮": "admiration", "😯": "admiration", "😲": "admiration", "🤩": "admiration",
    "🌈": "admiration", "🔥": "admiration", "💯": "admiration", "👌": "admiration",
    "👍": "admiration", "🏆": "admiration", "🥇": "admiration", "🎖️": "admiration",
    
    # EXCITEMENT / ENTHUSIASM
    "🤩": "excitement", "😃": "excitement", "🥳": "excitement", "🎊": "excitement",
    "🎉": "excitement", "🎈": "excitement", "🚀": "excitement", "💥": "excitement",
    "⚡": "excitement", "🔥": "excitement",
    
    # OPTIMISM / HOPE
    "🤞": "optimism", "🌅": "optimism", "🌄": "optimism", "☀️": "optimism",
    "🌻": "optimism", "🌺": "optimism", "🌸": "optimism", "💪": "optimism",
    "✊": "optimism", "🎯": "optimism",
    
    # PRIDE / ACHIEVEMENT
    "😎": "pride", "🏆": "pride", "🥇": "pride", "🥈": "pride", "🥉": "pride",
    "🎖️": "pride", "🏅": "pride", "👑": "pride", "💪": "pride",
    
    # RELIEF / RELAXED
    "😌": "relief", "😇": "relief", "🙏": "relief", "😮‍💨": "relief",
    
    # ANGER / RAGE
    "😠": "anger", "😡": "anger", "🤬": "anger", "👿": "anger", "😾": "anger",
    "💢": "anger", "🔥": "anger", "💥": "anger", "⚡": "anger",
    
    # SADNESS / DEPRESSION
    "😢": "sadness", "😭": "sadness", "😿": "sadness", "😞": "sadness",
    "😔": "sadness", "😟": "sadness", "😥": "sadness", "😰": "sadness",
    "😓": "sadness", "🥺": "sadness", "💔": "sadness", "🌧️": "sadness",
    
    # FEAR / ANXIETY
    "😨": "fear", "😱": "fear", "😰": "fear", "😧": "fear", "😦": "fear",
    "😵": "fear", "🙀": "fear", "💀": "fear", "☠️": "fear",
    
    # DISAPPOINTMENT / LETDOWN
    "😞": "disappointment", "😔": "disappointment", "😕": "disappointment",
    "🙁": "disappointment", "☹️": "disappointment", "😣": "disappointment",
    "😖": "disappointment", "😫": "disappointment", "💔": "disappointment",
    
    # DISGUST / REVULSION
    "🤢": "disgust", "🤮": "disgust", "😷": "disgust", "🤧": "disgust",
    "😬": "disgust", "😖": "disgust", "🤒": "disgust",
    
    # ANNOYANCE / IRRITATION
    "😒": "annoyance", "🙄": "annoyance", "😤": "annoyance", "😑": "annoyance",
    "😐": "annoyance", "💢": "annoyance",
    
    # DISAPPROVAL / DISLIKE
    "👎": "disapproval", "❌": "disapproval", "🚫": "disapproval",
    "⛔": "disapproval", "🙅": "disapproval", "🙅‍♂️": "disapproval",
    "🙅‍♀️": "disapproval", "❎": "disapproval",
    
    # EMBARRASSMENT / SHAME
    "😳": "embarrassment", "🙈": "embarrassment", "😬": "embarrassment",
    "🤦": "embarrassment", "🤦‍♂️": "embarrassment", "🤦‍♀️": "embarrassment",
    
    # CONFUSION / PUZZLED
    "🤔": "confusion", "😕": "confusion", "😵": "confusion", "😵‍💫": "confusion",
    "🤷": "confusion", "🤷‍♂️": "confusion", "🤷‍♀️": "confusion", "❓": "confusion",
    
    # SURPRISE / SHOCK
    "😮": "surprise", "😯": "surprise", "😲": "surprise", "🤯": "surprise",
    "😱": "surprise", "💥": "surprise", "⚡": "surprise",
    
    # CURIOSITY / INTEREST
    "🤔": "curiosity", "🧐": "curiosity", "👀": "curiosity", "🔍": "curiosity",
    "🔎": "curiosity", "❓": "curiosity", "❔": "curiosity",
    
    # NERVOUSNESS / WORRY
    "😬": "nervousness", "😰": "nervousness", "😅": "nervousness",
    "😓": "nervousness", "🥵": "nervousness",
    
    # APPROVAL / AGREEMENT
    "👍": "approval", "👌": "approval", "✅": "approval", "☑️": "approval",
    "✔️": "approval", "💯": "approval", "🙆": "approval", "🙆‍♂️": "approval",
    "🙆‍♀️": "approval", "👏": "approval",
    
    # CARING / SUPPORTIVE
    "🤗": "caring", "🫂": "caring", "💝": "caring", "💐": "caring",
    "🌹": "caring", "🌷": "caring", "🎁": "caring",
    
    # DESIRE / WANT
    "😍": "desire", "🤤": "desire", "😋": "desire", "🤩": "desire",
    
    # REALIZATION / UNDERSTANDING
    "💡": "realization", "🤓": "realization", "🧠": "realization",
    
    # GRIEF / MOURNING
    "😢": "grief", "😭": "grief", "💐": "grief", "🕊️": "grief",
    "🖤": "grief", "⚰️": "grief",
    
    # REMORSE / GUILT
    "😔": "remorse", "😞": "remorse", "🙏": "remorse",
    
    # NEUTRAL / AMBIGUOUS
    "😐": "neutral", "😶": "neutral", "🤷": "neutral", "➖": "neutral",
}


# Emoji regex pattern (matches most Unicode emoji)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
    "\u200d"                 # zero width joiner
    "\u2640-\u2642"          # gender symbols
    "\uFE0F"                 # variation selector
    "]+", 
    flags=re.UNICODE
)


def extract_emojis(text: str) -> List[str]:
    """
    Extract all emojis from text
    
    Args:
        text: Input text with potential emojis
        
    Returns:
        List of emoji characters found
    """
    if not text:
        return []
    
    emojis = EMOJI_PATTERN.findall(text)
    return emojis


def analyze_emoji_emotions(text: str) -> Dict[str, float]:
    """
    Analyze emotional signals from emojis in text
    
    Args:
        text: Input text with potential emojis
        
    Returns:
        Dictionary of emotion scores based on emoji presence
    """
    emojis = extract_emojis(text)
    
    if not emojis:
        return {}
    
    # Count emotions indicated by emojis
    emotion_counts = defaultdict(int)
    total_emojis = 0
    
    for emoji in emojis:
        emotion = EMOJI_EMOTION_MAP.get(emoji)
        if emotion:
            emotion_counts[emotion] += 1
            total_emojis += 1
    
    if total_emojis == 0:
        return {}
    
    # Convert counts to probabilities
    emoji_emotions = {
        emotion: count / total_emojis 
        for emotion, count in emotion_counts.items()
    }
    
    return emoji_emotions


def boost_with_emoji_signals(bert_emotions: Dict[str, float], 
                             emoji_emotions: Dict[str, float],
                             boost_factor: float = 0.15) -> Dict[str, float]:
    """
    Boost BERT emotion predictions when emoji signals align
    
    Args:
        bert_emotions: Original BERT emotion probabilities
        emoji_emotions: Emotion signals from emojis
        boost_factor: How much to boost aligned emotions (0.15 = 15% boost)
        
    Returns:
        Adjusted emotion probabilities
    """
    if not emoji_emotions:
        return bert_emotions
    
    boosted_emotions = bert_emotions.copy()
    
    for emotion, emoji_score in emoji_emotions.items():
        if emotion in boosted_emotions:
            # Boost if emoji confirms BERT prediction
            original_score = boosted_emotions[emotion]
            boost_amount = emoji_score * boost_factor
            boosted_emotions[emotion] = min(original_score + boost_amount, 1.0)
    
    return boosted_emotions


def get_emoji_summary(text: str) -> Dict[str, any]:
    """
    Get comprehensive emoji analysis summary
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with emoji analysis results
    """
    emojis = extract_emojis(text)
    emoji_emotions = analyze_emoji_emotions(text)
    
    # Get most common emotion from emojis
    dominant_emoji_emotion = None
    if emoji_emotions:
        dominant_emoji_emotion = max(emoji_emotions.items(), key=lambda x: x[1])
    
    return {
        "emojis_found": emojis,
        "emoji_count": len(emojis),
        "emoji_emotions": emoji_emotions,
        "dominant_emoji_emotion": dominant_emoji_emotion[0] if dominant_emoji_emotion else None,
        "emoji_confidence": dominant_emoji_emotion[1] if dominant_emoji_emotion else 0.0
    }


def format_emoji_insights(emoji_summary: Dict[str, any]) -> str:
    """
    Format emoji analysis into human-readable insight
    
    Args:
        emoji_summary: Results from get_emoji_summary()
        
    Returns:
        Formatted string describing emoji emotional signals
    """
    if emoji_summary["emoji_count"] == 0:
        return ""
    
    emojis_str = " ".join(emoji_summary["emojis_found"])
    
    if emoji_summary["dominant_emoji_emotion"]:
        emotion = emoji_summary["dominant_emoji_emotion"]
        confidence = emoji_summary["emoji_confidence"]
        
        return (f"Emojis detected ({emojis_str}) strongly indicate **{emotion}** "
                f"({confidence:.0%} of emoji signals)")
    
    return f"Emojis detected ({emojis_str})"
