from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import lifespan
from app.routes.user import router as user_router

app : FastAPI = FastAPI(lifespan=lifespan,servers=[{"url":"http://127.0.0.1:8001"}])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8007","http://127.0.0.1:8005"],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Auth user soursecode"}

app.include_router(user_router)
