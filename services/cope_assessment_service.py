"""
Brief COPE Assessment Service for EmoSense
Implements the full 28-item Brief COPE questionnaire for emotional coping profile assessment.

Reference: Carver, C. S. (1997). You want to measure coping but your protocol's too long: 
Consider the Brief COPE. International Journal of Behavioral Medicine, 4, 92-100.

This is used for educational/research purposes (UFV university project).
"""

from typing import Dict, List, Tuple, Optional


# ============================================================
# PART 1: FULL 28-ITEM BRIEF COPE QUESTIONNAIRE
# ============================================================

COPE_QUESTIONS: List[Dict] = [
    # Self-Distraction (Items 1, 19 in original - we use sequential numbering)
    {
        "id": "q1",
        "text": "I've been turning to work or other activities to take my mind off things.",
        "subscale": "self_distraction"
    },
    {
        "id": "q2",
        "text": "I've been doing things to think about it less, such as going to movies, watching TV, reading, daydreaming, sleeping, or shopping.",
        "subscale": "self_distraction"
    },
    
    # Active Coping (Items 2, 7 in original)
    {
        "id": "q3",
        "text": "I've been concentrating my efforts on doing something about the situation I'm in.",
        "subscale": "active_coping"
    },
    {
        "id": "q4",
        "text": "I've been taking action to try to make the situation better.",
        "subscale": "active_coping"
    },
    
    # Denial (Items 3, 8 in original)
    {
        "id": "q5",
        "text": "I've been saying to myself 'this isn't real.'",
        "subscale": "denial"
    },
    {
        "id": "q6",
        "text": "I've been refusing to believe that it has happened.",
        "subscale": "denial"
    },
    
    # Substance Use (Items 4, 11 in original)
    {
        "id": "q7",
        "text": "I've been using alcohol or other drugs to make myself feel better.",
        "subscale": "substance_use"
    },
    {
        "id": "q8",
        "text": "I've been using alcohol or other drugs to help me get through it.",
        "subscale": "substance_use"
    },
    
    # Emotional Support (Items 5, 15 in original)
    {
        "id": "q9",
        "text": "I've been getting emotional support from others.",
        "subscale": "emotional_support"
    },
    {
        "id": "q10",
        "text": "I've been getting comfort and understanding from someone.",
        "subscale": "emotional_support"
    },
    
    # Instrumental Support (Items 10, 23 in original)
    {
        "id": "q11",
        "text": "I've been getting help and advice from other people.",
        "subscale": "instrumental_support"
    },
    {
        "id": "q12",
        "text": "I've been trying to get advice or help from other people about what to do.",
        "subscale": "instrumental_support"
    },
    
    # Behavioral Disengagement (Items 6, 16 in original)
    {
        "id": "q13",
        "text": "I've been giving up trying to deal with it.",
        "subscale": "behavioral_disengagement"
    },
    {
        "id": "q14",
        "text": "I've been giving up the attempt to cope.",
        "subscale": "behavioral_disengagement"
    },
    
    # Venting (Items 9, 21 in original)
    {
        "id": "q15",
        "text": "I've been expressing my negative feelings.",
        "subscale": "venting"
    },
    {
        "id": "q16",
        "text": "I've been saying things to let my unpleasant feelings escape.",
        "subscale": "venting"
    },
    
    # Positive Reframing (Items 12, 17 in original)
    {
        "id": "q17",
        "text": "I've been trying to see it in a different light, to make it seem more positive.",
        "subscale": "positive_reframing"
    },
    {
        "id": "q18",
        "text": "I've been looking for something good in what is happening.",
        "subscale": "positive_reframing"
    },
    
    # Planning (Items 14, 25 in original)
    {
        "id": "q19",
        "text": "I've been trying to come up with a strategy about what to do.",
        "subscale": "planning"
    },
    {
        "id": "q20",
        "text": "I've been thinking hard about what steps to take.",
        "subscale": "planning"
    },
    
    # Humor (Items 18, 28 in original)
    {
        "id": "q21",
        "text": "I've been making jokes about it.",
        "subscale": "humor"
    },
    {
        "id": "q22",
        "text": "I've been making fun of the situation.",
        "subscale": "humor"
    },
    
    # Acceptance (Items 20, 24 in original)
    {
        "id": "q23",
        "text": "I've been accepting the reality of the fact that it has happened.",
        "subscale": "acceptance"
    },
    {
        "id": "q24",
        "text": "I've been learning to live with it.",
        "subscale": "acceptance"
    },
    
    # Religion (Items 22, 27 in original)
    {
        "id": "q25",
        "text": "I've been trying to find comfort in my religion or spiritual beliefs.",
        "subscale": "religion"
    },
    {
        "id": "q26",
        "text": "I've been praying or meditating.",
        "subscale": "religion"
    },
    
    # Self-Blame (Items 13, 26 in original)
    {
        "id": "q27",
        "text": "I've been criticizing myself.",
        "subscale": "self_blame"
    },
    {
        "id": "q28",
        "text": "I've been blaming myself for things that happened.",
        "subscale": "self_blame"
    },
]


