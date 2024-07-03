from pydantic import BaseModel

class UserReq(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

class UserRes(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str
    
