"""
Big Five Personality Assessment Service (Mini-IPIP-20)
Based on Donnellan et al., 2006 - validated 20-item scale

Measures 5 personality dimensions:
- Extraversion (E)
- Agreeableness (A)
- Conscientiousness (C)
- Neuroticism (N)
- Openness/Intellect (O)

Each trait score ranges from 1.0 to 5.0
"""

from typing import Dict, List, Tuple, Optional


# ============================================================
# MINI-IPIP-20 QUESTIONS
# ============================================================

MINI_IPIP_QUESTIONS: List[Dict] = [
    # Extraversion (items 1-4)
    {"id": 1, "trait": "E", "text": "I am the life of the party.", "reverse": False},
    {"id": 2, "trait": "E", "text": "I don't talk a lot.", "reverse": True},
    {"id": 3, "trait": "E", "text": "I feel comfortable around people.", "reverse": False},
    {"id": 4, "trait": "E", "text": "I keep in the background.", "reverse": True},
    
    # Agreeableness (items 5-8)
    {"id": 5, "trait": "A", "text": "I sympathize with others' feelings.", "reverse": False},
    {"id": 6, "trait": "A", "text": "I am not interested in other people's problems.", "reverse": True},
    {"id": 7, "trait": "A", "text": "I have a soft heart.", "reverse": False},
    {"id": 8, "trait": "A", "text": "I feel others' emotions.", "reverse": False},
    
    # Conscientiousness (items 9-12)
    {"id": 9, "trait": "C", "text": "I get chores done right away.", "reverse": False},
    {"id": 10, "trait": "C", "text": "I often forget to put things back in their proper place.", "reverse": True},
    {"id": 11, "trait": "C", "text": "I like order.", "reverse": False},
    {"id": 12, "trait": "C", "text": "I make a mess of things.", "reverse": True},
    
    # Neuroticism (items 13-16)
    {"id": 13, "trait": "N", "text": "I have frequent mood swings.", "reverse": False},
    {"id": 14, "trait": "N", "text": "I am relaxed most of the time.", "reverse": True},
    {"id": 15, "trait": "N", "text": "I get upset easily.", "reverse": False},
    {"id": 16, "trait": "N", "text": "I seldom feel blue.", "reverse": True},
    
    # Openness/Intellect (items 17-20)
    {"id": 17, "trait": "O", "text": "I have a vivid imagination.", "reverse": False},
    {"id": 18, "trait": "O", "text": "I am not interested in abstract ideas.", "reverse": True},
    {"id": 19, "trait": "O", "text": "I have difficulty understanding abstract ideas.", "reverse": True},
    {"id": 20, "trait": "O", "text": "I am full of ideas.", "reverse": False},
]

# Response options (1-5 Likert scale)
RESPONSE_OPTIONS: List[Dict] = [
    {"value": 1, "label": "Strongly Disagree"},
    {"value": 2, "label": "Disagree"},
    {"value": 3, "label": "Neutral"},
    {"value": 4, "label": "Agree"},
    {"value": 5, "label": "Strongly Agree"},
]

# Trait full names and emojis
TRAIT_INFO: Dict[str, Dict] = {
    "E": {
        "name": "Extraversion",
        "emoji": "🔵",
        "color": "#3B82F6",
        "high_desc": "Outgoing, energetic, talkative",
        "low_desc": "Reserved, quiet, introspective",
    },
    "A": {
        "name": "Agreeableness", 
        "emoji": "🟢",
        "color": "#10B981",
        "high_desc": "Warm, compassionate, trusting",
        "low_desc": "Direct, practical, analytical",
    },
    "C": {
        "name": "Conscientiousness",
        "emoji": "🟡", 
        "color": "#F59E0B",
        "high_desc": "Organized, disciplined, reliable",
        "low_desc": "Flexible, spontaneous, adaptable",
    },
    "N": {
        "name": "Neuroticism",
        "emoji": "🔴",
        "color": "#EF4444",
        "high_desc": "Emotionally sensitive, reactive",
        "low_desc": "Emotionally stable, resilient",
    },
    "O": {
        "name": "Openness",
        "emoji": "🟣",
        "color": "#8B5CF6",
        "high_desc": "Creative, curious, imaginative",
        "low_desc": "Practical, conventional, grounded",
    },
}


# ============================================================
# SCORING FUNCTIONS
# ============================================================

