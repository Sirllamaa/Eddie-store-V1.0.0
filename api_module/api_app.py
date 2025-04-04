from fastapi import FastAPI
from api_module.v1_router import v1_router as v1_api_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    pass

app.include_router(v1_api_router)