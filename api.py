from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chat import ask
from src.ingest import ingest_pdf
import os

app = FastAPI(
    title="dbt Knowledge Assistant API",
    description="RAG-powered API for querying dbt documentation",
    version="1.0.0"
)

# Request/Response models
class Message(BaseModel):
    role: str
    content: str

class QuestionRequest(BaseModel):
    question: str
    chat_history: list[Message] = []

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

class IngestRequest(BaseModel):
    pdf_path: str

# Routes
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "dbt Knowledge Assistant is running"}

@app.post("/chat", response_model=AnswerResponse)
def chat(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    history = [{"role": m.role, "content": m.content} for m in request.chat_history]
    result = ask(request.question, history)
    return AnswerResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

@app.post("/ingest")
def ingest(request: IngestRequest):
    if not os.path.exists(request.pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    ingest_pdf(request.pdf_path)
    return {"status": "success", "message": f"PDF ingested: {request.pdf_path}"}