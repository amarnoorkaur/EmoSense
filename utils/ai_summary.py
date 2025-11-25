"""
AI-powered summary generation using OpenAI API
"""
import os
from openai import OpenAI
import pandas as pd

def generate_ai_summary(results_df, api_key=None):
    """
    Generate AI-powered insights from emotion analysis results
    
    Args:
        results_df: DataFrame with columns ['Comment', 'Primary Emotion', 'Confidence']
        api_key: OpenAI API key (optional, will use env var if not provided)
    
    Returns:
        str: Markdown-formatted AI summary
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        
        # Prepare emotion statistics
        emotion_counts = results_df['Primary Emotion'].value_counts()
        total_comments = len(results_df)
        avg_confidence = results_df['Confidence'].mean()
        
        # Get top comments for each emotion category
        top_emotions = emotion_counts.head(5)
        
        # Build structured prompt
        emotion_summary = "\n".join([f"- {emotion}: {count} comments ({count/total_comments*100:.1f}%)" 
                                      for emotion, count in top_emotions.items()])
        
        sample_comments = []
        for emotion in top_emotions.index[:3]:
            samples = results_df[results_df['Primary Emotion'] == emotion]['Comment'].head(2).tolist()
            if samples:
                sample_comments.append(f"\n{emotion.upper()}:")
                for i, comment in enumerate(samples, 1):
                    # Truncate long comments
                    comment_text = comment[:150] + "..." if len(comment) > 150 else comment
                    sample_comments.append(f"  {i}. \"{comment_text}\"")
        
        prompt = f"""Analyze the following emotion analysis results and provide professional insights:

OVERALL STATISTICS:
- Total Comments Analyzed: {total_comments}
- Average Confidence: {avg_confidence:.1%}

EMOTION DISTRIBUTION:
{emotion_summary}

SAMPLE COMMENTS:
{"".join(sample_comments)}

Please provide a comprehensive summary with:
1. **Overall Sentiment** - General mood and tone assessment
2. **Key Emotions** - Analysis of dominant emotions and what they indicate
3. **Positive Signals** - Encouraging patterns or emotions detected
4. **Concerns** - Negative emotions or warning signs
5. **Recommendations** - 3-4 actionable steps based on the emotional landscape
6. **Priority Actions** - Immediate actions to address critical issues

Format the response in clear markdown with headers and bullet points."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective model
            messages=[
                {"role": "system", "content": "You are an expert emotional intelligence analyst providing professional insights from sentiment analysis data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return the summary
        summary = response.choices[0].message.content
        return summary
        
    except Exception as e:
        return f"""### ⚠️ Unable to Generate AI Summary

**Error:** {str(e)}

**Possible Causes:**
- OpenAI API key not configured
- API rate limit exceeded
- Network connection issue

**How to Fix:**
1. Set your OpenAI API key in Streamlit secrets or environment variables
2. For Streamlit Cloud: Add `OPENAI_API_KEY` to your app secrets
3. For local development: Set `OPENAI_API_KEY` environment variable

**Manual Analysis Tips:**
Based on the data shown above:
- Review the emotion distribution chart to identify dominant emotions
- Focus on high-frequency negative emotions that may need attention
- Consider the confidence scores - higher confidence indicates clearer sentiment
- Look for patterns in the top emotions across your comments
"""
    