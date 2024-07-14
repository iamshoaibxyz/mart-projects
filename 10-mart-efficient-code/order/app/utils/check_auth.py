from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from app.config.security import decode_access_token
from app.models.all_models import UserModel

def user_auth_checker(session: Session, token: str):
    try:
        decoded_token = decode_access_token(token)
        user_id = decoded_token.get("sub").get("id")
        user = session.get(UserModel, UUID(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))