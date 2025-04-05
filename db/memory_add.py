# memory_add.py
from chroma_setup import get_collection
import uuid
from datetime import datetime

def add_memory(username: str, text: str, embedding: list[float], metadata: dict = None):
    collection = get_collection(username)

    metadata = metadata or {}
    metadata["timestamp"] = datetime.utcnow().isoformat()

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )

    return {"status": "ok", "username": username}
