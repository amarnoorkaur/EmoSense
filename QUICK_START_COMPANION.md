# Quick Start Guide - EmoSense Companion 2.0

## 🚀 Immediate Setup

### 1. Configure OpenAI API Key

**Option A: Environment Variable (Local Development)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Or add to system environment variables permanently
```

**Option B: Streamlit Secrets (Cloud Deployment)**
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-your-key-here"
```

### 2. Run the App
```bash
streamlit run App.py
```

### 3. Navigate to Personal Chatbot
Click **"Personal Chatbot"** in the sidebar (or **"💜 Personal Emotion Companion"** if using pages.toml)

---

## 💬 How to Test

### Test 1: Basic Conversation (No Emotion Analysis)
1. **Mode:** Casual Chat
2. **Personality:** Friendly
3. **Message:** "Hey! How's it going?"
4. **Click:** 💬 Send
5. **Expected:** Natural, friendly response without emotion chips

### Test 2: Reflective Mode (Auto Emotion Analysis)
1. **Mode:** Help Me Reflect
2. **Personality:** Deep Thinker
3. **Message:** "I'm feeling really stressed about work lately"
4. **Click:** 💬 Send
5. **Expected:** 
   - BERT analyzes emotions automatically
   - Response includes reflective questions
   - Emotion chips visible if "Show emotions" enabled

### Test 3: Crisis Detection
1. **Mode:** Comfort Me
2. **Personality:** Calm
3. **Message:** "I feel like I can't do this anymore. What's the point?"
4. **Click:** 💬 Send
5. **Expected:**
   - Immediate grounding response
   - Crisis hotline resources (988, Crisis Text Line)
   - Non-judgmental, supportive language

### Test 4: Explicit Emotion Analysis
1. **Mode:** Casual Chat (pure conversation mode)
2. **Message:** "I just got promoted and I'm so excited but also nervous!"
3. **Click:** 🔍 Analyze (instead of Send)
4. **Expected:**
   - Forces BERT emotion detection
   - Shows emotion chips (joy, anxiety, etc.)
   - LLM reflection on detected emotions

### Test 5: Conversation Memory
1. Send multiple messages in sequence:
   - "I had a tough day at work"
   - "My boss criticized my presentation"
   - "I'm starting to doubt myself"
2. **Expected:** 
   - Bot references previous messages naturally
   - Emotional trend detection kicks in (rising stress)
   - Response adjusts to softer, more supportive tone

### Test 6: Mode Switching
1. Send message in **Casual Chat** mode
2. Switch to **Hype Me Up** mode
3. Send another message
4. **Expected:** Completely different tone (enthusiastic, energizing)

### Test 7: Personality Switching
1. Send message with **Friendly** personality
2. Switch to **Big Sister** personality
3. Send another message about same topic
4. **Expected:** Different communication style (more protective, advice-oriented)

---

## 🎭 Mode Quick Reference

| Mode | Best For | Auto Emotion Analysis? |
|------|----------|------------------------|
| **Casual Chat** 💬 | General conversation | ❌ No (unless distress keywords) |
| **Comfort Me** 🤗 | Need support/validation | ❌ No (unless distress keywords) |
| **Help Me Reflect** 🤔 | Understanding emotions | ✅ Yes (auto-analyzes every message) |
| **Hype Me Up** 🔥 | Celebrating wins | ❌ No |
| **Just Listen** 👂 | Processing thoughts | ❌ No (minimal responses) |

---

## 🧪 Distress Keywords That Trigger Emotion Analysis

Even in "Casual Chat" mode, these keywords will trigger automatic BERT emotion detection:

**Emotional Distress:**
- sad, depressed, hopeless, worthless
- anxious, panic, scared, overwhelmed
- stressed, burned out, exhausted
- lonely, isolated, hurt, pain

**Crisis Keywords (Immediate Grounding Response):**
- want to die, suicidal, kill myself
- end it all, better off dead
- want to disappear, hurt myself

---

## 📊 Session State (Developer Reference)

```python
# Chat history (last 20 messages / 10 exchanges)
st.session_state.chat_history = [
    {"role": "user", "content": "...", "timestamp": "12:34 PM", "emotion_data": {...}},
    {"role": "assistant", "content": "...", "timestamp": "12:34 PM"}
]

# Emotion history (last 10 analyses)
st.session_state.emotion_history = [
    {"timestamp": datetime, "emotions": [...], "probabilities": {...}, "message": "..."}
]

# User preferences
st.session_state.conversation_mode = "Casual Chat"
st.session_state.bot_personality = "Friendly"
st.session_state.show_emotion_analysis = False
```

---

## 🐛 Troubleshooting

