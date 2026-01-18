"""
Answer Service for FlyFair
Handles query processing, retrieval, and response formatting.
"""
import os
from typing import List, Dict, Optional
from rag_service import RAGService
from llm_service import LLMService
import re


class AnswerService:
    """Service for generating answers from RAG chunks"""
    
    OUT_OF_SCOPE_RESPONSE = "This is out of my Scope."
    RELEVANCE_THRESHOLD = 0.38  # Lowered to capture queries with noisy words like airline names
    
    def __init__(self, rag_service: RAGService, llm_service: Optional[LLMService], system_prompt_path: str):
        """
        Initialize answer service.
        """
        self.rag_service = rag_service
        self.llm_service = llm_service
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
    
    def answer(self, query: str, use_llm: bool = True) -> Dict[str, str]:
        """
        Answer a user query.
        """
        # Retrieve a larger set for re-ranking
        raw_chunks = self.rag_service.retrieve(query, top_k=10)

        chunks = [
            c for c in raw_chunks
            if c.get("similarity", 0) >= self.RELEVANCE_THRESHOLD
        ]
        
        if not chunks:
            return {
                "response": self.OUT_OF_SCOPE_RESPONSE,
                "chunks": []
            }
        
        # 1. Selection logic: Find the best single chunk to format
        top_chunk = self._select_best_chunk(chunks, query)
        
        if use_llm and self.llm_service is not None:
            try:
                # 2. Provide the LLM with context of multiple chunks to help it decide
                # but it will still format the 'best' one.
                formatted_response = self._format_with_llm(query, chunks[:3], top_chunk)
                return {
                    "response": formatted_response,
                    "chunks": chunks
                }
            except Exception as e:
                print(f"LLM formatting failed: {e}, using direct formatting")
                return self._format_direct(top_chunk)
        else:
            return self._format_direct(top_chunk)


    def _select_best_chunk(self, chunks: list, query: str) -> dict:
        """
        Heuristic-based re-ranking to prioritize general rules over exceptions.
        """
        import re
        q = query.lower()

        # Weighted scoring for each chunk
        scored_chunks = []
        for c in chunks:
            score = c.get("similarity", 0)
            text = c["text"].lower()
            cid = c.get("chunk_id", "").lower()

            # --- Rule 1: Category Matching ---
            is_delay_q = any(w in q for w in ["delay", "wait", "late", "hours"])
            is_cancel_q = any(w in q for w in ["cancel", "booked", "inform"])
            is_denied_q = any(w in q for w in ["denied", "boarding", "overbook"])

            cat = c['metadata'].get('category', '')
            if is_delay_q and cat == 'Flight Delay': score += 0.2
            if is_cancel_q and cat == 'Flight Cancellation': score += 0.2
            if is_denied_q and cat == 'Denied Boarding': score += 0.2

            # --- Rule 2: Anti-Exception Bias ---
            # Most users ask about general rights. Chunks that describe "No compensation" 
            # or "Exception" should only be picked if the query has specific exception keywords.
            negative_keywords = ["not payable", "not liable", "no compensation", "except", "extraordinary", "weather", "atc"]
            is_negative_chunk = any(w in text or w in cid for w in negative_keywords)
            
            positive_keywords = ["shall be entitled", "shall be paid", "shall provide", "shall be offered", "shall receive", "shall be compensated"]
            is_positive_chunk = any(w in text for w in positive_keywords)
            
            exception_query_keywords = ["weather", "storm", "rain", "atc", "traffic", "security", "force majeure"]
            has_exception_query = any(w in q for w in exception_query_keywords)
            
            if is_negative_chunk and not has_exception_query:
                score -= 0.5  # Heavy penalty for negative/exception chunks in general queries
            
            if is_positive_chunk:
                score += 0.2  # Slight boost for positive entitlements

            # --- Rule 3: Precise Duration Match ---
            # Use regex for hours to be precise
            hours_match = re.search(r'(\d+)\s*(?:h(?:ou)?rs?)', q)
            if hours_match:
                h = int(hours_match.group(1))
                if h >= 6 and "six hours" in text: score += 0.6
                if h >= 2 and h < 6 and "two hours" in text and "meal" in text: score += 0.6
                
                # If query mentions a specific hour, avoid 72-hour notice chunks unless it's a 72-hour query
                if h < 24 and "seventy-two" in text: score -= 0.6
                if h < 24 and "twenty-four" in text: score -= 0.4


            scored_chunks.append((score, c))

        # Sort by the new heuristic score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return scored_chunks[0][1]

    
    def _format_with_llm(self, query: str, context_chunks: List[Dict], best_chunk: Dict) -> str:
        """Format response using LLM with context awareness"""
        context_text = "\n\n".join([f"Option {i+1}:\n{c['text']}" for i, c in enumerate(context_chunks)])
        
        user_prompt = f"""User Query: {query}

I have retrieved several possible chunks. Based on the query, the most likely relevant chunk is:
CHUNK TO FORMAT:
{best_chunk['text']}

OTHER CONTEXT:
{context_text}

Metadata of CHUNK TO FORMAT:
- Category: {best_chunk['metadata']['category']}
- Source: {best_chunk['metadata']['source']}
- Page: {best_chunk['metadata'].get('page', 'N/A')}

Task: Use the CHUNK TO FORMAT to answer the query according to the system rules. 
If the CHUNK TO FORMAT doesn't perfectly match but is the best available, focus on its literal content.
If the query is blocked by words like 'indigo', ignore the airline name and focus on the flight status.

Format the response EXACTLY as:
Applicable Scenario:
[...]
Conditions:
[...]
Passenger Rights:
[...]
Source:
[...]"""
        
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
