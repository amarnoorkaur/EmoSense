# EmoSense AI - Complete Glassmorphic Redesign

## 🎨 Design System Overview

### Color Palette
- **Background:** `#0E0F14` (Deep dark)
- **Glass Cards:** `rgba(255, 255, 255, 0.05)` with `backdrop-filter: blur(10px)`
- **Primary Gradient:** `linear-gradient(135deg, #8A5CF6, #C06CFF)`
- **Text Primary:** `#FFFFFF`
- **Text Secondary:** `#A8A9B3`
- **Accent Colors:**
  - Teal: `#00C4CC`
  - Pink: `#FB7185`
  - Yellow: `#FFD166`

### Typography
- **Font Family:** Inter, system-ui, sans-serif
- **Hero Titles:** 2.5rem, bold, gradient text
- **Section Headers:** 1.5rem, bold, white
- **Body Text:** 1rem, #A8A9B3

### Components
- **Border Radius:** 24px for cards, 50px for buttons
- **Glass Effect:** `backdrop-filter: blur(10px)`, 1px white border at 6% opacity
- **Animations:** fadeIn (0.6s), pulse (2s infinite), smooth transitions with cubic-bezier
- **Shadows:** Soft lifts on hover (0 8px 32px rgba(138, 92, 246, 0.3))

---

## 📁 File Structure

```
emosense_backend/
├── app.py                           # ✅ NEW: Landing page with gradient hero
├── components/
│   ├── layout.py                    # ✅ NEW: Global design system (400+ lines CSS)
│   ├── footer.py                    # ✅ NEW: Glass footer with newsletter
│   └── emotional_summary_card.py    # Existing (used in business chatbot)
├── pages/
│   ├── personal_chatbot.py          # ✅ REDESIGNED: Warm chat interface
│   ├── business_chatbot.py          # ✅ REDESIGNED: Complete business logic
│   ├── about.py                     # ✅ REDESIGNED: Four clean cards
│   └── terms_and_conditions.py      # ✅ REDESIGNED: Expander layout
├── utils/                           # Existing ML utilities
├── services/                        # Existing AI services
└── data/                            # Newsletter subscribers, etc.
```

---

## 🚀 Pages Overview

### 1. Landing Page (`app.py`)
**Components:**
- Gradient hero: "EmoSense AI" with subtitle
- Two CTA buttons: "💛 Personal Companion" & "📊 Business Intelligence"
- Two feature cards: For Individuals vs For Businesses
- "How It Works" 3-card row: 🧠 Detect, 🧾 Understand, 🚀 Act
- Technology showcase: BERT, BART, GPT-4, RAG badges
- Stats metrics: 28 emotions, 9 categories, 6+ sources
- Glass footer with newsletter signup

**Navigation:**
- Personal button → `st.switch_page("pages/personal_chatbot.py")`
- Business button → `st.switch_page("pages/business_chatbot.py")`

---

### 2. Personal Chatbot (`pages/personal_chatbot.py`)
**Features:**
- **Two-column layout:**
  - **Left:** Text area (input), Dropdown (analysis type), Analyze button
  - **Right:** Chat bubbles (user gradient, AI glass), emotion chips, timestamps
- **Analysis Options:**
  - "Just label my emotions"
  - "Help me reflect on this"
  - "Suggest gentle coping ideas"
- **Context-aware AI responses** based on detected emotions
- **Session history** with clear button
- **Safety disclaimer** about mental health support

**Styling:**
- Warm, cozy microcopy
- `.message-user` class (gradient background, right-aligned)
- `.message-ai` class (glass background, left-aligned)
- Emotion chips below AI messages

---

### 3. Business Chatbot (`pages/business_chatbot.py`)
**Features:**
- **Three modes** in sidebar:
  - 💬 **Chat Mode:** Single message analysis with emotion charts
  - 📊 **Bulk Analysis:** CSV upload or paste comments, analyze at scale
  - 🧠 **Smart Summary:** Social media analytics with category detection
  
- **Chat Mode:**
  - Text area input
  - Emotion chips display
  - Top 5 emotions bar chart
  - Session history

- **Bulk Analysis:**
  - Upload CSV or paste text
  - Auto-detect comment column
  - Progress bar during analysis
  - Results table with download CSV
  - **Analytics Dashboard:**
    - Top 4 dominant emotions (metrics)
    - Summary narrative
    - Bar chart & pie chart (matplotlib with dark theme)
    - Detailed stats table
  - **AI-Powered Insights:**
    - OpenAI API integration
    - Generate comprehensive report
    - Download as Markdown

