from fastapi import APIRouter, Depends
from auth import verify_token

v1_router = APIRouter(prefix="/store/api/v1")

@v1_router.get("/me")
def get_user_info(user=Depends(verify_token)):
    return {
        "username": user["username"],
        "role": user["role"],
        "message": "Welcome to your Eddie Store!"
    }

# Example placeholder route for user-specific data
@v1_router.get("/dbs")
def list_databases(user=Depends(verify_token)):
    # Replace this with real per-user logic
    return {"dbs": [f"{user['username']}_vector_store"]}
