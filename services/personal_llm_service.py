"""
Personal LLM Service for EmoSense Companion
Handles emotion-aware conversational AI using GPT-4o-mini
"""

import os
from typing import List, Dict, Optional, Tuple
from openai import OpenAI
import streamlit as st


class PersonalLLMService:
    """
    Manages emotionally intelligent conversations for Personal Chatbot.
    Integrates BERT emotion detection with GPT-4o-mini for natural dialogue.
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
    
    def get_system_prompt(self, mode: str, personality: str, emotion_context: Optional[Dict] = None) -> str:
        """
        Generate system prompt based on conversation mode and personality
        
        Args:
            mode: Conversation mode (Casual Chat, Comfort Me, etc.)
            personality: Bot personality (Calm, Big Sister, etc.)
            emotion_context: Current emotional state from BERT
            
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
        emotion_trend: Optional[str] = None
    ) -> str:
        """
        Generate emotionally aware conversational response
        
        Args:
            user_message: Current user message
            chat_history: Previous conversation (last 10 messages)
            mode: Conversation mode
            personality: Bot personality
            emotion_context: Current emotions from BERT (optional)
            emotion_trend: Detected emotional trend (optional)
            
        Returns:
            AI-generated response
        """
        try:
            # Build system prompt
            system_prompt = self.get_system_prompt(mode, personality, emotion_context)
            
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
            
            return response.choices[0].message.content.strip()
            
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
