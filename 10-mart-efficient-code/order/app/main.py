from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.order import router
from app.config.database import lifespan

app : FastAPI = FastAPI(lifespan=lifespan, title="order", servers=[{
    "url": "http://127.0.0.1:8005",
    "description": "Development server"
}])
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1:8007",],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "order soursecode"}

app.include_router(router)
