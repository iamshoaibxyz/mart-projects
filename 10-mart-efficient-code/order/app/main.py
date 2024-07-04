
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app : FastAPI = FastAPI(title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8005",
    "description": "Development server"
}])

@app.get("/")
def root():
    return {"message": "order soursecode"}

@app.get("/me")
def root():
    return {"message": "Hey i am shoaib"}