### "I need an OpenAI API key to chat with you"
**Solution:** Set `OPENAI_API_KEY` in environment variables or Streamlit secrets

### Bot responses are too similar/repetitive
**Solution:** This shouldn't happen with GPT-4o-mini. Check:
- API key is valid
- `frequency_penalty=0.3` in LLM service
- Temperature set to 0.8 for creativity

### Emotion analysis running on every message
**Solution:** Check conversation mode:
- Should only auto-analyze in "Help Me Reflect" mode
- Or when distress keywords detected
- Otherwise, click 🔍 Analyze button explicitly

### Chat history not persisting
**Solution:** This is expected (session-based storage)
- History clears when page reloads
- Last 20 messages retained during active session
- Click 🗑️ Clear to manually reset

### Emotion chips not showing
**Solution:** Enable "Show emotions" checkbox at top right

---

## 🎨 UI Customization (Optional)

### Change Chat Bubble Colors
Edit `Personal_Chatbot.py` CSS:

```css
/* User message gradient */
.message-user-chat {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Bot message background */
.message-bot-chat {
    background: rgba(138, 92, 246, 0.15);
    border: 1px solid rgba(138, 92, 246, 0.3);
}
```

### Adjust Chat Container Height
```css
.chat-container {
    max-height: 500px;  /* Change this value */
}
```

---

## 📱 User Instructions (For End Users)

**Share this with your users:**

### Welcome to EmoSense Companion! 💜

I'm your emotionally intelligent AI friend. Here's how we can chat:

**1. Pick How You Want to Talk:**
- 💬 **Casual Chat** - Just regular conversation
- 🤗 **Comfort Me** - Need extra support
- 🤔 **Help Me Reflect** - Understand your emotions
- 🔥 **Hype Me Up** - Celebrate your wins!
- 👂 **Just Listen** - I'll give you space

**2. Choose My Personality:**
- 🤝 **Friendly** - Warm and approachable
- 🧘 **Calm** - Tranquil and grounding
- 👩‍👧 **Big Sister** - Caring and protective
- 😄 **Funny** - Lighthearted with humor
- 🤔 **Deep Thinker** - Philosophical

**3. Start Chatting:**
- Type naturally, like texting a friend
- Click **💬 Send** to chat normally
- Click **🔍 Analyze** to check your emotions
- Toggle **Show emotions** to see emotion labels

**Important:**
- I'm here for support, but I'm not a therapist
- In crisis? I'll share helpline resources (988, Crisis Text Line)
- Your conversations are private (not stored permanently)

---

## ✅ What's Different from Before?

| Feature | Old Version | New Version |
|---------|-------------|-------------|
| **Style** | One-shot analysis | Continuous conversation |
| **Memory** | None | Last 10 exchanges remembered |
| **Responses** | Template-based | Natural AI (GPT-4o-mini) |
| **Emotion Detection** | Every message | Smart/selective |
| **Customization** | None | 5 modes × 5 personalities |
| **UI** | Two-column form | Chat bubbles |

---

## 🎯 Success Metrics

**How to know it's working well:**

✅ **Natural Conversation Flow**
- Bot references previous messages
- No repetitive phrases
- Responses feel human-like

✅ **Emotional Intelligence**
- Tone adjusts based on detected emotions
- Rising stress triggers softer responses
- Crisis keywords get immediate support

✅ **Mode Effectiveness**
- "Casual Chat" feels friendly and light
- "Comfort Me" is gentle and reassuring
- "Hype Me Up" is energetic and celebratory
- "Just Listen" gives brief, validating responses

✅ **Memory Persistence**
- Chat history visible after sending messages
- Last 10 exchanges retained (20 messages)
- Emotion history tracks patterns

---

## 🔐 Privacy & Security

**What's stored:**
- Session-based chat history (clears on page reload)
- Last 10 emotion analyses (temporary)
- No permanent database storage

**What's sent to OpenAI:**
- Last 10 conversation messages
- Current emotion context (if analysis ran)
- Mode and personality settings

**What's NOT stored:**
- User identity
- Conversation history beyond current session
- Personal information (unless user shares in messages)

---

## 📞 Support

**If something breaks:**
1. Check browser console for errors (F12)
2. Verify OPENAI_API_KEY is set correctly
3. Clear browser cache and reload
4. Check `PERSONAL_CHATBOT_UPGRADE.md` for detailed docs

**Common Issues:**
- API key not configured → Set environment variable
- Emotion analysis every message → Check mode (should be "Casual Chat")
- Bot not responding → Check API key validity
- UI looks broken → Hard refresh (Ctrl+Shift+R)

---

**Ready to test? Start with Test 1 (Basic Conversation) and work through all 7 tests!** 🚀
