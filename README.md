# 🎭 EmoSense - Emotion Analysis Chatbot

EmoSense is an AI-powered emotion analysis chatbot that uses a fine-tuned BERT model to detect and analyze emotions in text. Built with Streamlit, it provides an interactive chat interface that identifies up to 28 different emotions from the GoEmotions dataset.

## ✨ Features

- **Real-time Emotion Detection**: Analyze text and detect 28 different emotions including joy, anger, sadness, excitement, fear, love, and more
- **Interactive Chat Interface**: Conversational UI with chat bubbles and message history
- **Smart Emotional Summary** 🧠 NEW:
  - AI-powered text summarization using Hugging Face BART model
  - Combines emotion analysis with intelligent text summary
  - Emotion-based reasoning and keyword detection
  - Context-aware suggested actions for each emotion type
  - Export results as Markdown or JSON
  - Beautiful visual presentation with emotion breakdowns
- **Bulk Comment Analysis**: Upload CSV files or paste multiple comments for batch processing
- **Analytics Dashboard**: 
  - Top 4 emotions with metric cards
  - Bar charts showing emotion distribution
  - Pie charts for percentage breakdown
  - Detailed statistics table
  - Download results as CSV
- **AI-Powered Insights**:
  - Automated summary generation using OpenAI GPT
  - Sentiment overview and key emotion analysis
  - Identification of positive signals and concerns
  - Actionable recommendations based on emotional landscape
  - Priority actions for critical issues
  - Download AI insights as markdown report
- **Visual Analytics**: 
  - Colorful emotion chips with probability scores
  - Emoji representations for each emotion
- **Customizable Threshold**: Adjust confidence threshold to filter emotion predictions
- **Chat History**: Persistent conversation history during your session
- **Dark Theme**: Modern dark UI with gradient accents

## 🎯 Supported Emotions

The model can detect 28 emotions from the GoEmotions dataset:

admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral

## 🚀 How to Run Locally

### Prerequisites

- Python 3.8 or higher
- A trained BERT emotion model saved in `./emotion_bert_model/`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd emosense_backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure model files are in place**
   
   Make sure you have your trained BERT model in the `./emotion_bert_model/` directory with:
   - `config.json`
   - `pytorch_model.bin` (or `model.safetensors`)
   - `tokenizer_config.json`
   - `vocab.txt`

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The app will automatically open in your default browser at `http://localhost:8501`

## 🌐 Deploy on Streamlit Cloud

### Quick Deployment

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy the app**
   - Click "New app"
   - Select your repository
   - Choose the branch (usually `main`)
   - Set main file path: `app.py`
   - Click "Deploy"

### Important Notes for Deployment

⚠️ **Model Size Considerations**: 
- BERT models can be large (>400MB)
- Streamlit Cloud has storage and memory limits
- Consider using a smaller model or model compression techniques
- Alternatively, host the model externally (e.g., HuggingFace Hub) and load it via API

**Loading from HuggingFace Hub** (Alternative):
```python
# In utils/predict.py, replace MODEL_PATH with:
MODEL_PATH = "your-username/emotion-bert-model"  # Your HuggingFace model
```

## 📁 Project Structure

```
emosense_backend/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration (dark theme)
├── services/
│   └── summary_service.py     # Smart Emotional Summary service
├── components/
│   └── emotional_summary_card.py  # UI component for summary display
├── utils/
│   ├── predict.py             # Model loading and prediction logic
│   ├── labels.py              # Emotion labels and emoji mappings
│   ├── ai_summary.py          # AI-powered insights generation
│   └── mock_predict.py        # Mock predictions for testing
├── tests/
│   └── test_summary.py        # Unit tests for summary service
└── emotion_bert_model/        # Trained BERT model (not included in repo)
    ├── config.json
    ├── pytorch_model.bin
    └── tokenizer files
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **ML Framework**: PyTorch, Transformers (HuggingFace)
- **Emotion Model**: BERT fine-tuned on GoEmotions dataset (hosted on HuggingFace Hub)
- **Summarization Model**: BART (facebook/bart-large-cnn) via HuggingFace Inference API
- **AI Insights**: OpenAI GPT-4o-mini
- **Visualization**: Matplotlib
- **Data Processing**: Pandas
- **Language**: Python 3.8+

## 📊 How It Works

### Emotion Detection
1. User enters text in the chat interface or uploads bulk comments
2. Text is tokenized using BERT tokenizer
3. Model processes the input and outputs logits for 28 emotion classes
4. Sigmoid activation converts logits to probabilities
5. Emotions above the threshold are displayed with emojis and confidence scores
6. Results visualized as colorful chips, bar charts, and pie charts

### Smart Emotional Summary
1. User enters text (single or bulk input)
2. Text is cleaned and validated (10-1000 words)
3. Hugging Face BART model generates concise summary via Inference API
4. Emotion classifier analyzes the text simultaneously
5. Service combines results with intelligent reasoning:
   - Matches emotion keywords in summary
   - Generates context-aware explanations
   - Provides emotion-specific suggested actions
6. Beautiful UI card displays:
   - AI-generated summary
   - Dominant emotion with confidence
   - Full emotion probability breakdown
   - Reasoning and detected keywords
   - Suggested actions (de-escalation, grounding, etc.)
7. Export results as Markdown or JSON

### AI-Powered Insights
1. After bulk analysis, emotion data is aggregated
2. AI analyzes emotion distribution and sample comments
3. OpenAI GPT generates professional insights including:
   - Overall sentiment assessment
   - Key emotion patterns
   - Positive signals and concerns
   - Actionable recommendations
   - Priority actions for critical issues
4. Report can be downloaded as markdown

## ⚙️ Configuration

### Hugging Face API Key Setup

For Smart Emotional Summary, configure your Hugging Face API key:

**Option 1: Streamlit Cloud Secrets** (Recommended for deployment)
1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets" section
3. Add the following:
   ```toml
   HUGGINGFACE_API_KEY = "hf_your-api-key-here"
   ```

**Option 2: Local Development**
- Set environment variable: `$env:HUGGINGFACE_API_KEY="hf-your-key"` (Windows PowerShell)
- Or: `export HUGGINGFACE_API_KEY=hf-your-key` (Linux/Mac)

### OpenAI API Key Setup

For AI-powered insights, configure your OpenAI API key:

**Option 1: Streamlit Cloud Secrets** (Recommended for deployment)
1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets" section
3. Add the following:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```

**Option 2: Local Development**
- Set environment variable: `set OPENAI_API_KEY=sk-your-key` (Windows)
- Or enter the key directly in the app interface (session only)

**Option 3: Manual Entry**
- Use the expandable section in the app to enter your key temporarily

## 🎨 Customization

### Adjust Confidence Threshold
Use the sidebar slider to change the minimum probability required for an emotion to be displayed (default: 0.3)

### Modify Theme
Edit `.streamlit/config.toml` to customize colors and appearance

### Change Model
Update the `MODEL_ID` in `utils/predict.py` to use a different HuggingFace model

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 💡 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input for emotion analysis
- [ ] Export chat history
- [ ] Emotion trends over conversation
- [ ] API endpoint for integration

---

**Built with ❤️ using Streamlit and BERT**
