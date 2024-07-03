from typing import ForwardRef, Optional
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from enum import Enum
from app.models.user import UserModel
from app.models.product import ProductModel

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderPlacedModel(SQLModel, table=True):
    __tablename__ = 'order'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    product_id: UUID = Field(foreign_key="product.id")
    product_price: float
    quantity: int
    total_price: float
    order_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    delivery_date: Optional[datetime] = None
    delivered: bool = Field(default=False)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    return_back: Optional[datetime] = None                  # can be return back within 7 days, after delivered 
    delivery_address: str
    user: Optional["UserModel"] = Relationship(ForwardRef("UserModel"), back_populates="orders")
    product: Optional["ProductModel"] = Relationship(ForwardRef("ProductModel"), back_populates="orders")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