- **Smart Summary Mode:**
  - Text area for social media comments
  - **Category Detection** (BART-MNLI): 9 categories with confidence
  - **Emotion Analysis** (BERT)
  - **Summarization** (BART/PEGASUS)
  - **RAG Recommendations** (Optional GPT-4 + ChromaDB)
  - **Business Report Downloads:**
    - Markdown report with executive summary
    - JSON export for analytics tools
  - **Metrics:**
    - Positive/negative sentiment scores
    - Brand health status
    - Response priority

**All ML Logic Preserved:**
- Full 904 lines from `app_backup.py` extracted
- BERT emotion detection (28 emotions)
- BART-MNLI category classification (9 categories)
- BART/PEGASUS summarization
- GPT-4 + RAG recommendations
- ChromaDB vector database integration

---

### 4. About Page (`pages/about.py`)
**Structure:**
- Gradient hero: "About EmoSense AI"
- **Card 1 - What is EmoSense?**
  - Mission statement
  - 6 key features (28 emotions, smart summarization, category detection, AI insights, bulk analysis, RAG)
- **Card 2 - Who is it for?**
  - 6 audience types: Individuals, Creators, Brands, CX Teams, Researchers, HR
  - Bullet points for each use case
- **Card 3 - How Technology Works**
  - BERT emotion detection explanation
  - BART/PEGASUS summarization details
  - BART-MNLI category detection
  - GPT-4 + RAG architecture
  - Integration pipeline diagram (ASCII art)
  - Privacy & security info
- **Card 4 - Built by Amarnoor Kaur**
  - Vision statement
  - Background
  - Contact info (email, LinkedIn, GitHub)
  - Collaboration CTA
  - Special thanks section

**All wrapped in `section_card()` with icons**

---

### 5. Terms & Conditions (`pages/terms_and_conditions.py`)
**Structure:**
- Gradient hero: "📜 Terms & Conditions"
- Last updated note in glass card
- **7 Expanders:**
  - ⚖️ **Use of Platform** - Permitted use, prohibited activities, account responsibility
  - 🛡️ **Privacy & Data Handling** - What we process, third-party services, GDPR/CCPA compliance
  - 🤖 **AI Output Limitations** - Not medical advice, accuracy disclaimers, bias awareness, responsible use
  - ⛔ **Prohibited Activities** - Harm, privacy violations, system abuse, illegal activities
  - 📉 **Limitation of Liability** - "As is" service, no warranty, indemnification, force majeure
  - 📝 **Modifications to Terms** - Right to modify, notification process, version history
  - ✉️ **Contact & Dispute Resolution** - Contact info, mediation, arbitration, governing law
- Acknowledgment card at bottom

---

## 🎨 Global Design System (`components/layout.py`)

### Functions

#### `set_page_config()`
Sets unified page configuration:
- Title: "EmoSense AI - Emotion Analysis"
- Icon: 🎭
- Layout: wide
- Sidebar: expanded

