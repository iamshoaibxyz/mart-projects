from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.config.database import lifespan
from app.routes.product import router

app : FastAPI = FastAPI(lifespan=lifespan, title="product", servers=[{
    "url": "http://127.0.0.1:8004",
    "description": "Development server"
}])
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1:8005",],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "product soursecode"}

app.include_router(router)