
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.inventory import router
from app.config.database import lifespan

app : FastAPI = FastAPI(lifespan=lifespan, title="inventry", servers=[{
    "url": "http://127.0.0.1:8006",
    "description": "Development server"
}])

@app.get("/")
def root():
    return {"message": "inventry soursecode"}

@app.get("/me")
def root():
    return {"message": "Hey i am shoaib"}

app.include_router(router)