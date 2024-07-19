from passlib import context
import base64

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_url(url: str) -> str:
    hashed_password = pwd_context.hash(url)
    return base64.urlsafe_b64encode(hashed_password.encode("utf-8")).decode("utf-8")
