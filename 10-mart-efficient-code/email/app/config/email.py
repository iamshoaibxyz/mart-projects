from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks, FastAPI
# Basic email related code
config = ConnectionConfig(
    MAIL_USERNAME="username", 
    MAIL_PASSWORD="12345", 
    MAIL_FROM="iamshoaib@test.com", 
    MAIL_FROM_NAME="Mart App", 
    MAIL_PORT=1025,
    MAIL_SERVER="smtpContainer",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=True
    )

fm = FastMail(config)

async def send_mail(email:str, html: str, subject: str = "Fastapi Mail Module"):
    message = MessageSchema(subject=subject, recipients=[email], body=html, subtype=MessageType.html,  )

    await fm.send_message(message)
    return {"email": "email has been sent!"}