# 🤖 AI-Powered Insights Guide

## Overview
EmoSense now includes AI-powered insights that automatically analyze bulk emotion analysis results and generate professional summaries with actionable recommendations.

## How to Use

### 1. Run Bulk Analysis
- Switch to **"📊 Bulk Analysis"** mode in the sidebar
- Upload a CSV file or paste comments
- Click **"🚀 Analyze All Comments"**

### 2. View Analytics Dashboard
After analysis completes, you'll see:
- Top 4 emotions with metric cards
- Bar chart of emotion distribution
- Pie chart showing percentages
- Detailed statistics table

### 3. Generate AI Insights
Scroll down to the **"🤖 AI-Powered Summary & Insights"** section:

#### First-time Setup
If you haven't configured your OpenAI API key yet:
1. Expand the "🔑 Configure OpenAI API Key" section
2. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
3. Enter the key (for local testing) OR add it to Streamlit secrets (for deployment)

#### Generate Insights
1. Click **"✨ Generate AI Insights"**
2. Wait for AI to analyze your data (~10-30 seconds)
3. Review the comprehensive report

## What's Included in AI Insights

The AI analysis provides:

### 📊 Overall Sentiment
General mood and tone assessment of all comments

### 🎯 Key Emotions
Analysis of dominant emotions and what they indicate about your audience

### ✅ Positive Signals
Encouraging patterns or emotions that show positive engagement

### ⚠️ Concerns
Negative emotions or warning signs that need attention

### 💡 Recommendations
3-4 actionable steps based on the emotional landscape

### 🚨 Priority Actions
Immediate actions to address critical issues or leverage opportunities

## Download Options

After generation, you can download:
- **CSV Results**: Raw emotion analysis data
- **AI Insights Report**: Formatted markdown report with all insights

## Cost & Model Information

- **Model Used**: GPT-4o-mini (cost-effective)
- **Estimated Cost**: ~$0.01-0.05 per analysis (depending on data size)
- **Processing Time**: 10-30 seconds depending on number of comments

## Configuration for Deployment

### Streamlit Cloud Setup
1. Go to your app settings on Streamlit Cloud
2. Click "Secrets" in the left menu
3. Add the following:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```
4. Save and reboot the app

### Local Development Setup
**Option 1: Environment Variable**
```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-api-key"

# Windows CMD
set OPENAI_API_KEY=sk-your-api-key

# Linux/Mac
export OPENAI_API_KEY=sk-your-api-key
```

**Option 2: Manual Entry**
Enter the key directly in the app interface (session only)

## Troubleshooting

### "Unable to Generate AI Summary" Error

**Possible causes:**
1. OpenAI API key not configured
2. Invalid API key
3. API rate limit exceeded
4. Network connection issue

**Solutions:**
1. Verify your API key is correctly entered
2. Check your OpenAI account has credits
3. Wait a few minutes if rate limited
4. Check internet connection

### API Key Security

⚠️ **Important Security Notes:**
- Never commit API keys to GitHub
- Use Streamlit secrets for deployment
- Manual entry is for testing only
- Rotate keys if accidentally exposed

## Example Use Cases

### Customer Feedback Analysis
Upload customer reviews/comments to identify:
- Overall satisfaction levels
- Common pain points
- Areas of delight
- Actionable improvements

### Social Media Monitoring
Analyze social media comments to:
- Gauge brand sentiment
- Identify trending emotions
- Respond to negative sentiment
- Capitalize on positive engagement

### Survey Response Analysis
Process open-ended survey responses to:
- Understand respondent emotions
- Identify key themes
- Generate executive summaries
- Prioritize follow-up actions

### Support Ticket Analysis
Evaluate support conversations to:
- Measure customer frustration
- Identify systemic issues
- Improve response strategies
- Track sentiment trends

## Tips for Best Results

1. **Clean Your Data**: Remove duplicates and irrelevant text before analysis
2. **Batch Size**: Analyze 50-500 comments for optimal insights
3. **Context**: Include representative samples from your target audience
4. **Threshold**: Use confidence threshold 0.3-0.5 for balanced results
5. **Review**: Always review AI insights alongside raw data

## Future Enhancements

Planned features:
- Custom prompts for industry-specific insights
- Comparison mode (before/after analysis)
- Trend tracking over time
- Integration with other AI models
- Scheduled analysis reports

---

**Need Help?**
- Report issues on [GitHub](https://github.com/amarnoorkaur/EmoSense/issues)
- Check the main [README.md](README.md) for general documentation
