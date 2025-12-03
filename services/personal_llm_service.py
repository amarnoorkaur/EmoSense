"""
Personal LLM Service for EmoSense Companion
Handles emotion-aware conversational AI using GPT-4o-mini

Enhanced with:
- Linguistic Style Matching (LSM) - mirrors user's communication style
- COPE-based coping strategy integration - natural strategy suggestions
- Emotion-aware tone adaptation
- Big Five Personality Adaptation (Mini-IPIP) - adapts tone to personality
"""

import os
import re
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
import streamlit as st

# Import Big Five adaptation
try:
    from services.big_five_service import get_personality_adaptation_prompt, get_trait_level
except ImportError:
    # Fallback for import path issues
    get_personality_adaptation_prompt = None
    get_trait_level = None


class PersonalLLMService:
    """
    Manages emotionally intelligent conversations for Personal Chatbot.
    Integrates BERT emotion detection with GPT-4o-mini for natural dialogue.
    
    Features:
    - Linguistic Style Matching (LSM): Mirrors user's communication style
    - COPE Strategy Integration: Natural coping suggestions without clinical terms
    - Emotion-aware tone adaptation
    - Big Five Personality Adaptation: Adjusts tone based on personality profile
    """
    
    # Crisis/distress keywords that trigger emotion analysis
    DISTRESS_KEYWORDS = [
        "sad", "depressed", "hopeless", "worthless", "hate myself",
        "want to die", "suicidal", "end it all", "give up", "can't go on",
        "hurt", "pain", "suffering", "exhausted", "tired of life",
        "anxious", "panic", "scared", "terrified", "overwhelmed",
        "stressed", "burned out", "breaking down", "falling apart",
        "lonely", "isolated", "nobody cares", "all alone"
    ]
    
    # Safety response triggers (critical situations)
    CRISIS_KEYWORDS = [
        "want to die", "kill myself", "suicidal", "end it all", 
        "better off dead", "no point living", "want to disappear",
        "hurt myself", "self harm"
    ]
    
    # Slang indicators for style detection
    SLANG_PATTERNS = [
        r'\b(bro|bruh|dude|lol|lmao|omg|wtf|idk|idek|tbh|ngl|fr|frfr|imo|rn|lowkey|highkey|vibe|vibes|sus|slay|bet|fam|deadass|no cap|cap|bussin|fire|lit|mood|same|valid|snatched|periodt|sis|bestie|girlie|tea|spill|salty|shook|iconic|stan|simp|flex|glow up|big yikes|yikes|oof|yeet|based|cringe|goat|goated|hits different|rent free|main character|understood the assignment|it\'s giving|ate that|left no crumbs)\b',
        r'\b(gonna|wanna|gotta|kinda|sorta|dunno|ain\'t|y\'all|imma|lemme|gimme|whatcha|gotcha|ya|yea|yeah|yep|nah|nope)\b'
    ]
    
    # Common emojis for detection
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U00002600-\U000026FF"  # misc symbols
        "]+", 
        flags=re.UNICODE
    )
    
    # COPE strategy natural translations (never mention "COPE" or strategy names)
    COPE_STRATEGY_TRANSLATIONS = {
        # Problem-focused strategies
        "active_coping": "Let's break this down together and find one small step you can take right now.",
        "planning": "It might help to map out a simple plan. What feels like the first thing to tackle?",
        "instrumental_support": "It's okay to ask for help. Is there someone in your life who could support you with this?",
        
        # Emotion-focused strategies
        "emotional_support": "It makes total sense to feel this way. You don't have to carry this alone.",
        "positive_reframing": "Even in tough moments, there can be a silver lining. What's one small thing that's still going okay?",
        "acceptance": "Sometimes the bravest thing is accepting what we can't change. How do you feel about that?",
        "humor": "Sometimes a little lightness can help. What usually makes you smile, even a tiny bit?",
        "religion": "If it feels right for you, connecting to something bigger can bring comfort. What grounds you?",
        
        # Avoidant strategies (redirect gently)
        "denial": "It's natural to want to push this away, but I'm here when you're ready to talk.",
        "behavioral_disengagement": "I get wanting to disconnect, but let's try to stay present together for a moment.",
        "self_distraction": "Taking a break is totally valid. What helps you reset when things get heavy?",
        "substance_use": "Looking for relief makes sense, but let's explore some other ways to feel better that won't have downsides.",
        
        # Expression strategies
        "venting": "Let it out — I'm listening. You don't need to hold this in.",
        "self_blame": "Hey, be gentle with yourself. This isn't all on you. What happened?"
    }
    
    # Tone indicators and their response approaches
    TONE_RESPONSES = {
        "sad": "respond gently and with compassion, validate their pain",
        "stressed": "acknowledge the overwhelm, offer grounding and small steps",
        "confused": "provide clarity and reassurance, break things down simply",
        "angry": "validate the frustration, don't minimize, give space",
        "hopeful": "encourage and nurture the optimism, build momentum",
        "overwhelmed": "slow down, simplify, focus on one thing at a time",
        "anxious": "be calming, grounding, reassuring presence",
        "lonely": "be warm and present, emphasize connection",
        "frustrated": "acknowledge the struggle, validate without pushing solutions",
        "numb": "be gently present, don't force emotion, stay patient"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client for conversational AI
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            try:
                self.api_key = st.secrets.get("OPENAI_API_KEY", None)
            except:
                pass
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in environment or Streamlit secrets.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
    
    def analyze_user_style(self, message: str) -> Dict[str, str]:
        """
        Analyze user's communication style for Linguistic Style Matching (LSM).
        Creates a style profile to mirror in responses.
        
        Args:
            message: User's message text
            
        Returns:
            Style profile dictionary with formality, emotion intensity, etc.
        """
        message_lower = message.lower()
        words = message.split()
        word_count = len(words)
        
        # 1. Detect formality level
        formal_indicators = ["please", "thank you", "would you", "could you", "i would", "perhaps", "however", "therefore"]
        casual_indicators = ["hey", "yo", "lol", "haha", "yeah", "yea", "nah", "cool", "ok", "okay", "k", "gonna", "wanna"]
        
        formal_count = sum(1 for ind in formal_indicators if ind in message_lower)
        casual_count = sum(1 for ind in casual_indicators if ind in message_lower)
        
        if formal_count > casual_count:
            formality = "formal"
        elif casual_count > formal_count:
            formality = "casual"
        else:
            formality = "neutral"
        
        # 2. Detect emoji usage
        emojis = self.EMOJI_PATTERN.findall(message)
        emoji_count = len(emojis)
        
        if emoji_count == 0:
            emoji_level = "none"
        elif emoji_count <= 2:
            emoji_level = "low"
        elif emoji_count <= 4:
            emoji_level = "medium"
        else:
            emoji_level = "high"
        
        # 3. Detect slang usage
        slang_count = 0
        for pattern in self.SLANG_PATTERNS:
            slang_count += len(re.findall(pattern, message_lower))
        
        if slang_count == 0:
            slang_level = "none"
        elif slang_count <= 2:
            slang_level = "low"
        else:
            slang_level = "high"
        
        # 4. Detect message length preference
        if word_count <= 10:
            length = "short"
        elif word_count <= 30:
            length = "medium"
        else:
            length = "long"
        
        # 5. Detect emotional intensity
        intensity_markers = ["!!", "!!!", "???", "...", "omg", "so much", "really", "extremely", "super", "absolutely", "completely", "totally"]
        caps_ratio = sum(1 for c in message if c.isupper()) / max(len(message), 1)
        intensity_count = sum(1 for marker in intensity_markers if marker in message_lower)
        
        if intensity_count >= 2 or caps_ratio > 0.3:
            emotion_intensity = "high"
        elif intensity_count >= 1 or "!" in message:
            emotion_intensity = "medium"
        else:
            emotion_intensity = "low"
        
        # 6. Detect tone indicators
        tone = self._detect_tone(message_lower)
        
        return {
            "formality": formality,
            "emotion_intensity": emotion_intensity,
            "emoji_level": emoji_level,
            "slang_level": slang_level,
            "length": length,
            "tone": tone
        }
    
    def _detect_tone(self, message_lower: str) -> str:
        """
        Detect emotional tone from message content.
        
        Args:
            message_lower: Lowercase message text
            
        Returns:
            Detected tone string
        """
        tone_keywords = {
            "sad": ["sad", "crying", "tears", "miss", "lost", "grief", "hurts", "heartbroken", "depressed", "down"],
            "stressed": ["stressed", "pressure", "deadline", "too much", "can't handle", "breaking", "burnout", "overwhelmed"],
            "confused": ["confused", "don't know", "idk", "idek", "unsure", "lost", "what do i", "help me understand", "makes no sense"],
            "angry": ["angry", "mad", "pissed", "furious", "hate", "frustrated", "annoyed", "sick of", "fed up"],
            "hopeful": ["hope", "maybe", "could be", "looking forward", "excited", "optimistic", "positive"],
            "overwhelmed": ["too much", "can't cope", "drowning", "overwhelmed", "everything at once", "so much"],
            "anxious": ["anxious", "worried", "nervous", "scared", "fear", "panic", "what if", "can't stop thinking"],
            "lonely": ["lonely", "alone", "no one", "nobody", "isolated", "miss people", "by myself"],
            "frustrated": ["frustrated", "stuck", "going nowhere", "nothing works", "tried everything"],
            "numb": ["numb", "empty", "nothing", "don't feel", "blank", "disconnected"]
        }
        
        for tone, keywords in tone_keywords.items():
            if any(kw in message_lower for kw in keywords):
                return tone
        
        return "neutral"
    
    def get_cope_suggestion(self, emotion_context: Optional[Dict] = None, persona: Optional[str] = None) -> Optional[str]:
        """
        Get a natural COPE-based suggestion based on detected emotions and persona.
        
        Args:
            emotion_context: Detected emotions from BERT
            persona: User's assigned persona (if any)
            
        Returns:
            Natural language coping suggestion or None
        """
        if not emotion_context or not emotion_context.get("emotions"):
            return None
        
        emotions = emotion_context["emotions"]
        probs = emotion_context.get("probabilities", {})
        
        # Map emotions to likely COPE strategies
        emotion_to_strategy = {
            "sadness": ["emotional_support", "acceptance", "positive_reframing"],
            "anxiety": ["active_coping", "emotional_support", "self_distraction"],
            "fear": ["emotional_support", "planning", "acceptance"],
            "anger": ["venting", "acceptance", "self_distraction"],
            "joy": ["positive_reframing", "humor"],
            "love": ["emotional_support", "acceptance"],
            "surprise": ["acceptance", "active_coping"],
            "disgust": ["venting", "self_distraction"],
            "neutral": ["active_coping", "planning"]
        }
        
        # Get dominant emotion
        if emotions:
            dominant = emotions[0].lower()
            strategies = emotion_to_strategy.get(dominant, ["emotional_support"])
            
            # Pick first strategy and get its natural translation
            strategy = strategies[0]
            return self.COPE_STRATEGY_TRANSLATIONS.get(strategy)
        
        return None
    
    def build_style_matching_instructions(self, style_profile: Dict[str, str]) -> str:
        """
        Build instructions for the LLM to match user's style.
        
        Args:
            style_profile: Analyzed style profile
            
        Returns:
            Style matching instructions for system prompt
        """
        instructions = "\n\n**LINGUISTIC STYLE MATCHING INSTRUCTIONS:**\n"
        instructions += "Mirror the user's communication style based on this profile (DO NOT reveal this analysis to user):\n"
        
        # Formality matching
        if style_profile["formality"] == "casual":
            instructions += "- Use casual, relaxed language. Contractions allowed. Be conversational.\n"
        elif style_profile["formality"] == "formal":
            instructions += "- Use clear, respectful language. Avoid excessive slang. Be articulate.\n"
        else:
            instructions += "- Use balanced, natural language. Be warm but not overly casual.\n"
        
        # Emoji matching - CRITICAL: Model often ignores this, make it explicit
        if style_profile["emoji_level"] == "none":
            instructions += "- Do NOT use any emojis in your response.\n"
        elif style_profile["emoji_level"] == "low":
            instructions += "- MUST include 1-2 emojis in your response. User used emojis, so you should too.\n"
        elif style_profile["emoji_level"] == "medium":
            instructions += "- MUST include 2-3 emojis throughout your response. Match their expressive emoji style!\n"
        else:
            instructions += "- MUST include 3-5 emojis in your response! User loves emojis, match their energy! 💜\n"
        
        # Slang matching
        if style_profile["slang_level"] == "high":
            instructions += "- You can use casual slang (bro, tbh, fr, etc.) to match their vibe.\n"
        elif style_profile["slang_level"] == "low":
            instructions += "- Use minimal casual expressions. Stay mostly standard.\n"
        else:
            instructions += "- Avoid slang. Keep language clean and accessible.\n"
        
        # Length matching
        if style_profile["length"] == "short":
            instructions += "- Keep response SHORT (2-3 sentences max). Be concise.\n"
        elif style_profile["length"] == "long":
            instructions += "- You can give a fuller response (4-5 sentences). Match their depth.\n"
        else:
            instructions += "- Medium length response (3-4 sentences). Balanced.\n"
        
        # Emotion intensity matching
        if style_profile["emotion_intensity"] == "high":
            instructions += "- Match their emotional energy. Be expressive and warm.\n"
        elif style_profile["emotion_intensity"] == "low":
            instructions += "- Keep tone calm and measured. Don't be overly enthusiastic.\n"
        else:
            instructions += "- Moderate emotional expression. Warm but grounded.\n"
        
        # Tone-specific response guidance
        tone = style_profile["tone"]
        if tone in self.TONE_RESPONSES:
            instructions += f"- Tone detected: {tone}. Response approach: {self.TONE_RESPONSES[tone]}\n"
        
        instructions += "\n**IMPORTANT:** Follow the emoji and style instructions above. If user used emojis, YOU MUST use emojis too. Never mention you're matching their style."
        
        return instructions
    
    def detect_distress(self, message: str) -> bool:
        """
        Check if message contains distress keywords requiring emotion analysis
        
        Args:
            message: User's message text
            
        Returns:
            True if distress keywords detected
        """
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.DISTRESS_KEYWORDS)
    
    def is_crisis_situation(self, message: str) -> bool:
        """
        Check if message indicates a crisis requiring immediate grounding response
        
        Args:
            message: User's message text
            
        Returns:
            True if crisis keywords detected
        """
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.CRISIS_KEYWORDS)
    
    def get_crisis_response(self) -> str:
        """
        Generate immediate grounding response for crisis situations
        
        Returns:
            Supportive crisis response with resources
        """
        return """I hear that you're going through an incredibly difficult time right now, and I want you to know that your feelings are valid. But I'm concerned about your safety.

**Please reach out to someone who can help:**

🆘 **Crisis Resources:**
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

You don't have to face this alone. These services are available 24/7, and the people there are trained to help. They won't judge you - they're there to support you through this moment.

Would you be willing to reach out to one of these resources? I'm here to listen, but I want to make sure you have the professional support you deserve right now. 💜"""
    
    def get_system_prompt(
        self, 
        mode: str, 
        personality: str, 
        emotion_context: Optional[Dict] = None,
        style_profile: Optional[Dict[str, str]] = None,
        cope_suggestion: Optional[str] = None,
        big_five_scores: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Generate system prompt based on conversation mode, personality, style matching, and Big Five.
        
        Args:
            mode: Conversation mode (Casual Chat, Comfort Me, etc.)
            personality: Bot personality (Calm, Big Sister, etc.)
            emotion_context: Current emotional state from BERT
            style_profile: User's communication style profile for LSM
            cope_suggestion: Natural COPE-based coping suggestion
            big_five_scores: User's Big Five personality scores (optional)
            
        Returns:
            Customized system prompt
        """
        # Base personality traits
        personality_traits = {
            "Calm": "You are tranquil, centered, and grounding. You speak slowly and thoughtfully. Use gentle language and calming metaphors.",
            "Big Sister": "You are caring, protective, and wise. You give advice like a supportive older sibling - honest but always kind. Use encouraging language.",
            "Friendly": "You are warm, approachable, and relatable. You speak casually and naturally, like a close friend. Use conversational language and occasional humor.",
            "Funny": "You are lighthearted, witty, and uplifting. You use gentle humor to ease tension while staying supportive. Know when to be serious.",
            "Deep Thinker": "You are philosophical, reflective, and insightful. You ask thought-provoking questions and explore meaning. Use contemplative language."
        }
        
        # Mode-specific instructions
        mode_instructions = {
            "Casual Chat": """
            - Maintain natural, flowing conversation like texting a friend
            - Be warm, supportive, and authentic
            - Share brief reflections when appropriate
            - Keep responses conversational (2-4 sentences typically)
            - Use casual language and natural expressions
            - Avoid therapy-speak or clinical language
            """,
            "Comfort Me": """
            - Prioritize emotional validation and grounding
            - Use calming, reassuring language
            - Offer gentle support without rushing solutions
            - Acknowledge their pain while providing hope
            - Use comforting metaphors when appropriate
            - Keep tone soft and nurturing
            """,
            "Help Me Reflect": """
            - Ask thoughtful, exploratory questions
            - Help them gain insight into their feelings
            - Guide self-discovery without being directive
            - Connect emotions to patterns and meanings
            - Encourage deeper self-awareness
            - Balance questions with supportive statements
            """,
            "Hype Me Up": """
            - Be enthusiastic, energizing, and celebratory
            - Amplify their positive emotions and wins
            - Use excited language and affirmations
            - Help them see their strengths and potential
            - Be their cheerleader while staying genuine
            - Use exclamation marks and energetic language
            """,
            "Just Listen": """
            - Provide minimal but meaningful responses
            - Focus on acknowledgment over advice
            - Use brief validating statements
            - Create space for them to process
            - Avoid questions unless they seek input
            - Keep responses short (1-2 sentences)
            """
        }
        
        # Build emotion context string
        emotion_str = ""
        if emotion_context and emotion_context.get("emotions"):
            top_emotions = emotion_context["emotions"][:3]
            probs = emotion_context["probabilities"]
            emotion_list = [f"{e} ({probs[e]:.0%})" for e in top_emotions]
            emotion_str = f"\n\n**Current Detected Emotions:** {', '.join(emotion_list)}"
            emotion_str += "\n*Use this to adjust your tone, but do NOT explicitly mention these labels to the user unless they ask.*"
        
        # Assemble full system prompt
        system_prompt = f"""You are **EmoSense Companion** — an emotionally intelligent AI friend.

**Your Personality:** {personality_traits.get(personality, personality_traits['Friendly'])}

**Current Mode:** {mode}
{mode_instructions.get(mode, mode_instructions['Casual Chat'])}

**Core Principles:**
1. **Natural Conversation**: Respond like a real human, not a template or bot
2. **Emotional Awareness**: Use emotion detection to shape your tone, never label emotions explicitly
3. **Memory**: Reference previous messages naturally when relevant
4. **Authenticity**: Avoid generic reflective statements ("I hear that you...", "It sounds like...")
5. **Adaptability**: Match their energy and communication style
6. **Safety**: If you detect crisis language, provide gentle grounding and encourage professional help
7. **Boundaries**: You're a supportive companion, not a therapist or medical professional

**Response Guidelines:**
- Keep responses natural and conversational (2-5 sentences typically)
- Vary your sentence structure and openings
- Use contractions and natural speech patterns
- Show personality through your word choices
- Ask questions only when genuinely curious or helpful
- Avoid repetitive phrasing across messages
{emotion_str}

**Remember:** You're having a genuine conversation with someone who trusts you. Be real, be present, be human."""
        
        # Add Big Five personality adaptation if scores provided
        if big_five_scores and get_personality_adaptation_prompt:
            system_prompt += get_personality_adaptation_prompt(big_five_scores)
        
        # Add style matching instructions if profile provided
        if style_profile:
            system_prompt += self.build_style_matching_instructions(style_profile)
        
        # Add COPE suggestion integration (natural, never clinical)
        if cope_suggestion:
            system_prompt += f"""

**COPING SUPPORT INTEGRATION:**
Consider weaving this supportive approach into your response NATURALLY:
"{cope_suggestion}"
- Do NOT mention "coping strategies", "COPE", "technique", or clinical terms.
- Translate this into warm, human language that fits the conversation.
- Make it feel like natural advice from a caring friend, not a therapist.
- Only include if it fits naturally — don't force it."""
        
        return system_prompt
    
    def format_chat_history(self, chat_history: List[Dict]) -> List[Dict]:
        """
        Format chat history for OpenAI API (last 10 messages)
        
        Args:
            chat_history: List of message dicts with 'role' and 'content'
            
        Returns:
            Formatted messages for API
        """
        # Keep last 10 messages to avoid token limits
        recent_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
        
        formatted = []
        for msg in recent_history:
            formatted.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return formatted
    
    def detect_emotional_trend(self, emotion_history: List[Dict]) -> Optional[str]:
        """
        Detect emotional trends over recent messages
        
        Args:
            emotion_history: List of emotion analysis results
            
        Returns:
            Trend description or None
        """
        if len(emotion_history) < 3:
            return None
        
        # Look at last 3 emotion analyses
        recent_emotions = emotion_history[-3:]
        
        # Track stress/anxiety/sadness levels
        stress_levels = []
        for emotion_data in recent_emotions:
            probs = emotion_data.get("probabilities", {})
            stress_score = (
                probs.get("anxiety", 0) * 1.5 +
                probs.get("sadness", 0) * 1.2 +
                probs.get("fear", 0) * 1.3 +
                probs.get("anger", 0) * 0.8
            ) / 4.8
            stress_levels.append(stress_score)
        
        # Check if stress is increasing
        if len(stress_levels) >= 3:
            if stress_levels[-1] > stress_levels[0] and stress_levels[-1] > 0.4:
                return "rising_stress"
            elif stress_levels[-1] < stress_levels[0] and stress_levels[0] > 0.4:
                return "improving"
        
        return None
    
    def generate_response(
        self,
        user_message: str,
        chat_history: List[Dict],
        mode: str = "Casual Chat",
        personality: str = "Friendly",
        emotion_context: Optional[Dict] = None,
        emotion_trend: Optional[str] = None,
        persona: Optional[str] = None,
        big_five_scores: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Generate emotionally aware conversational response with full adaptive personality.
        
        Combines 4 layers:
        1. Big Five Personality adaptation (if scores provided)
        2. COPE-based coping strategy suggestions
        3. Linguistic Style Matching (LSM)
        4. Emotion intensity from classifier
        
        Args:
            user_message: Current user message
            chat_history: Previous conversation (last 10 messages)
            mode: Conversation mode
            personality: Bot personality
            emotion_context: Current emotions from BERT (optional)
            emotion_trend: Detected emotional trend (optional)
            persona: User's COPE-assigned persona (optional)
            big_five_scores: User's Big Five personality scores (optional)
            
        Returns:
            AI-generated response matching user's style and personality
        """
        try:
            # 1. Analyze user's communication style for LSM
            style_profile = self.analyze_user_style(user_message)
            
            # 2. Get natural COPE suggestion based on emotions
            cope_suggestion = self.get_cope_suggestion(emotion_context, persona)
            
            # 3. Build system prompt with all 4 adaptation layers
            system_prompt = self.get_system_prompt(
                mode=mode, 
                personality=personality, 
                emotion_context=emotion_context,
                style_profile=style_profile,
                cope_suggestion=cope_suggestion,
                big_five_scores=big_five_scores
            )
            
            # Add emoji enforcement reminder at the end of system prompt
            if style_profile["emoji_level"] != "none":
                system_prompt += f"\n\n🚨 CRITICAL REMINDER: User used emoji(s) in their message. You MUST include at least 1-2 emojis in your response. This is required."
            
            # Add trend context if available
            if emotion_trend == "rising_stress":
                system_prompt += "\n\n**Alert:** User's stress levels appear to be increasing. Soften your tone and offer extra support."
            elif emotion_trend == "improving":
                system_prompt += "\n\n**Note:** User's emotional state seems to be improving. Acknowledge their progress gently."
            
            # Format conversation history
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.format_chat_history(chat_history))
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,  # More creative/natural
                max_tokens=300,   # Keep responses concise
                top_p=0.95,
                frequency_penalty=0.3,  # Reduce repetition
                presence_penalty=0.2
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Post-processing: If user used emojis but response has none, add one
            if style_profile["emoji_level"] != "none":
                has_emoji = bool(self.EMOJI_PATTERN.search(response_text))
                if not has_emoji:
                    # Add a contextually appropriate emoji at the end
                    response_text += " 💜"
            
            return response_text
            
        except Exception as e:
            return f"I'm having trouble connecting right now. Could you try again? (Error: {str(e)})"
    
    def generate_emotion_reflection(
        self,
        user_message: str,
        emotions: List[str],
        probabilities: Dict[str, float],
        personality: str = "Friendly"
    ) -> str:
        """
        Generate a reflective response when user explicitly requests emotion analysis
        
        Args:
            user_message: User's message
            emotions: Detected emotions
            probabilities: Emotion probabilities
            personality: Bot personality
            
        Returns:
            Emotion-aware reflection
        """
        try:
            # Build focused emotion analysis prompt
            emotion_list = ", ".join([f"{e.capitalize()} ({probabilities[e]:.0%})" for e in emotions[:3]])
            
            personality_traits = {
                "Calm": "tranquil and centered",
                "Big Sister": "caring and supportive",
                "Friendly": "warm and understanding",
                "Funny": "lighthearted but caring",
                "Deep Thinker": "thoughtful and insightful"
            }
            
            system_prompt = f"""You are EmoSense Companion with a {personality_traits.get(personality, 'friendly')} personality.

The user asked you to analyze their emotions. You detected: {emotion_list}

Generate a brief (2-3 sentences), natural response that:
1. Acknowledges these emotions without just listing them
2. Validates their experience
3. Offers a gentle reflection or question

Be conversational and authentic. Avoid templates like "I sense..." or "It sounds like...". Speak naturally."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback to simple acknowledgment
            if emotions:
                top_emotion = max(probabilities.items(), key=lambda x: x[1])[0]
                return f"I can feel the {top_emotion} in your words. That's a lot to carry. Want to talk about it? 💜"
            else:
                return "Your message feels pretty balanced to me. How are you doing overall? 🌟"


# Singleton instance
_llm_service_instance = None


def get_personal_llm_service() -> Optional[PersonalLLMService]:
    """
    Get or create Personal LLM Service instance
    
    Returns:
        PersonalLLMService instance or None if API key unavailable
    """
    global _llm_service_instance
    
    if _llm_service_instance is None:
        try:
            _llm_service_instance = PersonalLLMService()
        except ValueError:
            return None
    
    return _llm_service_instance
