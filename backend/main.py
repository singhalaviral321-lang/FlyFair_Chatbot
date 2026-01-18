"""
FlyFair Backend API
FastAPI application for RAG-based passenger rights chatbot.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path

from rag_service import RAGService
from llm_service import LLMService, LLMConfig
from answer_service import AnswerService


# Initialize FastAPI app
app = FastAPI(
    title="FlyFair API",
    description="RAG-based chatbot for Indian domestic air passenger rights",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).parent
CHUNKS_PATH = BASE_DIR / "rag" / "flyfair_rag_chunks.json"
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.txt"

# Initialize services (lazy loading)
rag_service: Optional[RAGService] = None
llm_service: Optional[LLMService] = None
answer_service: Optional[AnswerService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService(str(CHUNKS_PATH))
    return rag_service


def get_llm_service() -> Optional[LLMService]:
    """Get or create LLM service"""
    global llm_service
    if llm_service is None:
        try:
            config = LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "ollama"),
                base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434"),
                model_name=os.getenv("LLM_MODEL", "llama2"),
                timeout=float(os.getenv("LLM_TIMEOUT", "30.0"))
            )
            llm_service = LLMService(config)
            # Test connection
            llm_service.generate("Test", "Hello")
            print("LLM service initialized successfully")
        except Exception as e:
            print(f"LLM service initialization failed: {e}")
            print("Continuing without LLM (will use direct formatting)")
            llm_service = None
    return llm_service


def get_answer_service() -> AnswerService:
    """Get or create answer service"""
    global answer_service
    if answer_service is None:
        rag = get_rag_service()
        llm = get_llm_service()
        answer_service = AnswerService(rag, llm, str(SYSTEM_PROMPT_PATH))
    return answer_service



# Request/Response models
class QueryRequest(BaseModel):
    query: str
    use_llm: bool = False  # Default to False for RAG-only production mode


class QueryResponse(BaseModel):
    response: str
    chunks: list = []


# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "FlyFair API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_loaded": rag_service is not None,
        "llm_available": llm_service is not None
    }


# Main query endpoint
@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query endpoint for passenger rights questions.
    
    Args:
        request: Query request with user question
    
    Returns:
        Formatted response with passenger rights information
    """
    try:
        answer_service = get_answer_service()
        result = answer_service.answer(request.query, use_llm=request.use_llm)
        
        # If result is a dict with response key, return it
        if isinstance(result, dict) and "response" in result:
            return QueryResponse(**result)
        else:
            # Fallback
            return QueryResponse(
                response=result.get("response", "This is out of my Scope."),
                chunks=result.get("chunks", [])
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
