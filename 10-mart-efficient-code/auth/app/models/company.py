from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship, TEXT
from typing import Optional, List, ForwardRef
from uuid import UUID, uuid4
from datetime import datetime
from app.models.product import ProductModel

class CompanyModel(SQLModel, table=True):
    __tablename__ = 'company'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = Field(sa_column=TEXT)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    tokens: Optional[List["CompanyTokenModel"]] = Relationship(ForwardRef("CompanyTokenModel") ,back_populates="company")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    products: Optional[List["ProductModel"]] = Relationship(ForwardRef("ProductModel") ,back_populates="company")

    def get_context_str(self):
        return f"{"PASSWORD_CONTEXT"}{self.password[-7:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"
    

class CompanyTokenModel(SQLModel, table=True):
    __tablename__ = "company_token"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    company_id: Optional[UUID] = Field(None, foreign_key="company.id")
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False )
    expired_at: datetime = Field(nullable=False) 
    company: Optional["CompanyModel"] = Relationship(ForwardRef("CompanyModel") ,back_populates="tokens")
