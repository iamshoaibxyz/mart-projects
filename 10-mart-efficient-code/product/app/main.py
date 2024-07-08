from fastapi import FastAPI
from app.config.database import lifespan
from app.routes.product import router

app : FastAPI = FastAPI(lifespan=lifespan, title="product", servers=[{
    "url": "http://127.0.0.1:8004",
    "description": "Development server"
}])

@app.get("/")
def root():
    return {"message": "product soursecode"}

@app.get("/me")
def root():
    return {"message": "Hey i am shoaib"}

app.include_router(router)