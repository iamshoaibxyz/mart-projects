from pydantic import BaseModel
from uuid import UUID

class OrderReq(BaseModel):
    product_id: UUID
    quantity: int


class ProductOrder(BaseModel):
    product_id: UUID
    quantity: int

class UserRes(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str
    
class MultiOrderReq(BaseModel):
    orders: list[OrderReq]