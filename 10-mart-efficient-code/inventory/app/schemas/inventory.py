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

class InventoryTransactionSchema(BaseResponse):
    id: str | UUID
    stock_id: str | UUID
    product_id: str | UUID
    quantity: int
    timestamp: datetime
    operation: str

class StockLevelSchema(BaseResponse):
    id: UUID | str
    product_id: UUID | str
    current_stock: int 
    created_at: datetime 
    updated_at: datetime 

