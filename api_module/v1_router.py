from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from auth import verify_token
from db.chroma_setup import get_collection, list_collections

v1_router = APIRouter(prefix="/store/api/v1")

@v1_router.get("/me")
def get_user_info(user=Depends(verify_token)):
    return {
        "username": user["sub"],
        "role": user["role"],
        "message": "Welcome to your Eddie Store!"
    }

@v1_router.get("/verify-token")
def secure_data(user_info: dict = Depends(verify_token)):
    return {
        "message": "Token is valid",
        "user": user_info
    }
    
class MemoryInput(BaseModel):
    username: str
    text: str
    embedding: List[float]
    metadata: Optional[dict] = None

class QueryInput(BaseModel):
    username: str
    embedding: List[float]
    top_k: int = 5

class RemoveInput(BaseModel):
    username: str
    ids: List[str]

@v1_router.post("/memory/add")
def add_memory(mem: MemoryInput, user=Depends(verify_token)):
    collection = get_collection(mem.username)
    metadata = mem.metadata or {}
    metadata["timestamp"] = datetime.utcnow().isoformat()

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[mem.text],
        embeddings=[mem.embedding],
        metadatas=[metadata]
    )
    return {"status": "ok", "username": mem.username}

@v1_router.post("/memory/query")
def query_memory(query: QueryInput, user=Depends(verify_token)):
    collection = get_collection(query.username)
    results = collection.query(
        query_embeddings=[query.embedding],
        n_results=query.top_k
    )
    return results

@v1_router.get("/memory/dbs")
def get_memory_dbs(user=Depends(verify_token)):
    return {"collections": list_collections()}

@v1_router.post("/memory/remove")
def remove_memories(data: RemoveInput, user=Depends(verify_token)):
    collection = get_collection(data.username)
    try:
        collection.delete(ids=data.ids)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok", "removed": data.ids}

@v1_router.delete("/memory/user/{username}")
def delete_user_memory(username: str, user=Depends(verify_token)):
    if user["sub"] != username and user["role"] != "system":
        raise HTTPException(status_code=403, detail="You can only delete your own memory.")

    from db.chroma_setup import client
    try:
        client.delete_collection(name=f"{username}_memory")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "ok", "message": f"Deleted memory for user '{username}'"}