# 🌱 ESG Risk Intelligence Assistant

An AI-powered chatbot that analyzes ESG (Environmental, Social, Governance) reports, assesses risks, and provides real-time sustainability insights.

## 🎯 Features

- **RAG (Retrieval-Augmented Generation)**: Upload ESG PDFs and query specific sections
- **Live Web Search**: Get latest ESG regulations and news
- **ESG Risk Scoring**: Automated keyword-based scoring across E, S, G categories
- **Response Modes**: Toggle between Concise and Detailed analysis
- **Smart Analysis**: Identifies strengths, risks, and compliance gaps

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.1)
- **Embeddings**: Transformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS
- **Web Search**: DuckDuckGo API
- **PDF Processing**: PyPDF2

## 📁 Project Structure
```
AI_USECASE/
├── config/
│   └── config_example.py      # Configuration template
├── models/
│   ├── llm.py                # LLM management
│   └── embeddings.py         # Text embeddings
├── utils/
│   ├── pdf_processor.py      # PDF extraction
│   ├── rag_engine.py         # Vector search
│   ├── web_search.py         # Web search
│   └── esg_scorer.py         # ESG scoring logic
├── app.py                    # Main Streamlit app
├── requirements.txt
└── README.md
```

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AI_USECASE
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get free Groq API key: https://console.groq.com/

### 4. Run the application
```bash
streamlit run app.py
```

## 📊 How to Use

1. **Upload ESG Report**: Upload a PDF in the sidebar
2. **Calculate Score**: Click "Calculate ESG Score" button
3. **Ask Questions**: Type queries about the report
4. **Web Search**: Enable for latest ESG news and regulations

## 💡 Example Queries

- "Analyze the ESG risks in this report"
- "What is the carbon emission reduction target?"
- "Calculate score" - Get automated ESG risk assessment
- "What are the latest ESG regulations in 2025?"

## 🎓 Use Case Objective

Help organizations understand and comply with ESG requirements by:
- Automating ESG report analysis
- Identifying compliance gaps
- Providing risk assessments
- Tracking latest regulations

## 🏆 Key Achievements

- ✅ RAG integration with FAISS vector store
- ✅ Real-time web search for current information
- ✅ Automated ESG scoring algorithm
- ✅ Concise/Detailed response modes
- ✅ Clean, modular code architecture

## 🔗 Live Demo

[Streamlit Cloud Link - Add after deployment]

## 👨‍💻 Developer

[Your Name]