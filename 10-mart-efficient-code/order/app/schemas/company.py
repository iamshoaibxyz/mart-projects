from pydantic import BaseModel

class CompanyReq(BaseModel):
    name: str
    description: str
    email: str
    password: str
