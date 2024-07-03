from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from app.models.comment import CommentModel
from app.models.order import OrderPlacedModel
from app.models.company import CompanyModel

class ProductModel(SQLModel, table=True):
    __tablename__ = 'product'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    price: float
    company_id: UUID = Field(foreign_key="company.id")
    product_ranking: Optional[float] = Field(default=0.0)
    stock: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    company: Optional[CompanyModel] = Relationship(back_populates="products")
    comments: Optional[List["CommentModel"]] = Relationship(back_populates="product")
    orders: Optional[List["OrderPlacedModel"]] = Relationship(back_populates="product")
