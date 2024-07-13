from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class InventoryAddReq(BaseModel):
    product_id: str
    quantity: int

class InventorySubtractReq(BaseModel):
    product_id: str
    quantity: int

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
    inventories: Optional[List["InventoryTransactionSchema"]] 

class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"

class InventoryTransactionSchema(BaseResponse):
    id: str | UUID
    stock_id: str | UUID
    product_id: str | UUID
    quantity: int
    timestamp: datetime
    operation: Operation
    # stock: Optional["StockLevelSchema"] 
    # product: Optional[ProductModelSchema]

class StockLevelSchema(BaseResponse):
    id: UUID | str
    product_id: UUID | str
    current_stock: int 
    created_at: datetime 
    updated_at: datetime 
    transactions: Optional[List[InventoryTransactionSchema]] 
    # product: Optional[ProductModelSchema]

