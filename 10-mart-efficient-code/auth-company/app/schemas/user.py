from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class UserTokenSchema(BaseModel):
    id: UUID
    token: str
    created_at: datetime
    expired_at: datetime

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: datetime
    tokens: List[UserTokenSchema] = []

    class Config:
        orm_mode = True

class UserReq(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr

class VerifyResetPasswordUserReq(BaseModel):
    token: str
    email: EmailStr
    new_password: str

class UserRes(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    
class UserAccountVerifyReq(BaseModel):
    email: EmailStr
    token: str
    
class UserToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: str 
    # scope: str = "create"