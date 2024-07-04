from fastapi import FastAPI
from app.config.database import lifespan
from app.routes.user import router as user_router
from app.routes.company import router as company_router

app : FastAPI = FastAPI(lifespan=lifespan,servers=[{"url":"http://127.0.0.1:8001"}])

# @app.get("/")
# def root():
#     return {"message": "Auth soursecode"}

app.include_router(user_router)

# app.include_router(company_router)