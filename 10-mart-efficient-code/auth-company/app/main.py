from app.config.database import lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routes.user import router as user_router
from app.routes.company import router

app : FastAPI = FastAPI(lifespan=lifespan,servers=[{"url":"http://127.0.0.1:8002"}])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Company Auth soursecode"}

app.include_router(router)