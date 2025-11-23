# Enhanced AI Recommendations - Hybrid RAG+LLM System

## 🎯 Overview

The EmoSense app now features a **Hybrid Recommendation System** that combines:
- **Static Recommendations** (Fast, pre-written advice)
- **Enhanced AI Recommendations** (GPT-4 + Market Research)

## 🏗️ Architecture

### Mode 1: Fast Mode (Static)
```
User Input → BERT (Emotions) → BART (Summary) → Static Lookup → Recommendations
```
- ⚡ **Speed**: Instant
- 💰 **Cost**: Free (no API calls)
- 📊 **Quality**: Generic but relevant

### Mode 2: Enhanced AI Mode (RAG + LLM)
```
User Input → BERT → BART → RAG Search → GPT-4 → Custom Recommendations
                                ↓
                        Market Research DB
                        (ChromaDB + Embeddings)
```
- 🧠 **Speed**: 5-10 seconds
- 💰 **Cost**: ~$0.01-0.02 per analysis
- 📊 **Quality**: Personalized, data-driven

## 📁 Project Structure

```
emosense_backend/
├── services/
│   ├── rag_service.py                    # Vector database (ChromaDB)
│   ├── llm_recommendation_service.py     # GPT-4 integration
│   ├── summary_service.py                # Enhanced with RAG support
│   └── emotion_service.py                # BERT emotion detection
├── data/
│   └── market_research/                  # Research documents
│       ├── positive_sentiment_strategies.md
│       ├── negative_sentiment_crisis.md
│       └── viral_content_emotions.md
└── components/
    └── emotional_summary_card.py         # Enhanced UI display
```

## 🔧 How It Works

### Step 1: Document Ingestion (RAG)
```python
from services.rag_service import get_rag_service

rag = get_rag_service()
rag.ingest_documents_from_folder("./data/market_research")
```

**What happens:**
- Loads market research documents (.md, .txt)
- Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores in ChromaDB vector database
- Enables semantic search

### Step 2: Semantic Search
```python
research_context = rag.search_relevant_research(
    query=summary,           # Text summary from BART
    emotion=dominant_emotion, # e.g., "joy"
    n_results=3              # Top 3 relevant docs
)
```

**What happens:**
- Converts query to embedding vector
- Searches vector DB using cosine similarity
- Returns top 3 most relevant research snippets
- Includes metadata (source, relevance score)

### Step 3: LLM Generation
```python
from services.llm_recommendation_service import get_llm_service

llm = get_llm_service()
result = llm.generate_recommendation(
    summary=summary,
    dominant_emotion="joy",
    all_emotions={...},
    confidence=0.89,
    research_context=research_context  # Retrieved docs
)
```

**What happens:**
- Builds detailed prompt with emotion + research
- Calls GPT-4o-mini API
- Generates personalized recommendations
- References specific research studies

### Step 4: Display Results
```python
render_emotional_summary(combined_result)
```

**UI shows:**
- ✅ Summary
- ✅ Emotions
- ✅ AI-generated recommendations
- ✅ Research sources used (expandable)

## 📊 Market Research Documents

### 1. Positive Sentiment Strategies
**Focus:** Joy, Love, Gratitude, Admiration, Excitement
**Key Insights:**
- Response time: 1-2 hours = 67% higher engagement
- UGC campaigns: 4.5x reach increase
- Referral programs: 23% conversion rate

### 2. Negative Sentiment Crisis
**Focus:** Anger, Sadness, Fear, Disappointment
**Key Insights:**
- First 60 minutes critical
- 45% angry customers → advocates with fast response
- De-escalation language patterns

### 3. Viral Content Emotions
**Focus:** Multi-emotion content performance
**Key Insights:**
- Joy + Surprise: 412% share rate
- Admiration + Curiosity: 387% CTR
- Emotion diversity → higher engagement

## 🎛️ User Interface

### Toggle Enhanced Mode
```python
use_enhanced_ai = st.checkbox(
    "🤖 Enable Enhanced AI Recommendations",
    value=False
)
```

**When enabled:**
- Shows: "🤖 AI-Generated Strategic Recommendations"
- Displays: "Powered by GPT-4 + Market Research Database"
- Includes: Research sources expandable section

