from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

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


class CompanyTokenSchema(BaseResponse):
    id: UUID
    company_id: UUID
    token: str
    created_at: datetime
    expired_at: datetime
        

class CompanySchema(BaseResponse):
    id: UUID
    name: str
    description: str
    email: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: datetime
    tokens: List[CompanyTokenSchema] = []

class CompanyBasicInfoRes(BaseResponse):
    id: UUID
    name: str
    description: str
    email: str
    is_verified: bool
    created_at: datetime

    
class VerifyResetPasswordCompanyReq(BaseModel):
    token: str
    email: EmailStr
    new_password: str
    
class getCompanyByIdReq(BaseModel):
    id: str
    
class getCompanyByNameReq(BaseModel):
    name: str
    
class getCompanyByEmailReq(BaseModel):
    email: EmailStr

class UpdateCompanyProfileReq(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