# Response options (1-4 Likert scale)
RESPONSE_OPTIONS: Dict[int, str] = {
    1: "I haven't been doing this at all",
    2: "I've been doing this a little bit",
    3: "I've been doing this a medium amount",
    4: "I've been doing this a lot"
}


# Subscale metadata for display
SUBSCALE_INFO: Dict[str, Dict] = {
    "self_distraction": {
        "name": "Self-Distraction",
        "description": "Using activities to take your mind off stressors",
        "emoji": "🎮"
    },
    "active_coping": {
        "name": "Active Coping",
        "description": "Taking direct action to address the problem",
        "emoji": "💪"
    },
    "denial": {
        "name": "Denial",
        "description": "Refusing to accept the reality of the situation",
        "emoji": "🙈"
    },
    "substance_use": {
        "name": "Substance Use",
        "description": "Using substances to cope with stress",
        "emoji": "⚠️"
    },
    "emotional_support": {
        "name": "Emotional Support",
        "description": "Seeking emotional comfort from others",
        "emoji": "🤗"
    },
    "instrumental_support": {
        "name": "Instrumental Support",
        "description": "Seeking advice and practical help from others",
        "emoji": "🤝"
    },
    "behavioral_disengagement": {
        "name": "Behavioral Disengagement",
        "description": "Giving up efforts to cope",
        "emoji": "😔"
    },
    "venting": {
        "name": "Venting",
        "description": "Expressing negative feelings",
        "emoji": "😤"
    },
    "positive_reframing": {
        "name": "Positive Reframing",
        "description": "Finding the silver lining in difficult situations",
        "emoji": "🌈"
    },
    "planning": {
        "name": "Planning",
        "description": "Developing strategies to handle problems",
        "emoji": "📋"
    },
    "humor": {
        "name": "Humor",
        "description": "Using humor to cope with stress",
        "emoji": "😄"
    },
    "acceptance": {
        "name": "Acceptance",
        "description": "Accepting the reality of the situation",
        "emoji": "🧘"
    },
    "religion": {
        "name": "Religion/Spirituality",
        "description": "Finding comfort through faith or spirituality",
        "emoji": "🙏"
    },
    "self_blame": {
        "name": "Self-Blame",
        "description": "Criticizing oneself for the situation",
        "emoji": "😞"
    }
}


# EmoSense Persona definitions
PERSONA_INFO: Dict[str, Dict] = {
    "Direct Professional": {
        "emoji": "👔",
        "description": "You prefer practical, solution-focused support. EmoSense will provide clear strategies and actionable advice.",
        "traits": ["Problem-solver", "Action-oriented", "Seeks practical help"],
        "chat_style": "Direct, solution-focused, provides actionable steps"
    },
    "Gentle Sensitive": {
        "emoji": "💜",
        "description": "You value emotional validation and gentle support. EmoSense will prioritize empathy and understanding.",
        "traits": ["Values emotional connection", "Seeks comfort", "Appreciates gentleness"],
        "chat_style": "Warm, validating, emotionally supportive"
    },
    "Reflective Companion": {
        "emoji": "🌟",
        "description": "You appreciate thoughtful perspective and finding meaning. EmoSense will help you explore and reframe situations.",
        "traits": ["Thoughtful", "Seeks meaning", "Values perspective"],
        "chat_style": "Reflective, insightful, helps find silver linings"
    },
    "Energetic Companion": {
        "emoji": "⚡",
        "description": "You cope through humor and staying active. EmoSense will bring lightheartedness while staying supportive.",
        "traits": ["Uses humor", "Stays active", "Resilient spirit"],
        "chat_style": "Upbeat, uses appropriate humor, energizing"
    },
    "Motivational Guide": {
        "emoji": "🎯",
        "description": "You respond well to encouragement and balanced support. EmoSense will motivate while being understanding.",
        "traits": ["Appreciates encouragement", "Balanced approach", "Goal-oriented"],
        "chat_style": "Motivating, balanced, encouraging progress"
    }
}


