from datetime import datetime, timedelta, timezone
from app.config.settings import SECRET_TOKEN, TOKEN_EXPIRY, TOKEN_ALGROITHM
from passlib import context
from fastapi import HTTPException, status
import base64
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


def create_access_token(payload: dict):
    token_expiry = datetime.now(timezone.utc) + timedelta(minutes= float(TOKEN_EXPIRY) )
    to_encode = {"exp": token_expiry, "sub": payload} 
    return jwt.encode(to_encode, SECRET_TOKEN, TOKEN_ALGROITHM)

def decode_access_token(token: str):
    """
    Decodes a JWT access token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded token payload.

    Raises:
        HTTPException: If the token is expired, invalid, or any other JWT-related error occurs.
    """
    try:
        # Decode the token using the secret key and the specified algorithm
        return jwt.decode(token, SECRET_TOKEN, algorithms=[TOKEN_ALGROITHM])
    except jwt.ExpiredSignatureError as e:
        # Token has expired
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        # Token is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError as e:
        # General JWT error
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token error")
    except Exception as e:
        # Any other exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))