"""
RAG Service for FlyFair
Handles loading chunks, creating embeddings, and retrieving relevant chunks.
"""
import json
import os
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class RAGService:
    """RAG service for retrieving relevant chunks from flyfair_rag_chunks.json"""
    
    def __init__(self, chunks_path: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG service.
        
        Args:
            chunks_path: Path to flyfair_rag_chunks.json
            model_name: Sentence transformer model name
        """
        self.chunks_path = chunks_path
        self.model = SentenceTransformer(
            model_name,
            device="cpu"
        )
        self.chunks: List[Dict] = []
        self.index = None
        self.embeddings = None
        self._load_chunks()
        self._build_index()
    
    def _load_chunks(self):
        """Load chunks from JSON file"""
        with open(self.chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        print(f"Loaded {len(self.chunks)} chunks from {self.chunks_path}")
    
    def _build_index(self):
        """Build FAISS index from chunk embeddings"""
        # Extract text from chunks
        texts = [chunk['text'] for chunk in self.chunks]
        
        # Generate embeddings
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings.astype('float32'))
        
        print(f"Built FAISS index with {self.index.ntotal} vectors")
    
    def retrieve(self, query: str, top_k: int = 3, threshold: float = 0.5) -> List[Dict]:
        """
        Retrieve top-k relevant chunks for a query.
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            List of relevant chunks with similarity scores
        """
        # Encode query
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        k = min(top_k, len(self.chunks))
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Convert distances to similarities (cosine similarity)
        similarities = 1 - distances[0]
        
        # Filter by threshold and return chunks
        results = []
        for i, (idx, sim) in enumerate(zip(indices[0], similarities)):
            if sim >= threshold:
                chunk = self.chunks[idx].copy()
                chunk['similarity'] = float(sim)
                results.append(chunk)
        
        return results
