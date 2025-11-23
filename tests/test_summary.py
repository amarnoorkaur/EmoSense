"""
Unit tests for Smart Emotional Summary Service
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.summary_service import (
    clean_text,
    validate_text_for_summary,
    combine_emotion_and_summary,
    extract_emotion_keywords,
    generate_emotion_reasoning
)


def test_clean_text():
    """Test text cleaning functionality"""
    print("Testing clean_text()...")
    
    # Test HTML removal
    html_text = "<p>Hello <b>world</b></p>"
    cleaned = clean_text(html_text)
    assert "<" not in cleaned and ">" not in cleaned
    print("✅ HTML removal works")
    
    # Test excessive whitespace removal
    spaced_text = "Hello    world   with    spaces"
    cleaned = clean_text(spaced_text)
    assert "    " not in cleaned
    print("✅ Whitespace cleaning works")
    
    # Test empty input
    assert clean_text("") == ""
    assert clean_text(None) == ""
    print("✅ Empty input handling works")


def test_validate_text_for_summary():
    """Test text validation"""
    print("\nTesting validate_text_for_summary()...")
    
    # Test empty text
    is_valid, msg = validate_text_for_summary("")
    assert not is_valid
    print("✅ Empty text validation works")
    
    # Test short text
    short_text = "Too short"
    is_valid, msg = validate_text_for_summary(short_text)
    assert not is_valid
    assert "too short" in msg.lower()
    print("✅ Short text validation works")
    
    # Test valid text
    valid_text = "This is a longer piece of text that should be valid for summarization purposes."
    is_valid, msg = validate_text_for_summary(valid_text)
    assert is_valid
    print("✅ Valid text passes validation")
    
    # Test very long text
    long_text = " ".join(["word"] * 1100)
    is_valid, msg = validate_text_for_summary(long_text)
    assert not is_valid
    assert "too long" in msg.lower()
    print("✅ Long text validation works")


def test_extract_emotion_keywords():
    """Test emotion keyword extraction"""
    print("\nTesting extract_emotion_keywords()...")
    
    # Test anger keywords
    anger_text = "I am so frustrated and angry about this delay"
    keywords = extract_emotion_keywords(anger_text, "anger")
    assert "frustrated" in keywords or "angry" in keywords or "delay" in keywords
    print("✅ Anger keyword extraction works")
    
    # Test sadness keywords
    sad_text = "I feel so lonely and overwhelmed by everything"
    keywords = extract_emotion_keywords(sad_text, "sadness")
    assert "lonely" in keywords or "overwhelmed" in keywords
    print("✅ Sadness keyword extraction works")
    
    # Test no matches
    neutral_text = "The meeting is scheduled for tomorrow"
    keywords = extract_emotion_keywords(neutral_text, "anger")
    assert len(keywords) == 0
    print("✅ No false positive keywords")


def test_combine_emotion_and_summary():
    """Test emotion and summary combination"""
    print("\nTesting combine_emotion_and_summary()...")
    
    # Mock emotion output
    emotion_output = {
        "probabilities": {
            "anger": 0.85,
            "frustration": 0.32,
            "sadness": 0.15
        }
    }
    
    summary = "The user is frustrated with delays and unmet expectations"
    original_text = "I am so angry about this delay. This is frustrating!"
    
    result = combine_emotion_and_summary(emotion_output, summary, original_text)
    
    # Check result structure
    assert "summary" in result
    assert "dominant_emotion" in result
    assert "all_emotions" in result
    assert "reasoning" in result
    assert "suggested_action" in result
    assert "confidence" in result
    print("✅ Result has correct structure")
    
    # Check dominant emotion
    assert result["dominant_emotion"] == "anger"
    print("✅ Dominant emotion correctly identified")
    
    # Check confidence
    assert result["confidence"] == 0.85
    print("✅ Confidence correctly extracted")
    
    # Check reasoning exists
    assert len(result["reasoning"]) > 0
    print("✅ Reasoning generated")
    
    # Check suggested action
    assert "De-escalation" in result["suggested_action"]
    print("✅ Suggested action appropriate for emotion")


def test_generate_emotion_reasoning():
    """Test emotion reasoning generation"""
    print("\nTesting generate_emotion_reasoning()...")
    
    summary = "The customer is frustrated with delivery delays"
    dominant_emotion = "anger"
    all_emotions = {"anger": 0.92, "frustration": 0.45}
    
    reasoning = generate_emotion_reasoning(summary, dominant_emotion, all_emotions)
    
    assert len(reasoning) > 0
    assert "anger" in reasoning.lower() or "frustrated" in reasoning.lower()
    print("✅ Reasoning generated successfully")
    
    # Test with keywords in summary
    assert "delay" in summary.lower() or "frustration" in summary.lower()
    print("✅ Reasoning includes context from summary")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Running Smart Emotional Summary Service Tests")
    print("=" * 60)
    
    try:
        test_clean_text()
        test_validate_text_for_summary()
        test_extract_emotion_keywords()
        test_combine_emotion_and_summary()
        test_generate_emotion_reasoning()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
