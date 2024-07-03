from sqlalchemy import Column, TEXT
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, ForwardRef
from uuid import UUID, uuid4
from datetime import datetime
from app.models.user import UserModel
from app.models.product import ProductModel

class CommentModel(SQLModel, table=True):
    __tablename__ = 'comment'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    product_id: UUID = Field(foreign_key="product.id")
    comment_text: str = Field(sa_column=Column(TEXT, nullable=False))
    rating: Optional[float] = Field(default=0.0)  # Rating out of 5
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    user: Optional["UserModel"] = Relationship(ForwardRef("UserModel") ,back_populates="comments")
    product: Optional["ProductModel"] = Relationship(ForwardRef("ProductModel") ,back_populates="comments")

