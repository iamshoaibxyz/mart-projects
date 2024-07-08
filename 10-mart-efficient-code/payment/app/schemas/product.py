from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class ProductAddReq(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float

class ProductAddWithInventoryReq(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float
    stock: int

class ProductGetByIdReq(BaseModel):
    id: str

class ProductsGetByCompanyIdReq(BaseModel):
    id : str

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

class CompanyBasicInfoRes(BaseModel):
    id: UUID
    name: str
    description: str
    email: str
    is_verified: bool
    created_at: datetime

    
