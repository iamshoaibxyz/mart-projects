import resend
from typing import Dict
from fastapi import FastAPI
from app.config.database import lifespan
# from app.config.settings import RESEND_API_Key

# resend.api_key = "re_123456789"

app : FastAPI = FastAPI(lifespan=lifespan, servers=[{"url":"http://127.0.0.1:8002"}])

@app.get("/")
def root():
    return {"message": "Email soursecode"}

# @app.post("/")
# def send_mail() -> Dict:
#     params: resend.Emails.SendParams = {
#         "from": "onboarding@resend.dev",
#         "to": ["iamshoaibxyz@gmail.com"],
#         "subject": "Hello World",
#         "html": "<strong>it works!</strong>",
#     }
#     email: resend.Email = resend.Emails.send(params)
#     return email