def score_mini_ipip(responses: Dict[int, int]) -> Dict[str, float]:
    """
    Score the Mini-IPIP-20 questionnaire.
    
    Args:
        responses: Dictionary mapping question ID (1-20) to response value (1-5)
        
    Returns:
        Dictionary with trait scores (1.0 to 5.0):
        {
            "extraversion": float,
            "agreeableness": float,
            "conscientiousness": float,
            "neuroticism": float,
            "openness": float
        }
    """
    # Reverse-keyed items
    reverse_items = {2, 4, 6, 10, 12, 14, 16, 18, 19}
    
    # Apply reverse scoring
    scored = {}
    for i in range(1, 21):
        if i in reverse_items:
            scored[i] = 6 - responses.get(i, 3)  # Default to neutral if missing
        else:
            scored[i] = responses.get(i, 3)
    
    # Compute trait means
    extraversion = (scored[1] + scored[2] + scored[3] + scored[4]) / 4
    agreeableness = (scored[5] + scored[6] + scored[7] + scored[8]) / 4
    conscientiousness = (scored[9] + scored[10] + scored[11] + scored[12]) / 4
    neuroticism = (scored[13] + scored[14] + scored[15] + scored[16]) / 4
    openness = (scored[17] + scored[18] + scored[19] + scored[20]) / 4
    
    return {
        "extraversion": round(extraversion, 2),
        "agreeableness": round(agreeableness, 2),
        "conscientiousness": round(conscientiousness, 2),
        "neuroticism": round(neuroticism, 2),
        "openness": round(openness, 2)
    }


def get_trait_level(score: float) -> str:
    """
    Categorize a trait score into low/medium/high.
    
    Args:
        score: Trait score (1.0 to 5.0)
        
    Returns:
        "low", "medium", or "high"
    """
    if score <= 2.5:
        return "low"
    elif score <= 3.5:
        return "medium"
    else:
        return "high"


def get_personality_summary(scores: Dict[str, float]) -> Dict[str, Dict]:
    """
    Generate a human-readable personality summary.
    
    Args:
        scores: Dictionary of trait scores
        
    Returns:
        Dictionary with trait details and levels
    """
    summary = {}
    
    trait_keys = {
        "extraversion": "E",
        "agreeableness": "A",
        "conscientiousness": "C",
        "neuroticism": "N",
        "openness": "O"
    }
    
    for trait_name, trait_code in trait_keys.items():
        score = scores.get(trait_name, 3.0)
        level = get_trait_level(score)
        info = TRAIT_INFO[trait_code]
        
        summary[trait_name] = {
            "score": score,
            "level": level,
            "emoji": info["emoji"],
            "color": info["color"],
            "description": info["high_desc"] if level == "high" else (info["low_desc"] if level == "low" else "Balanced")
        }
    
    return summary


def get_dominant_traits(scores: Dict[str, float], threshold: float = 3.5) -> List[str]:
    """
    Get list of dominant (high-scoring) traits.
    
    Args:
        scores: Dictionary of trait scores
        threshold: Minimum score to be considered dominant
        
    Returns:
        List of dominant trait names
    """
    dominant = []
    for trait, score in scores.items():
        if score >= threshold:
            dominant.append(trait)
    return dominant


# ============================================================
# TONE ADAPTATION RULES
# ============================================================

def get_big_five_tone_instructions(scores: Dict[str, float]) -> str:
    """
    Generate tone adaptation instructions based on Big Five scores.
    
    Args:
        scores: Dictionary of trait scores
        
    Returns:
        String with tone instructions for the LLM
    """
    instructions = []
    
    # Extraversion rules
    e_score = scores.get("extraversion", 3.0)
    if e_score >= 3.5:
        instructions.append("• EXTRAVERSION (High): Use energetic, enthusiastic tone. Emojis encouraged. Be encouraging and upbeat.")
    elif e_score <= 2.5:
        instructions.append("• EXTRAVERSION (Low): Use calm, quieter tone. Fewer emojis. Be more reflective and gentle.")
    else:
        instructions.append("• EXTRAVERSION (Medium): Use balanced energy. Moderate expressiveness.")
    
    # Agreeableness rules
    a_score = scores.get("agreeableness", 3.0)
    if a_score >= 3.5:
        instructions.append("• AGREEABLENESS (High): Be very warm, compassionate, validating. Prioritize emotional support.")
    elif a_score <= 2.5:
        instructions.append("• AGREEABLENESS (Low): Be direct and practical. Less emotional fluff, more straightforward advice.")
    else:
        instructions.append("• AGREEABLENESS (Medium): Balance warmth with practicality.")
    
    # Conscientiousness rules
    c_score = scores.get("conscientiousness", 3.0)
    if c_score >= 3.5:
        instructions.append("• CONSCIENTIOUSNESS (High): Provide structured, step-by-step guidance. Actionable plans with clear steps.")
    elif c_score <= 2.5:
        instructions.append("• CONSCIENTIOUSNESS (Low): Keep advice simple and low-effort. Small, easy steps. No overwhelming lists.")
    else:
        instructions.append("• CONSCIENTIOUSNESS (Medium): Balance structure with flexibility.")
    
    # Neuroticism rules
    n_score = scores.get("neuroticism", 3.0)
    if n_score >= 3.5:
        instructions.append("• NEUROTICISM (High): Use very soothing, reassuring tone. Prioritize grounding. Avoid overwhelming with too much detail.")
    elif n_score <= 2.5:
        instructions.append("• NEUROTICISM (Low): Be action-focused and straightforward. Cognitive reframing is okay.")
    else:
        instructions.append("• NEUROTICISM (Medium): Balance reassurance with practical guidance.")
    
    # Openness rules
    o_score = scores.get("openness", 3.0)
    if o_score >= 3.5:
        instructions.append("• OPENNESS (High): Use creative suggestions, analogies, metaphors. Encourage deeper reflection and exploration.")
    elif o_score <= 2.5:
        instructions.append("• OPENNESS (Low): Keep suggestions practical and literal. Avoid abstract concepts. Concrete advice only.")
    else:
        instructions.append("• OPENNESS (Medium): Mix practical with occasional creative suggestions.")
    
    return "\n".join(instructions)