**When disabled:**
- Shows: "🎯 Recommended Business Actions"
- Uses: Pre-written static recommendations
- Fast: Instant results

## 💡 Adding Your Own Research

### Method 1: Add Markdown Files
```bash
# Create new file
cd data/market_research
nano your_research.md

# Structure:
# Research Title
## Key Findings
- Insight 1
- Insight 2
## Data Points
- Statistic 1
- Statistic 2
```

### Method 2: Programmatic Ingestion
```python
from services.rag_service import get_rag_service

rag = get_rag_service()

rag.ingest_document(
    text="Your research content here...",
    metadata={
        "filename": "custom_research.md",
        "category": "engagement",
        "source": "internal_study",
        "date": "2024-11"
    },
    doc_id="research_001"
)
```

### Method 3: Clear and Rebuild
```python
rag = get_rag_service()
rag.clear_collection()  # Remove all documents
rag.ingest_documents_from_folder("./data/market_research")
```

## 🔑 API Keys Required

### For Enhanced Mode:
```bash
# .env or Streamlit secrets
OPENAI_API_KEY=sk-proj-xxxxx
HUGGINGFACE_API_KEY=hf_xxxxx  # Already required
```

### Cost Estimation:
- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Average analysis**: 500 input + 300 output = ~$0.01-0.02
- **1000 analyses**: ~$10-20

## 🚀 Performance Optimization

### 1. Caching
```python
@st.cache_resource
def get_rag_service():
    return MarketResearchRAG()

@st.cache_resource
def get_llm_service():
    return LLMRecommendationService()
```

**Benefits:**
- Vector DB loaded once per session
- LLM client reused
- Embedding model cached

### 2. Fallback Handling
```python
try:
    # Enhanced AI
    llm_result = llm.generate_recommendation(...)
except Exception as e:
    # Fallback to static
    suggested_action = EMOTION_ACTIONS.get(dominant_emotion)
```

**Benefits:**
- Never fails completely
- Graceful degradation
- User always gets recommendations

### 3. Lazy Loading
```python
if use_enhanced_ai:
    # Only load RAG/LLM when needed
    rag = initialize_rag_with_defaults()
```

**Benefits:**
- Fast mode stays fast
- No unnecessary API calls
- Reduced memory usage

## 📈 Future Enhancements

### Planned Features:
1. **Custom Research Upload** - Users upload their own PDFs/docs
2. **Multi-language Support** - Research in different languages
3. **Industry-Specific Databases** - E-commerce, SaaS, B2B
4. **A/B Testing** - Compare static vs. enhanced recommendations
5. **Analytics Dashboard** - Track recommendation performance
6. **Fine-tuned Models** - Custom emotion → action mappings

### Potential Upgrades:
- Switch to `gpt-4o` for higher quality (higher cost)
- Add `claude-3-sonnet` as alternative
- Use `text-embedding-3-large` for better search
- Implement hybrid search (keyword + semantic)

## 🐛 Troubleshooting

### Issue: "No documents in collection"
**Solution:**
```python
from services.rag_service import initialize_rag_with_defaults
rag = initialize_rag_with_defaults()
print(rag.get_collection_stats())
```

### Issue: "OpenAI API key not found"
**Solution:**
```bash
# Add to .env
OPENAI_API_KEY=sk-proj-xxxxx

# Or Streamlit secrets
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-proj-xxxxx"
```

### Issue: "ChromaDB persistence error"
**Solution:**
```bash
# Delete and recreate
rm -rf ./data/chroma_db
# Restart app to reinitialize
```

## 📚 References

- **ChromaDB**: https://www.trychroma.com/
- **Sentence Transformers**: https://www.sbert.net/
- **OpenAI GPT-4o-mini**: https://platform.openai.com/docs/models
- **LangChain**: https://python.langchain.com/

## 🎓 Learning Resources

### Understanding RAG:
1. What is RAG? Vector search + LLM generation
2. Why embeddings? Semantic similarity vs keyword matching
3. How ChromaDB works? HNSW algorithm for fast search

### Understanding Prompts:
1. System prompt: Expert role definition
2. Context injection: Research snippets + emotion data
3. Output formatting: Structured business recommendations

---

**Built with ❤️ for EmoSense - Smart Social Media Analytics**