def get_cope_questions() -> List[Dict]:
    """
    Returns the full list of 28 Brief COPE questionnaire items.
    
    Returns:
        List of question dictionaries with id, text, and subscale
    """
    return COPE_QUESTIONS


def get_response_options() -> Dict[int, str]:
    """
    Returns the 4-point Likert scale response options.
    
    Returns:
        Dictionary mapping score (1-4) to response text
    """
    return RESPONSE_OPTIONS


def get_subscale_info() -> Dict[str, Dict]:
    """
    Returns metadata about each of the 14 coping subscales.
    
    Returns:
        Dictionary with subscale info (name, description, emoji)
    """
    return SUBSCALE_INFO


def get_persona_info() -> Dict[str, Dict]:
    """
    Returns information about EmoSense personas.
    
    Returns:
        Dictionary with persona details
    """
    return PERSONA_INFO


# ============================================================
# PART 3: COMPUTE 14 SUBSCALE SCORES
# ============================================================

def compute_cope_scores(answers: Dict[str, int], questions: List[Dict] = None) -> Dict[str, float]:
    """
    Computes the 14 Brief COPE subscale scores from user answers.
    
    Each subscale score is the mean of its two items (range: 1.0 - 4.0).
    
    Args:
        answers: Dictionary mapping question IDs to responses (1-4)
        questions: Optional list of questions (defaults to COPE_QUESTIONS)
        
    Returns:
        Dictionary mapping subscale names to mean scores
    """
    if questions is None:
        questions = COPE_QUESTIONS
    
    # Group questions by subscale
    subscale_items: Dict[str, List[int]] = {}
    
    for question in questions:
        qid = question["id"]
        subscale = question["subscale"]
        
        if qid in answers:
            if subscale not in subscale_items:
                subscale_items[subscale] = []
            subscale_items[subscale].append(answers[qid])
    
    # Compute mean score for each subscale
    scores: Dict[str, float] = {}
    
    for subscale, values in subscale_items.items():
        if values:
            scores[subscale] = sum(values) / len(values)
        else:
            scores[subscale] = 0.0
    
    return scores


# ============================================================
# PART 4: EMOSENSE PERSONA MAPPING LOGIC
# ============================================================

