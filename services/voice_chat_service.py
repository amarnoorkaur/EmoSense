"""
Voice Chat Service for EmoSense Personal Companion
Handles Speech-to-Text (STT), Text-to-Speech (TTS), and emotion-aware responses
"""

import os
from typing import Optional, Tuple, Dict, List
from openai import OpenAI
import streamlit as st


class VoiceChatService:
    """
    Manages voice conversation pipeline:
    1. Speech-to-Text (Whisper)
    2. Emotion Detection
    3. Emotion-Aware Response Generation
    4. Text-to-Speech (TTS)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client for voice services
        
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
        self.chat_model = "gpt-4o-mini"
        self.whisper_model = "whisper-1"
        self.tts_model = "tts-1"
        self.tts_voice = "nova"  # Warm, friendly voice
    
    def speech_to_text(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio to text using OpenAI Whisper
        
        Args:
            audio_bytes: Raw audio bytes from st.audio_input()
            
        Returns:
            Transcribed text string
        """
        try:
            # Create transcription from audio bytes
            result = self.client.audio.transcriptions.create(
                file=("user_audio.wav", audio_bytes),
                model=self.whisper_model,
                response_format="text"
            )
            return result.strip()
        except Exception as e:
            raise Exception(f"Speech-to-text failed: {str(e)}")
    
    def generate_supportive_reply(
        self,
        user_text: str,
        emotion: str,
        confidence: float,
        chat_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate emotionally supportive response based on detected emotion
        
        Args:
            user_text: Transcribed user message
            emotion: Detected dominant emotion
            confidence: Confidence score for the emotion
            chat_history: Previous conversation history (optional)
            
        Returns:
            Supportive text response
        """
        try:
            # Build emotion-aware system prompt
            SYSTEM_PROMPT = f"""You are EmoSense Voice Companion — an emotionally aware AI support friend.

**User's Detected Emotion:** {emotion.capitalize()} ({confidence:.0%} confidence)

**Your Role:**
- Respond with warmth, empathy, and genuine care
- Validate the user's emotions without judgment
- Offer gentle support and grounding strategies when appropriate
- Keep responses conversational and natural (2-4 sentences)
- Speak as if having a voice conversation (avoid text-specific phrases)
- Use comforting and uplifting language

**Guidelines:**
- Do NOT diagnose or provide medical advice
- Acknowledge their feelings before offering support
- Use the detected emotion to shape your tone, but don't explicitly mention the analysis
- If they seem distressed, offer calming techniques
- If they seem happy, celebrate with them
- Keep responses concise for voice playback

**Tone:** Warm, supportive, genuine, like talking to a trusted friend"""

            # Build messages
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Add conversation history if available (last 6 messages)
            if chat_history:
                recent = chat_history[-6:]
                for msg in recent:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            messages.append({"role": "user", "content": user_text})
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.8,
                max_tokens=200,  # Shorter for voice
                top_p=0.95,
                frequency_penalty=0.3,
                presence_penalty=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Response generation failed: {str(e)}")
    
    def text_to_speech(self, reply_text: str) -> bytes:
        """
        Convert text response to speech audio
        
        Args:
            reply_text: Text to convert to speech
            
        Returns:
            Audio bytes (MP3 format)
        """
        try:
            speech_response = self.client.audio.speech.create(
                model=self.tts_model,
                voice=self.tts_voice,
                input=reply_text,
                response_format="mp3"
            )
            return speech_response.read()
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    def process_voice_input(
        self,
        audio_bytes: bytes,
        detect_emotion_fn,
        chat_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Full voice chat pipeline:
        1. Transcribe audio
        2. Detect emotion
        3. Generate response
        4. Convert to speech
        
        Args:
            audio_bytes: Raw audio from user
            detect_emotion_fn: Function to detect emotion (returns emotion, confidence)
            chat_history: Previous conversation history
            
        Returns:
            Dictionary containing:
            - user_text: Transcribed text
            - emotion: Detected emotion
            - confidence: Emotion confidence score
            - bot_response: Generated text response
            - audio_response: TTS audio bytes
        """
        result = {}
        
        # Step 1: Transcribe audio to text
        user_text = self.speech_to_text(audio_bytes)
        result["user_text"] = user_text
        
        if not user_text.strip():
            raise Exception("Could not transcribe audio. Please try speaking more clearly.")
        
        # Step 2: Detect emotion
        emotion, confidence = detect_emotion_fn(user_text)
        result["emotion"] = emotion
        result["confidence"] = confidence
        
        # Step 3: Generate supportive response
        bot_response = self.generate_supportive_reply(
            user_text, 
            emotion, 
            confidence, 
            chat_history
        )
        result["bot_response"] = bot_response
        
        # Step 4: Convert response to speech
        audio_response = self.text_to_speech(bot_response)
        result["audio_response"] = audio_response
        
        return result


# Singleton instance
_voice_service_instance = None


def get_voice_chat_service() -> Optional[VoiceChatService]:
    """
    Get or create Voice Chat Service instance
    
    Returns:
        VoiceChatService instance or None if API key unavailable
    """
    global _voice_service_instance
    
    if _voice_service_instance is None:
        try:
            _voice_service_instance = VoiceChatService()
        except ValueError:
            return None
    
    return _voice_service_instance
