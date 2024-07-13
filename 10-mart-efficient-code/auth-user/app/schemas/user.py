from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, constr, Field
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class UserTokenSchema(BaseResponse):
    id: UUID
    token: str
    created_at: datetime
    expired_at: datetime


class UserSchema(BaseResponse):
    id: UUID
    first_name: str 
    last_name: str
    email: str
    is_verified: bool
    verified_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: datetime
    tokens: List[UserTokenSchema] = []

class UpdataUserProfileReq(BaseResponse):
    first_name : str
    last_name : str
    email : EmailStr

class UserReq(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    # email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
    # @field_validator("email")
    # def validate_gmail(cls, v):
    #     if not v.endswith("@gmail.com"):
    #         raise ValueError("Only Gmail addresses are allowed")
    #     return v
    
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

class UserBasicInfoRes(BaseResponse):
    id: UUID
    first_name: str
    last_name: str
    email: str
    is_verified: bool 
    created_at: datetime

class GetUserByIdReq(BaseModel):
    id: str

class GetUserByEmailReq(BaseModel):
    email: str
    # email: EmailStr
