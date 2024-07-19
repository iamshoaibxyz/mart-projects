from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4

class ProductModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = Field(default="other")
    company_id: UUID = Field(index=True)  # Reference to company
    product_ranking: Optional[float] = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
