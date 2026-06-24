# 🔧 dbt Knowledge Assistant

A RAG (Retrieval-Augmented Generation) powered chatbot that answers questions 
about dbt Core from a PDF knowledge base. Built as a portfolio project to 
demonstrate applied AI/ML engineering skills on top of a data engineering background.

---

## 🏗️ Architecture

User Question

↓

Streamlit UI

↓

FastAPI Backend

↓

ChromaDB Vector Search → Retrieve top 4 relevant chunks

↓

OpenAI GPT-3.5 → Generate answer grounded in retrieved context

↓

Answer + Source Citations

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| LLM | OpenAI GPT-3.5-turbo |
| Embeddings | OpenAI text-embedding-ada-002 |
| Vector Store | ChromaDB |
| Orchestration | LangChain |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Language | Python 3.14 |

---

## 📁 Project Structure


RAG/

├── data/                  # PDF knowledge base

├── src/

│   ├── ingest.py          # PDF ingestion pipeline

│   ├── retrieval.py       # Vector similarity search

│   ├── chat.py            # RAG chain + LLM logic

│   └── evaluate.py        # Evaluation framework

├── api.py                 # FastAPI backend

├── app.py                 # Streamlit frontend

├── chroma_db/             # Vector database (gitignored)

├── evaluation_results.json

├── requirements.txt

└── README.md


---

## 🚀 How to Run Locally

**1. Clone the repo:**
```bash
git clone <your-repo-url>
cd RAG
```

**2. Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Add your OpenAI API key:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

**5. Ingest the PDF:**
```bash
python src/ingest.py
```

**6. Start the API:**
```bash
uvicorn api:app --reload
```

**7. Start the UI (new terminal):**
```bash
streamlit run app.py
```

Open http://localhost:8501 and start asking questions.

---

## 📊 Evaluation Results

Built a custom evaluation framework testing 20 dbt questions 
with keyword-based answer verification.

| Metric | Score |
|---|---|
| Questions Passed | 17/20 |
| Overall Score | 85% |
| Rating | 🟢 Great |

**What was measured:**
- Answer relevancy — did the answer address the question
- Keyword accuracy — did the answer contain expected terminology
- Source citation — did the system return correct page references

**Failures analyzed:**
- 3 failures were keyword mismatches, not wrong answers
- 0 hallucinations detected on factual dbt questions
- Retrieval consistently returning relevant chunks

---

## 💡 What I Learned

- How vector embeddings represent meaning numerically
- Why chunk size and overlap matter for retrieval quality
- How to ground LLM answers in real documents to prevent hallucination
- How to separate frontend and backend in an AI application
- How to evaluate RAG systems beyond just "does it work"

---

## 🔄 What I Would Improve Next

- Add support for multiple PDFs
- Implement conversation memory across sessions
- Add Ragas evaluation once Python 3.14 wheels are available
- Fine-tune chunk size based on evaluation results
- Add user feedback mechanism to improve over time

---

## 👤 Author

Built by Srikanth Alokam — Data Engineer transitioning into ML/AI Engineering.