def get_personality_adaptation_prompt(scores: Dict[str, float]) -> str:
    """
    Generate a complete personality adaptation section for the system prompt.
    
    Args:
        scores: Dictionary of trait scores
        
    Returns:
        Full personality adaptation instructions
    """
    tone_rules = get_big_five_tone_instructions(scores)
    
    prompt = f"""
**BIG FIVE PERSONALITY ADAPTATION:**
The user has completed a personality assessment. Adapt your communication style to match their personality profile:

{tone_rules}

**CRITICAL:** Apply these rules subtly and naturally. NEVER mention personality traits, Big Five, or assessment results to the user. Just adapt your tone seamlessly."""
    
    return prompt


# ============================================================
# PERSONA MAPPING FROM BIG FIVE
# ============================================================

def map_big_five_to_persona(scores: Dict[str, float]) -> Tuple[str, str]:
    """
    Map Big Five scores to the closest COPE-based persona.
    
    Args:
        scores: Dictionary of trait scores
        
    Returns:
        Tuple of (persona_name, rationale)
    """
    e = scores.get("extraversion", 3.0)
    a = scores.get("agreeableness", 3.0)
    c = scores.get("conscientiousness", 3.0)
    n = scores.get("neuroticism", 3.0)
    o = scores.get("openness", 3.0)
    
    # Decision tree for persona mapping
    if c >= 3.5 and n <= 3.0:
        # High conscientiousness, low neuroticism → Direct Professional
        return "Direct Professional", "You prefer structured, practical approaches and stay calm under pressure."
    
    elif a >= 4.0 and n >= 3.5:
        # High agreeableness, high neuroticism → Gentle Sensitive
        return "Gentle Sensitive", "You're deeply empathetic and may need gentle, validating support."
    
    elif o >= 4.0 and e <= 3.0:
        # High openness, lower extraversion → Reflective Companion
        return "Reflective Companion", "You enjoy deep thinking and introspection."
    
    elif e >= 4.0 and a >= 3.5:
        # High extraversion, high agreeableness → Energetic Companion
        return "Energetic Companion", "You thrive on positive energy and social connection."
    
    elif c >= 3.0 and e >= 3.0 and n <= 3.5:
        # Balanced with action orientation → Motivational Guide
        return "Motivational Guide", "You respond well to encouragement and goal-oriented support."
    
    elif n >= 4.0:
        # Very high neuroticism → Gentle Sensitive (needs soothing)
        return "Gentle Sensitive", "You may benefit from gentle, calming support."
    
    elif a >= 3.5:
        # Agreeable → Gentle Sensitive
        return "Gentle Sensitive", "Your warm, empathetic nature aligns with nurturing support."
    
    else:
        # Default → Motivational Guide (balanced)
        return "Motivational Guide", "A balanced approach with encouragement and practical guidance."


def get_recommended_personality(scores: Dict[str, float]) -> str:
    """
    Get recommended bot personality based on Big Five scores.
    
    Args:
        scores: Dictionary of trait scores
        
    Returns:
        Recommended personality name
    """
    persona, _ = map_big_five_to_persona(scores)
    
    # Map persona to bot personality
    persona_to_personality = {
        "Direct Professional": "Calm",
        "Gentle Sensitive": "Big Sister",
        "Reflective Companion": "Deep Thinker",
        "Energetic Companion": "Funny",
        "Motivational Guide": "Friendly"
    }
    
    return persona_to_personality.get(persona, "Friendly")
