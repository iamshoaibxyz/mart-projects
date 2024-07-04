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