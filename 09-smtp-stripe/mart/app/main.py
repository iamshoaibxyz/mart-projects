from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.config.database import lifespan
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.order import router as order_router
from app.routes.product import router as product_router
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

app: FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8002/auth/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Message":"Mart API Sourcecode"}

app.include_router(product_router)
app.include_router(order_router)

