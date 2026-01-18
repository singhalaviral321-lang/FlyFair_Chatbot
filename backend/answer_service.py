"""
Answer Service for FlyFair
Handles query processing, retrieval, and response formatting.
"""
import os
from typing import List, Dict, Optional
from rag_service import RAGService
from llm_service import LLMService


class AnswerService:
    """Service for generating answers from RAG chunks"""
    
    OUT_OF_SCOPE_RESPONSE = "This is out of my Scope."
    RELEVANCE_THRESHOLD = 0.5
    
    def __init__(self, rag_service: RAGService, llm_service: Optional[LLMService], system_prompt_path: str):
        """
        Initialize answer service.
        
        Args:
            rag_service: RAG service instance
            llm_service: LLM service instance (can be None)
            system_prompt_path: Path to system prompt file
        """
        self.rag_service = rag_service
        self.llm_service = llm_service
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
    
    def answer(self, query: str, use_llm: bool = True) -> Dict[str, str]:
        """
        Answer a user query.
        
        Args:
            query: User query
            use_llm: Whether to use LLM for formatting (if False, returns raw chunk)
        
        Returns:
            Dictionary with formatted response or out-of-scope message
        """
        # Retrieve relevant chunks
        chunks = self.rag_service.retrieve(
            query, 
            top_k=3, 
            threshold=self.RELEVANCE_THRESHOLD
        )
        
        # If no relevant chunks, return out-of-scope
        if not chunks:
            return {
                "response": self.OUT_OF_SCOPE_RESPONSE,
                "chunks": []
            }
        
        # Get the most relevant chunk
        top_chunk = chunks[0]
        
        # If LLM is available and requested, use it to format the response
        if use_llm and self.llm_service is not None:
            try:
                formatted_response = self._format_with_llm(query, top_chunk)
                return {
                    "response": formatted_response,
                    "chunks": chunks
                }
            except Exception as e:
                print(f"LLM formatting failed: {e}, using direct formatting")
                # Fallback to direct formatting
                return self._format_direct(top_chunk)
        else:
            return self._format_direct(top_chunk)
    
    def _format_with_llm(self, query: str, chunk: Dict) -> str:
        """Format response using LLM"""
        user_prompt = f"""User Query: {query}

Retrieved Chunk:
{chunk['text']}

Metadata:
- Category: {chunk['metadata']['category']}
- Source: {chunk['metadata']['source']}
- Page: {chunk['metadata'].get('page', 'N/A')}

Format the response EXACTLY as:
Applicable Scenario:
[Extract the scenario from the chunk text]

Conditions:
[Extract the conditions from the chunk text]

Passenger Rights:
[Extract the rights from the chunk text]

Source:
{chunk['metadata']['source']} – {chunk['metadata']['category']}"""
        
        response = self.llm_service.generate(self.system_prompt, user_prompt)
        return response.strip()
    
    def _format_direct(self, chunk: Dict) -> Dict[str, str]:
        """Format response directly from chunk without LLM"""
        text = chunk['text']
        metadata = chunk['metadata']

        # RAG-only formatting must use ONLY retrieved text (no added wording).
        # Best-effort split: "If <conditions>, <rights>."
        lower_text = text.lower()
        sep = lower_text.find(", the ")
        if sep == -1:
            sep = lower_text.find(", passenger ")

        if sep != -1:
            conditions = text[:sep].strip()
            rights = text[sep + 1 :].strip()
        else:
            conditions = text
            rights = text

        # Keep "Applicable Scenario" as verbatim chunk text for safety.
        response = f"""Applicable Scenario:
{text}

Conditions:
{conditions}

Passenger Rights:
{rights}

Source:
{metadata['source']} – {metadata['category']}"""
        
        return {
            "response": response,
            "chunks": [chunk]
        }
