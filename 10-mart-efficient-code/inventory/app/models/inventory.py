from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

Operation = Literal["add", "subtract"]

class InventoryTransaction(SQLModel, table=True):
    __tablename__ = "transaction"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    stock_id: UUID = Field(index=True)  # Reference to stock
    product_id: UUID = Field(index=True)  # Reference to product
    quantity: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    operation: str  # Operation

class StockLevel(SQLModel, table=True):
    __tablename__ = "stock"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(index=True, unique=True)  # Reference to product
    current_stock: int
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
