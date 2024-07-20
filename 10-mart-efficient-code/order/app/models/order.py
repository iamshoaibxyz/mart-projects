from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import Optional, List, Literal
from uuid import UUID, uuid4

OrderStatus = Literal["initialized", "pending", "processing", "shipped", "delivered", "cancelled"]
CartStatus = Literal["initialized", "pending", "paid", "cancelled", "completed"]

class OrderPlacedModel(SQLModel, table=True):
    __tablename__ = 'order'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    cart_id: UUID = Field(index=True)
    user_id: UUID = Field(index=True)  # Removed foreign_key
    product_id: UUID = Field(index=True)  # Removed foreign_key
    product_price: float
    quantity: int
    total_price: float
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    delivery_date: Optional[datetime] = None
    delivered: bool = Field(default=False)
    status: str # OrderStatus
    return_back: Optional[datetime] = None
    delivery_address: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # cart: Optional["CartModel"] = Relationship(back_populates="orders")

class CartModel(SQLModel, table=True):
    __tablename__ = 'cart'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)  
    status: str  # CartStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    total_price: float = Field(default=0.0)
    # orders: Optional[list["OrderPlacedModel"]] = Relationship(back_populates="cart")