#### `inject_global_styles()`
Injects comprehensive CSS (400+ lines):
- **Base styles:** #0E0F14 background, #FFFFFF text, Inter font
- **Glass cards:** rgba(255,255,255,0.05), backdrop-filter blur(10px), 24px radius, hover lift
- **Gradient hero:** Linear gradient (#8A5CF6 to #C06CFF), pulse animation, relative positioning
- **Buttons:** Primary (gradient, hover lift, 50px radius), Secondary (ghost style)
- **Emotion chips:** Glass background, color-coded borders (joy yellow, sadness teal, anger pink)
- **Chat bubbles:**
  - `.message-user` - gradient right-aligned
  - `.message-ai` - glass left-aligned
- **Inputs:** Glass background, focus glow (#8A5CF6)
- **Scrollbar:** Custom purple gradient thumb
- **Metrics:** Glass background, gradient value text
- **Expanders:** Glass with hover glow
- **Animations:** fadeIn (0.6s), pulse (2s infinite)

#### `page_container()`
Returns `st.container()` after calling `inject_global_styles()`

#### `gradient_hero(title, subtitle)`
Creates gradient bar with:
- Large title text (2.5rem)
- Subtitle (1.125rem, #A8A9B3)
- Pulse animation
- Responsive padding

#### `section_card(title, icon, body_fn)`
Creates glass card with:
- Header bar (gradient accent border)
- Icon + title (1.5rem bold)
- Body content via callback function
- Automatic padding and spacing

#### `emotion_chip(emotion, score, emoji)`
Returns HTML for emotion chip:
- Glass background
- Emoji + emotion label
- Score percentage
- Color-coded border (joy/sadness/anger variants)

#### `spacer(size="md")`
Creates vertical spacing:
- "sm": 1rem
- "md": 2rem
- "lg": 3rem

---

## 🦶 Footer Component (`components/footer.py`)

### `render_footer()`
**Layout:**
- Two-column glass card
- **Left column:**
  - "EmoSense AI" title
  - "Built with ❤️ by Amarnoor Kaur" subtitle
- **Right column:**
  - Email link (purple)
  - LinkedIn link (purple)
  - Newsletter signup:
    - Text input (glass style)
    - "✨ Notify Me" button
- Horizontal rule divider
- Copyright text

### `save_subscriber(email)`
Saves newsletter email to `data/newsletter_subscribers.json`

---

## 🧠 ML Features Preserved

### Emotion Detection
- **Model:** `j-hartmann/emotion-english-distilroberta-base`
- **Emotions:** 28 fine-grained labels
- **Threshold:** User-adjustable (0.1-0.9, default 0.3)
- **Output:** List of emotions with probabilities

### Summarization
- **Models:** `facebook/bart-large-cnn`, `google/pegasus-xsum`
- **Purpose:** Condense long feedback
- **Used in:** Bulk analysis, Smart summary mode

### Category Detection
- **Model:** `facebook/bart-large-mnli`
- **Categories:** 9 types (Product Reviews, Customer Support, Social Media, Marketing, HR, etc.)
- **Method:** Zero-shot classification

### AI Recommendations
- **Model:** `gpt-4o-mini` via OpenAI API
- **Enhanced Mode:** ChromaDB RAG with market research
- **Fast Mode:** Pre-defined recommendations

---

## ✅ Design Consistency Checklist

All pages follow this pattern:
1. `set_page_config()` - Unified configuration
2. `inject_global_styles()` - CSS injection
3. `page_container()` - Main wrapper
4. `gradient_hero(title, subtitle)` - Hero section
5. Content in glass cards (`.glass-card` class or `section_card()`)
6. `render_footer()` - Footer at bottom

**Color consistency:**
- Background: #0E0F14
- Glass cards: rgba(255,255,255,0.05)
- Gradient: #8A5CF6 to #C06CFF
- Text: #FFFFFF primary, #A8A9B3 secondary
- Accents: #00C4CC teal, #FB7185 pink, #FFD166 yellow

**Typography:**
- Inter font throughout
- Consistent heading hierarchy (h1: 2.5rem, h2: 2rem, h3: 1.5rem)

**Spacing:**
- Cards have 2rem padding
- Sections separated by `spacer("md")` (2rem)
- Large gaps with `spacer("lg")` (3rem)

---

## 🚀 Deployment Notes

### Running Locally
```bash
streamlit run app.py
```

### Environment Variables
- `HUGGINGFACE_API_KEY` - For BART summarization (optional, can use local models)
- `OPENAI_API_KEY` - For GPT-4 recommendations (optional, fast mode available)

### Configuration
Located in `.streamlit/config.toml`:
- Dark theme enabled
- Primary color: #8A5CF6 (purple)
- Background: #0E0F14
- Secondary background: #1A1B23

### Performance
- BERT model runs locally (first load takes ~5-10 seconds)
- BART summarization can use local or API mode
- ChromaDB runs on server (no external calls)
- GPT-4 is optional (only for enhanced recommendations)

---

## 🎯 User Experience Enhancements

### Navigation
- Clear CTAs on landing page
- `st.switch_page()` for seamless routing
- Sidebar visible on all pages

### Feedback
- Loading spinners for all AI operations
- Success/error messages with icons
- Progress bars for bulk analysis

### Accessibility
- High contrast (#FFFFFF on #0E0F14)
- Clear button states (hover, active)
- Readable font sizes (1rem minimum)
- Semantic HTML structure

### Responsive Design
- `max-width: 1400px` on main container
- Fluid columns with st.columns()
- Mobile-friendly spacing

---

## 📊 Testing Checklist

✅ **Landing Page:**
- [x] Gradient hero renders correctly
- [x] CTA buttons navigate to correct pages
- [x] Feature cards display all bullets
- [x] "How It Works" cards render
- [x] Tech showcase badges visible
- [x] Footer newsletter signup works

✅ **Personal Chatbot:**
- [x] Two-column layout renders
- [x] Text area accepts input
- [x] Dropdown has 3 options
- [x] Analyze button triggers emotion detection
- [x] Chat bubbles display correctly (user right, AI left)
- [x] Emotion chips show below AI messages
- [x] Clear history button works
- [x] Session state persists across reruns

✅ **Business Chatbot:**
- [x] Three modes in sidebar radio
- [x] **Chat Mode:** Input, analyze, display chips and chart
- [x] **Bulk Analysis:** Upload CSV, auto-detect column, analyze all
- [x] Analytics dashboard: Top 4, charts, stats table
- [x] AI insights generate and download
- [x] **Smart Summary:** Text input, category detection, summarization
- [x] RAG recommendations (with/without GPT-4)
- [x] Download reports (MD and JSON)

✅ **About Page:**
- [x] Four section cards render
- [x] All content displays correctly
- [x] Icons show in card headers
- [x] Links are styled correctly

✅ **Terms & Conditions:**
- [x] Seven expanders render
- [x] Content displays when expanded
- [x] Icons show in expander labels
- [x] Acknowledgment card at bottom

✅ **Footer:**
- [x] Two-column layout renders
- [x] Links work (email, LinkedIn)
- [x] Newsletter input accepts email
- [x] "Notify Me" button saves to JSON

✅ **Global:**
- [x] No Python errors
- [x] CSS loads on all pages
- [x] Navigation works between all pages
- [x] Theme consistent across all pages

---

## 🔮 Future Enhancements

1. **User Accounts** - Save history, track analytics over time
2. **API Integration** - Provide REST API for developers
3. **Multi-language Support** - Emotion detection in Spanish, French, etc.
4. **Advanced Charts** - D3.js interactive visualizations
5. **Export Options** - PDF reports, PowerPoint slides
6. **Real-time Analysis** - Webhook integrations for social media
7. **Mobile App** - Native iOS/Android emotion companion
8. **Voice Input** - Speech-to-text + emotion detection

---

## 📝 Changelog

### Version 5.0 (Current) - Complete Glassmorphic Redesign
- ✨ NEW: Glassmorphic design system with 400+ lines of CSS
- ✨ NEW: Gradient hero component with pulse animation
- ✨ NEW: Glass footer with newsletter signup
- 🔄 REDESIGNED: Landing page with emotional CTAs and feature showcase
- 🔄 REDESIGNED: Personal chatbot with warm chat interface
- 🔄 REDESIGNED: Business chatbot with complete logic (904 lines) + glassmorphic UI
- 🔄 REDESIGNED: About page with four clean section cards
- 🔄 REDESIGNED: Terms & Conditions with organized expanders
- 🗑️ REMOVED: Old main.py (using native Streamlit multipage)
- 🗑️ REMOVED: Outdated landing_page.py
- 🎨 THEME: Dark mode (#0E0F14) with purple gradients (#8A5CF6 to #C06CFF)
- 🔧 COMPONENTS: Emotion chips, chat bubbles, glass cards, gradient buttons

### Version 4.0 (Previous)
- Added Terms & Conditions page
- Multi-page architecture with routing

### Version 3.0
- Added Smart Summary mode with category detection
- Integrated RAG recommendations

### Version 2.0
- Added bulk analysis mode
- CSV upload functionality

### Version 1.0
- Initial release with chat mode
- BERT emotion detection

---

## 🙏 Credits

- **BERT Model:** `j-hartmann/emotion-english-distilroberta-base` from Hugging Face
- **BART Model:** `facebook/bart-large-cnn` from Meta AI
- **PEGASUS Model:** `google/pegasus-xsum` from Google Research
- **GPT-4:** OpenAI API
- **UI Framework:** Streamlit
- **Design Inspiration:** Glassmorphism trend, Apple design language
- **Color Palette:** Custom gradient (#8A5CF6 to #C06CFF)
- **Icons:** Unicode emojis
- **Font:** Inter by Rasmus Andersson

---

## 📧 Support

For questions, issues, or feature requests:
- **Email:** support@emosense.ai
- **GitHub Issues:** [Create an issue](https://github.com/amarnoorkaur/emosense-backend/issues)
- **Documentation:** This README

---

**Built with 💜 by Amarnoor Kaur**  
*Making emotional intelligence accessible through AI*
