from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from app.config.settings import SECRET_TOKEN, TOKEN_EXPIRY, TOKEN_ALGROITHM
import base64
from passlib import context
import jwt

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")\


def hashed_password(plain_password: str):
    return pwd_context.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def hashed_url(url: str) -> str:
    hashed_password = pwd_context.hash(url)
    return base64.urlsafe_b64encode(hashed_password.encode("utf-8")).decode("utf-8")

def verify_hashed_url(db_url: str, user_url: str) -> bool:
    try:
        decoded_hashed = base64.urlsafe_b64decode(user_url).decode("utf-8")
        return pwd_context.verify(db_url, decoded_hashed)
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return False

# def verify_hashed_url(db_url: str, user_url: str):
#     try:
#         decoded_hashed = base64.urlsafe_b64decode(user_url).decode("utf-8")
#         return pwd_context.verify(db_url, decoded_hashed)
#     except Exception as e:
#         print(f"Error decoding token: {str(e)}")
#         return {"error": str(e)}

def create_access_token(payload: dict):
    token_expiry = datetime.now(timezone.utc) + timedelta(minutes= float(TOKEN_EXPIRY) )
    to_encode = {"exp": token_expiry, "sub": payload} 
    return jwt.encode(to_encode, SECRET_TOKEN, TOKEN_ALGROITHM)

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_TOKEN, algorithms=[TOKEN_ALGROITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except Exception as e:
        return {"error": str(e)}