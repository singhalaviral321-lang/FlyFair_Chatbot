from rag_service import RAGService
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = BASE_DIR / "rag" / "flyfair_rag_chunks.json"

rag = RAGService(str(CHUNKS_PATH))

query = "My domestic flight in India is delayed by 3 hours. What are my rights?"

results = rag.retrieve(query, top_k=5)

print("\nRETRIEVAL RESULTS:")
for r in results:
    print("----")
    print("chunk_id:", r.get("chunk_id"))
    print("similarity:", r.get("similarity"))
    print("text:", r.get("text"))
