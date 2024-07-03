
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config.database import lifespan

app : FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

@app.get("/")
def root():
    return {"message": "product soursecode"}

@app.get("/me")
def root():
    return {"message": "Hey i am shoaib"}