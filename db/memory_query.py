# memory_query.py
from chroma_setup import get_collection

def query_memories(username: str, embedding: list[float], top_k: int = 5):
    collection = get_collection(username)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results
