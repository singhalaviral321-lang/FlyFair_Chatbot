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
        """Load chunks from JSON file using absolute path"""
        chunks_path = os.path.abspath(self.chunks_path)

        if not os.path.exists(chunks_path):
            raise FileNotFoundError(f"RAG chunks file not found at: {chunks_path}")

        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        print(f"Loaded {len(self.chunks)} chunks from {chunks_path}")

    
    def _build_index(self):
        """
        Build FAISS index using search-optimized representations
        """
        texts = []

        for chunk in self.chunks:
            meta = chunk.get("metadata", {})
            searchable_text = f"""
            Category: {meta.get('category', '')}
            Scenario: {chunk.get('chunk_id', '')}
            Rule: {chunk.get('text', '')}
            """.strip()

            texts.append(searchable_text)

        self.embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # 🔑 USE COSINE DIRECTLY
        self.index.add(self.embeddings.astype("float32"))

        print(f"Built FAISS index with {self.index.ntotal} vectors")





    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            k
        )

        results = []
        for idx, score in zip(indices[0], scores[0]):
            chunk = self.chunks[idx].copy()
            chunk["similarity"] = float(score)
            results.append(chunk)

        return results


    
