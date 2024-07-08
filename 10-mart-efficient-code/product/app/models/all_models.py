from pydantic import EmailStr
from sqlalchemy import TEXT, Column
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List 
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
 
class CompanyModel(SQLModel, table=True):
    __tablename__ = 'company'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = Field(sa_column=TEXT)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    tokens: Optional[List["CompanyTokenModel"]] = Relationship(back_populates="company")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    products: Optional[List["ProductModel"]] = Relationship(back_populates="company")

    def get_context_str(self, context: str = "PASSWORD_CONTEXT"):
        return f"{context}{self.password[-7:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"

class CompanyTokenModel(SQLModel, table=True):
    __tablename__ = "company_token"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    company_id: Optional[UUID] = Field(None, foreign_key="company.id")
    token: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False )
    expired_at: datetime = Field(nullable=False) 
    company: Optional["CompanyModel"] = Relationship(back_populates="tokens")

class UserModel(SQLModel, table=True):
    __tablename__ = "user"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    first_name: str
    last_name: str
    password: str  # This should be hashed
    email: str = Field(unique=True, index=True)
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    tokens: Optional[List["UserTokenModel"]] = Relationship(back_populates="user")
    orders: Optional[List["OrderPlacedModel"]] = Relationship(back_populates="user")
    comments: Optional[List["CommentModel"]] = Relationship(back_populates="user")

    def get_context_str(self, context: str = "USER_CONTEXT"):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"

class UserTokenModel(SQLModel, table=True):
    __tablename__ = "user_token"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: Optional[UUID] = Field(None, foreign_key="user.id")
    token: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False )
    expired_at: datetime = Field(nullable=False) 
    user: "UserModel" = Relationship(back_populates="tokens")

class CommentModel(SQLModel, table=True):
    __tablename__ = 'comment'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    product_id: UUID = Field(foreign_key="product.id")
    comment_text: str = Field(sa_column=Column(TEXT, nullable=False))
    rating: Optional[float] = Field(default=0.0)  # Rating out of 5
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    user: Optional["UserModel"] = Relationship(back_populates="comments")
    product: Optional["ProductModel"] = Relationship(back_populates="comments")

class Email(SQLModel, table=True):
    __tablename__ = 'email'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    recipient_email: str = Field(nullable=False)
    subject: str = Field(nullable=False)
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(nullable=False)
    
    contents: List["EmailContent"] = Relationship(back_populates="email")

class EmailContent(SQLModel, table=True):
    __tablename__ = 'email_content'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    content: str = Field(sa_column=Column(TEXT, nullable=False))
    email_id: UUID = Field(foreign_key='email.id')
    
    email: "Email" = Relationship(back_populates="contents")
 
class ProductModel(SQLModel, table=True):
    __tablename__ = 'product'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = Field(default="other")
    company_id: UUID = Field(foreign_key="company.id")
    product_ranking: Optional[float] = Field(default=0.0)
    # stock: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    company: Optional["CompanyModel"] = Relationship(back_populates="products")
    comments: Optional[List["CommentModel"]] = Relationship(back_populates="product")
    orders: Optional[List["OrderPlacedModel"]] = Relationship(back_populates="product")
    stock: Optional["StockLevel"] = Relationship(back_populates="product", sa_relationship_kwargs={"uselist": False})
    transactions: Optional[List["InventoryTransaction"]] = Relationship(back_populates="product")

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
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    delivery_date: Optional[datetime] = None
    delivered: bool = Field(default=False)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    return_back: Optional[datetime] = None                  # can be return back within 7 days, after delivered 
    delivery_address: str
    user: Optional["UserModel"] = Relationship(back_populates="orders")
    product: Optional["ProductModel"] = Relationship(back_populates="orders")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Operation(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"

class InventoryTransaction(SQLModel, table=True):
    __tablename__ = 'inventory_transaction'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    stock_id: UUID = Field(foreign_key="stock_level.id")
    product_id: UUID = Field(foreign_key="product.id")
    quantity: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operation: Operation
    stock: Optional["StockLevel"] = Relationship(back_populates="transactions")
    product: Optional["ProductModel"] = Relationship(back_populates="transactions")

class StockLevel(SQLModel, table=True):
    __tablename__ = 'stock_level'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="product.id")
    current_stock: int = 0
    transactions: Optional[List["InventoryTransaction"]] = Relationship(back_populates="stock")
    product: Optional["ProductModel"] = Relationship(back_populates="stock")