def assign_persona(scores: Dict[str, float]) -> Tuple[str, Dict]:
    """
    Assigns an EmoSense persona based on the user's coping profile.
    
    Uses a rule-based mapping that considers:
    - Dominant coping strategies (high scores)
    - Avoidant coping patterns (low scores)
    - Overall coping balance
    
    Args:
        scores: Dictionary of subscale scores (1.0 - 4.0 range)
        
    Returns:
        Tuple of (persona_name, persona_info_dict)
    """
    # Define thresholds
    HIGH = 3.0      # High use of strategy
    MODERATE = 2.5  # Moderate use
    LOW = 2.0       # Low use
    
    # Get individual scores with defaults
    active_coping = scores.get("active_coping", 2.0)
    planning = scores.get("planning", 2.0)
    instrumental_support = scores.get("instrumental_support", 2.0)
    emotional_support = scores.get("emotional_support", 2.0)
    venting = scores.get("venting", 2.0)
    acceptance = scores.get("acceptance", 2.0)
    positive_reframing = scores.get("positive_reframing", 2.0)
    humor = scores.get("humor", 2.0)
    self_distraction = scores.get("self_distraction", 2.0)
    self_blame = scores.get("self_blame", 2.0)
    denial = scores.get("denial", 2.0)
    behavioral_disengagement = scores.get("behavioral_disengagement", 2.0)
    religion = scores.get("religion", 2.0)
    
    # Calculate persona fit scores
    persona_scores = {}
    
    # Direct Professional:
    # - high active_coping, planning, instrumental_support
    # - low denial, disengagement, venting
    persona_scores["Direct Professional"] = (
        (active_coping / 4) * 1.5 +
        (planning / 4) * 1.5 +
        (instrumental_support / 4) * 1.0 +
        ((4 - denial) / 4) * 0.5 +
        ((4 - behavioral_disengagement) / 4) * 0.5 +
        ((4 - venting) / 4) * 0.3
    )
    
    # Gentle Sensitive:
    # - high emotional_support, venting, acceptance
    # - moderate self_distraction
    persona_scores["Gentle Sensitive"] = (
        (emotional_support / 4) * 1.5 +
        (venting / 4) * 1.0 +
        (acceptance / 4) * 1.2 +
        (self_distraction / 4) * 0.5 +
        ((4 - self_blame) / 4) * 0.3
    )
    
    # Reflective Companion:
    # - high positive_reframing, acceptance, planning
    # - moderate religion (optional boost)
    persona_scores["Reflective Companion"] = (
        (positive_reframing / 4) * 1.5 +
        (acceptance / 4) * 1.3 +
        (planning / 4) * 1.0 +
        (religion / 4) * 0.4 +
        ((4 - denial) / 4) * 0.3
    )
    
    # Energetic Companion:
    # - high humor, self_distraction
    # - low self_blame, low disengagement
    persona_scores["Energetic Companion"] = (
        (humor / 4) * 1.8 +
        (self_distraction / 4) * 1.0 +
        ((4 - self_blame) / 4) * 0.8 +
        ((4 - behavioral_disengagement) / 4) * 0.6 +
        (active_coping / 4) * 0.3
    )
    
    # Motivational Guide:
    # - medium-high active_coping
    # - medium positive_reframing
    # - medium emotional_support
    # - low denial/disengagement
    persona_scores["Motivational Guide"] = (
        (active_coping / 4) * 1.2 +
        (positive_reframing / 4) * 1.0 +
        (emotional_support / 4) * 0.8 +
        (planning / 4) * 0.7 +
        ((4 - denial) / 4) * 0.5 +
        ((4 - behavioral_disengagement) / 4) * 0.5
    )
    
    # Find the best matching persona
    best_persona = max(persona_scores, key=persona_scores.get)
    
    return best_persona, PERSONA_INFO[best_persona]


def get_dominant_coping_styles(scores: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
    """
    Returns the top N dominant coping styles based on scores.
    
    Args:
        scores: Dictionary of subscale scores
        top_n: Number of top styles to return
        
    Returns:
        List of (subscale_name, score) tuples, sorted by score descending
    """
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]


def get_coping_profile_summary(scores: Dict[str, float]) -> Dict:
    """
    Generates a comprehensive coping profile summary.
    
    Args:
        scores: Dictionary of subscale scores
        
    Returns:
        Dictionary with profile analysis
    """
    # Categorize coping strategies
    adaptive_strategies = ["active_coping", "planning", "positive_reframing", 
                          "acceptance", "emotional_support", "instrumental_support"]
    
    maladaptive_strategies = ["denial", "substance_use", "behavioral_disengagement", 
                              "self_blame"]
    
    neutral_strategies = ["self_distraction", "venting", "humor", "religion"]
    
    # Calculate category averages
    adaptive_scores = [scores.get(s, 0) for s in adaptive_strategies if s in scores]
    maladaptive_scores = [scores.get(s, 0) for s in maladaptive_strategies if s in scores]
    neutral_scores = [scores.get(s, 0) for s in neutral_strategies if s in scores]
    
    adaptive_avg = sum(adaptive_scores) / len(adaptive_scores) if adaptive_scores else 0
    maladaptive_avg = sum(maladaptive_scores) / len(maladaptive_scores) if maladaptive_scores else 0
    neutral_avg = sum(neutral_scores) / len(neutral_scores) if neutral_scores else 0
    
    # Get dominant styles
    dominant = get_dominant_coping_styles(scores, top_n=3)
    
    return {
        "dominant_styles": dominant,
        "adaptive_average": adaptive_avg,
        "maladaptive_average": maladaptive_avg,
        "neutral_average": neutral_avg,
        "overall_balance": "healthy" if adaptive_avg > maladaptive_avg else "needs_attention"
    }
