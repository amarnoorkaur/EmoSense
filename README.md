# 🎭 EmoSense - Emotion Analysis Chatbot

EmoSense is an AI-powered emotion analysis chatbot that uses a fine-tuned BERT model to detect and analyze emotions in text. Built with Streamlit, it provides an interactive chat interface that identifies up to 28 different emotions from the GoEmotions dataset.

## ✨ Features

- **Real-time Emotion Detection**: Analyze text and detect 28 different emotions including joy, anger, sadness, excitement, fear, love, and more
- **Interactive Chat Interface**: Conversational UI with chat bubbles and message history
- **Visual Analytics**: 
  - Colorful emotion chips with probability scores
  - Bar charts showing top detected emotions
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
├── utils/
│   ├── predict.py             # Model loading and prediction logic
│   └── labels.py              # Emotion labels and emoji mappings
└── emotion_bert_model/        # Trained BERT model (not included in repo)
    ├── config.json
    ├── pytorch_model.bin
    └── tokenizer files
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **ML Framework**: PyTorch, Transformers (HuggingFace)
- **Model**: BERT fine-tuned on GoEmotions dataset
- **Language**: Python 3.8+

## 📊 How It Works

1. User enters text in the chat interface
2. Text is tokenized using BERT tokenizer
3. Model processes the input and outputs logits for 28 emotion classes
4. Sigmoid activation converts logits to probabilities
5. Emotions above the threshold are displayed with emojis and confidence scores
6. Results visualized as colorful chips and bar charts

## 🎨 Customization

### Adjust Confidence Threshold
Use the sidebar slider to change the minimum probability required for an emotion to be displayed (default: 0.3)

### Modify Theme
Edit `.streamlit/config.toml` to customize colors and appearance

### Change Model
Replace the model in `emotion_bert_model/` directory or update the `MODEL_PATH` in `utils/predict.py`

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
