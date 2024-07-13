from datetime import datetime
from typing import List, Optional
from uuid import UUID
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.all_models import ProductModel, StockLevel

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class ProductAddReq(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float

class ProductUpdateReq(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

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

class ProductModelSchema(BaseResponse):
    id: str | UUID
    name: str
    description: str
    price: float
    category: str
    company_id: str | UUID
    product_ranking: float
    created_at: datetime 
    updated_at: datetime 
    # company: Optional["CompanyModel"] = Relationship(back_populates="products")
    # comments: Optional[List["CommentModel"]] = Relationship(back_populates="product")
    # orders: Optional[List["OrderPlacedModel"]] = Relationship(back_populates="product")
    # transactions: Optional[List["InventoryTransactionSchema"]] 

class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"

class InventoryTransactionSchema(BaseResponse):
    id: str | UUID
    stock_id: str | UUID
    product_id: str | UUID
    quantity: int
    timestamp: datetime
    created_at: datetime 
    updated_at: datetime 
    product: ProductModel
    operation: Operation
    stock: Optional["StockLevel"] 
    product: Optional[ProductModel]

class StockLevelSchema(BaseResponse):
    id: UUID | str
    product_id: UUID | str
    current_stock: int 
    created_at: datetime 
    updated_at: datetime 
    # transactions: Optional[List[InventoryTransactionSchema]] 
    # product: Optional[ProductModel]

