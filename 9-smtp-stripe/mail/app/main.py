from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI(title="Mail SMTP Mart", servers=[{
    "url": "http://127.0.0.1:8005",
    "description": "Development server"
}])

class EmailSchema(BaseModel):
    email: list[EmailStr]
    subject: str
    body: str

# Step-by-Step Guide
# Generate an App Password:

# Go to your Google Account(https://myaccount.google.com/).
# Navigate to the "Security" tab.
# Under the "Signing in to Google" section, select "App passwords".
# Select the app and device you want to generate the password for and click "Generate".
# Copy the generated password (it will be a 16-character password).
# it look like "buob hhbk snsw nwer" replace with "YOUR_GENERATED_APP_PASSWORD"

conf = ConnectionConfig(
    MAIL_USERNAME = "your@gmail.com",
    MAIL_PASSWORD = "YOUR_GENERATED_APP_PASSWORD",
    MAIL_FROM = "your@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@app.post("/send-email")
async def send_email(email: EmailSchema, background_tasks: BackgroundTasks):
    await send_mail(email=email, background_tasks=background_tasks)
    return {"message": "Email has been sent"}

async def send_mail(email: EmailSchema, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,  # List of recipients, as many as you can pass
        body=email.body,
        subtype="html"
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
