from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class CompanyReq(BaseModel):
    name: str
    description: str
    email: EmailStr
    password: str

class VerifyCompanyReq(BaseModel):
    email: EmailStr
    password: str

class CompanyTokenReq(BaseModel):
    email: EmailStr
    token: str

class CompanyToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: str 


class CompanyTokenSchema(BaseModel):
    id: UUID
    company_id: UUID
    token: str
    created_at: datetime
    expired_at: datetime

    class Config:
        orm_mode = True

class CompanySchema(BaseModel):
    id: UUID
    name: str
    description: str
    email: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: datetime
    tokens: List[CompanyTokenSchema] = []

    class Config:
        orm_mode = True
class VerifyResetPasswordCompanyReq(BaseModel):
    token: str
    email: EmailStr
    new_password: str

class UpdateCompanyProfileReq(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
