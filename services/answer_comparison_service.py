"""
Answer Comparison Service for Business Buddy
Compares Raw ChatGPT responses vs Refined Business Buddy responses
Demonstrates the power of prompt engineering
"""

import os
from typing import Dict, Optional, Tuple
from openai import OpenAI
import streamlit as st


# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

# Raw ChatGPT - minimal instruction (baseline)
RAW_SYSTEM_PROMPT = """You are ChatGPT. Answer the user's question directly."""

# Refined Business Buddy - custom instruction set with prompt engineering
REFINED_SYSTEM_PROMPT = """You are Business Buddy — an AI assistant specialized in customer feedback interpretation, 
emotion-aware analysis, and business recommendations.

Your goal is to answer with:
- Clear structure (bullet points, insights, do/don't)
- Emotion-aware tone (understand the emotional context behind business questions)
- Actionable business suggestions with specific steps
- Crisp, concise, jargon-free language
- Professional yet approachable tone

RESPONSE FORMAT:
1. **Quick Answer** - 1-2 sentence direct answer
2. **Key Insights** - Bullet points of main points
3. **Recommendations** - Actionable steps (numbered)
4. **Do's and Don'ts** - Quick guidance table
5. **Summary** - One-liner takeaway

Keep responses focused, structured, and immediately actionable for business professionals."""


class AnswerComparisonService:
    """
    Service for comparing raw vs refined AI responses
    Demonstrates prompt engineering impact on response quality
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Try Streamlit secrets if env var not found
        if not self.api_key:
            try:
                self.api_key = st.secrets.get("OPENAI_API_KEY", None)
            except:
                pass
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Cost-effective, fast model
    
    def get_raw_answer(self, question: str) -> Dict[str, any]:
        """
        Get raw ChatGPT response without prompt engineering
        
        Args:
            question: User's business question
            
        Returns:
            Dict with response text, tokens used, and success status
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": RAW_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "tokens_used": None,
                "model": self.model
            }
    
    def get_refined_answer(self, question: str) -> Dict[str, any]:
        """
        Get refined Business Buddy response with prompt engineering
        
        Args:
            question: User's business question
            
        Returns:
            Dict with response text, tokens used, and success status
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": REFINED_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=0.6,  # Slightly lower for more consistent structure
                max_tokens=700    # More tokens for structured response
            )
            
            return {
                "success": True,
                "response": response.choices[0].message.content.strip(),
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "model": self.model
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "tokens_used": None,
                "model": self.model
            }
    
    def get_comparison(self, question: str) -> Tuple[Dict, Dict]:
        """
        Get both raw and refined answers for comparison
        
        Args:
            question: User's business question
            
        Returns:
            Tuple of (raw_result, refined_result)
        """
        raw_result = self.get_raw_answer(question)
        refined_result = self.get_refined_answer(question)
        
        return raw_result, refined_result
    
    def analyze_differences(self, raw_response: str, refined_response: str) -> Dict[str, any]:
        """
        Analyze key differences between raw and refined responses
        
        Args:
            raw_response: Raw ChatGPT response text
            refined_response: Refined Business Buddy response text
            
        Returns:
            Dict with analysis of improvements
        """
        # Basic analysis metrics
        raw_lines = raw_response.strip().split('\n')
        refined_lines = refined_response.strip().split('\n')
        
        # Count structural elements
        raw_bullets = sum(1 for line in raw_lines if line.strip().startswith(('-', '•', '*')))
        refined_bullets = sum(1 for line in refined_lines if line.strip().startswith(('-', '•', '*')))
        
        raw_numbered = sum(1 for line in raw_lines if line.strip()[:2].replace('.', '').isdigit())
        refined_numbered = sum(1 for line in refined_lines if line.strip()[:2].replace('.', '').isdigit())
        
        # Count headers/sections (markdown bold or ##)
        raw_sections = sum(1 for line in raw_lines if '**' in line or line.strip().startswith('#'))
        refined_sections = sum(1 for line in refined_lines if '**' in line or line.strip().startswith('#'))
        
        # Word count
        raw_words = len(raw_response.split())
        refined_words = len(refined_response.split())
        
        return {
            "structure_improvement": {
                "raw_bullets": raw_bullets,
                "refined_bullets": refined_bullets,
                "raw_numbered_lists": raw_numbered,
                "refined_numbered_lists": refined_numbered,
                "raw_sections": raw_sections,
                "refined_sections": refined_sections
            },
            "length": {
                "raw_words": raw_words,
                "refined_words": refined_words,
                "difference": refined_words - raw_words
            },
            "improvements": [
                "✅ Better structure" if refined_sections > raw_sections else None,
                "✅ More actionable points" if refined_bullets + refined_numbered > raw_bullets + raw_numbered else None,
                "✅ Organized sections" if refined_sections >= 3 else None,
                "✅ Professional formatting" if refined_sections > 0 else None
            ]
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_comparison_service = None


def get_comparison_service() -> Optional[AnswerComparisonService]:
    """
    Get or create singleton comparison service instance
    
    Returns:
        AnswerComparisonService instance or None if API key not available
    """
    global _comparison_service
    
    if _comparison_service is None:
        try:
            _comparison_service = AnswerComparisonService()
        except ValueError as e:
            st.warning(f"⚠️ Comparison service unavailable: {e}")
            return None
    
    return _comparison_service
