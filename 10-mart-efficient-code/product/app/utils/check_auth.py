from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from app.config.security import decode_access_token
from app.models.all_models import CompanyModel

def auth_checker(session: Session, token: str):
    try:
        decoded_token = decode_access_token(token)
        company_id = decoded_token.get("sub").get("id")        
        company = session.get(CompanyModel, UUID(company_id))
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))