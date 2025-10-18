# 🤖 AI Agent Library

> Professional-grade AI tools, prompts, and automations for real-world business applications

Welcome to my curated collection of production-ready AI solutions, battle-tested prompts, and intelligent automation workflows. These tools represent 30+ years of marketing expertise combined with cutting-edge AI technology.

---

## 🎯 What's Inside

This repository contains **production-ready AI tools** organized into three main categories:

### 📝 **Prompts** (`/prompts/`)
Advanced prompt engineering templates for ChatGPT, Claude, and other LLMs
- Multi-dimensional content analysis
- Hyper-personalized email generation
- LinkedIn intelligence extraction
- Business strategy analysis
- Content repurposing frameworks

### 🐍 **Python Scripts** (`/scripts/`)
Intelligent automation tools built with OpenAI API
- AI Content Analyzer with quality scoring
- Intelligent Email Response Generator
- Meeting Notes Processor with action item extraction
- Excel Q&A Translator with glossary support

### ⚡ **Automation Workflows** (`/automations/`)
n8n and Make.com workflow templates
- Lead enrichment pipelines
- Marketing automation sequences
- CRM data synchronization
- Multi-channel communication workflows

---

## 🚀 Featured Tools

### 1. **AI Content Analyzer** 
`/scripts/ai_content_analyzer.py`

Analyzes any content with multi-dimensional scoring across clarity, engagement, persuasiveness, readability, and SEO. Provides actionable recommendations for improvement.

**Use Cases:**
- Content audits and optimization
- Quality control for marketing copy
- SEO content evaluation
- Competitive analysis

**Features:**
- 6 quality dimensions scored 0-100
- Batch processing for content libraries
- Export to CSV for reporting
- Competitor comparison analysis

**Usage:**
```bash
python ai_content_analyzer.py --file article.txt --type blog-post
python ai_content_analyzer.py --batch content_folder/ --export report.csv
```

---

### 2. **Intelligent Email Responder**
`/scripts/email_responder.py`

Generates context-aware, professional email responses with intent analysis, urgency detection, and multi-tone support.

**Use Cases:**
- Customer support automation
- Sales correspondence
- Executive assistant workflows
- High-volume email management

**Features:**
- Automatic intent & sentiment analysis
- 5 tone options (professional, casual, empathetic, assertive, apologetic)
- Thread context awareness
- Batch email processing

**Usage:**
```bash
python email_responder.py --email incoming.txt --tone professional
python email_responder.py --batch inbox/ --export responses/
```

---

### 3. **Meeting Notes Processor**
`/scripts/meeting_notes_processor.py`

Transforms messy meeting notes or transcripts into structured summaries with automatic action item extraction and follow-up generation.

**Use Cases:**
- Meeting documentation
- Action item tracking
- Follow-up email generation
- JIRA/Linear ticket creation

**Features:**
- Extracts action items with owners & deadlines
- Identifies key decisions
- Generates follow-up emails
- Creates project management tickets
- Meeting effectiveness scoring

**Usage:**
```bash
python meeting_notes_processor.py --notes meeting.txt --format email
python meeting_notes_processor.py --transcript zoom.vtt --format jira
```

---

### 4. **Excel Q&A Translator**
`/scripts/translate_qna.py`

Bulk translation tool for Q&A datasets with glossary support and terminology control.

**Use Cases:**
- Multilingual content creation
- Knowledge base localization
- Training data preparation
- Customer support internationalization

**Features:**
- DeepL and OpenAI provider support
- Glossary-based terminology control
- Batch translation with failure logging
- Multi-language output in single Excel file

**Usage:**
```bash
python translate_qna.py --in questions.xlsx --question-col Q --answer-col A --targets it es de fr --out translations.xlsx
```

---

## 📚 Professional Prompt Templates

### **Hyper-Personalized Cold Email Generator**
`/prompts/cold_email_generator.md`

Production-ready prompt for B2B cold outreach that achieves 25%+ open rates and 8%+ response rates.

**Key Features:**
- Context-aware personalization using LinkedIn, tech stack, recent news
- Strict rules to avoid generic cold email mistakes
- Forces specific, verifiable details
- Eliminates buzzwords and clichés

---

### **LinkedIn Profile Intelligence Analyzer**
`/prompts/linkedin_analyzer.md`

Extracts actionable sales intelligence from LinkedIn profiles.

**What It Provides:**
- Pain point identification based on role and industry
- Personalization hooks for outreach
- Multi-channel conversation starters
- Outreach strategy recommendations

---

### **AI Business Analyst**
`/prompts/business_analyst.md`

Strategic decision support prompt using proven frameworks (5 Whys, ROI analysis, risk mitigation).

**Output Includes:**
- Root cause analysis
- Strategic options comparison
- Implementation roadmap with phases
- Success metrics and KPIs
- Resource requirements

---

### **Advanced Content Repurposing Engine**
`/prompts/content_repurposing.md`

Transforms one piece of content into 5 platform-optimized versions (LinkedIn, Twitter, Email, Instagram, YouTube).

**Key Benefits:**
- 5x content output efficiency
- Platform-specific optimization
- Algorithm-friendly formatting
- Engagement strategy included

---

## 🛠️ Setup & Requirements

### **Python Scripts Requirements**

