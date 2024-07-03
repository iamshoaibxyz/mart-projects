from pydantic import BaseModel
from datetime import datetime
from app.models import OrderStatus

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderUpdate(BaseModel):
    status: OrderStatus

class OrderRead(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
