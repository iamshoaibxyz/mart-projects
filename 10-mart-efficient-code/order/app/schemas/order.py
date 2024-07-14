from pydantic import BaseModel

class OrderReq(BaseModel):
    product_id: str
    quantity: int

class UserRes(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str
    