```bash
# Install dependencies
pip install openai pandas rich python-dateutil webvtt-py deepl

# Set environment variable
export OPENAI_API_KEY="sk-your-key-here"
export DEEPL_API_KEY="your-deepl-key"  # For translation tool
```

### **General Requirements**
- Python 3.8+
- OpenAI API account
- (Optional) DeepL API for translation
- (Optional) n8n or Make.com for automation workflows

---

## 📊 Use Case Matrix

| Tool | Content Creation | Sales & Marketing | Operations | Support |
|------|-----------------|-------------------|------------|---------|
| Content Analyzer | ✅ Primary | ✅ Quality Control | ⚪ | ⚪ |
| Email Responder | ⚪ | ✅ Primary | ✅ Primary | ✅ Primary |
| Meeting Processor | ⚪ | ⚪ | ✅ Primary | ⚪ |
| Q&A Translator | ✅ Primary | ⚪ | ⚪ | ✅ Primary |
| Cold Email Prompts | ⚪ | ✅ Primary | ⚪ | ⚪ |
| LinkedIn Analyzer | ⚪ | ✅ Primary | ⚪ | ⚪ |
| Business Analyst | ⚪ | ✅ Strategic | ✅ Strategic | ⚪ |

---

## 💡 Best Practices

### **Prompt Engineering Principles**
1. ✅ **Be Specific** - Define exact output format and structure
2. ✅ **Provide Context** - Include all relevant information upfront
3. ✅ **Set Constraints** - Specify what NOT to do
4. ✅ **Use Examples** - Show the AI what good looks like
5. ✅ **Iterate** - Test, measure, refine based on results

### **Tool Usage Tips**
- **Start Small**: Test with single examples before batch processing
- **Monitor Costs**: Track API usage and set budget limits
- **Version Control**: Keep track of prompt versions that work
- **Error Handling**: Always review AI outputs before using in production
- **Customization**: Adapt prompts to your specific use case and brand voice

---

## 📈 Performance Metrics

**Measured Results from Production Use:**

| Tool | Metric | Result |
|------|--------|--------|
| Cold Email Prompt | Open Rate | 25-40% |
| Cold Email Prompt | Response Rate | 8-15% |
| Content Analyzer | Accuracy vs Human Review | 87% |
| Email Responder | Time Savings | 60%+ |
| Meeting Processor | Action Item Capture Rate | 95%+ |
| Q&A Translator | Cost per Prospect | ~$0.11 |

---

## 🎓 Learning Resources

**Want to learn more about AI automation?**

- 📚 [My 20-Week AI Agent Master Plan](https://www.notion.so/1f74805894588091ae79e11d2a10070a)
- 💼 [LinkedIn Profile](https://www.linkedin.com/in/aldeluca) - Connect with me
- 🌐 [BizzBrain.AI](https://bizzbrain.ai) - AI Development & Automation Services
- 📧 [Email Me](mailto:alessandro@carism.it) - Consulting & Collaboration

---

## 🤝 Contributing & Collaboration

### **How to Use These Tools**

1. **Clone or Download**: Get the tools you need
2. **Install Dependencies**: Follow setup instructions above
3. **Customize**: Adapt prompts and scripts to your use case
4. **Test**: Start with small batches
5. **Deploy**: Scale to production with confidence

### **Want to Collaborate?**

I'm open to:
- 💼 **Consulting Projects** - AI automation implementation
- 🎤 **Speaking Engagements** - AI adoption strategies
- 🤝 **Partnerships** - Integration and development
- 📚 **Training** - Team upskilling on AI tools

**Reach out:** [LinkedIn](https://www.linkedin.com/in/aldeluca) | [Email](mailto:alessandro@carism.it)

---

## 📂 Repository Structure

```
ai-prompts-library/
├── README.md
├── prompts/
│   ├── PROFESSIONAL_PROMPTS.md          # 4 advanced prompt templates
│   ├── cold_email_generator.md
│   ├── linkedin_analyzer.md
│   ├── business_analyst.md
│   └── content_repurposing.md
├── scripts/
│   ├── ai_content_analyzer.py           # Content quality scoring
│   ├── email_responder.py               # Intelligent email responses
│   ├── meeting_notes_processor.py       # Meeting summary automation
│   └── translate_qna.py                 # Bulk translation tool
└── automations/
    ├── n8n_workflows/
    └── make_scenarios/
```

---

## 🏆 About Me

**Alessandro De Luca**  
AI Solutions Architect | 30+ Years Marketing Veteran | Founder @ BizzBrain.AI

I've spent three decades in marketing and business strategy, and I've learned that the best technology is invisible—it just works. These tools represent that philosophy: powerful AI capabilities wrapped in practical, production-ready solutions.

**My Mission:** Make AI accessible, practical, and profitable for businesses of all sizes.

### **Portfolio Highlights**
- 🎯 Built CARISM SDR - Enterprise AI sales platform processing 10K+ prospects/month
- 📱 Published 2 apps on Apple App Store (BondQuest.AI, Momentum Flow pending)
- 🚀 Launched 9 production SaaS applications
- 🧠 Founded BizzBrain.AI - AI development and automation company
- 🎓 Certified in: LangChain, n8n, Make.com, Python, Prompt Engineering

---

##
