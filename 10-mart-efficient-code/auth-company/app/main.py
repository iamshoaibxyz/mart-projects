from fastapi import FastAPI, Request
from app.config.database import lifespan
# from app.routes.user import router as user_router
from app.routes.company import router

app : FastAPI = FastAPI(lifespan=lifespan,servers=[{"url":"http://127.0.0.1:8002"}])

@app.get("/")
def root():
    return {"message": "Company Auth soursecode"}

app.include_router(router)