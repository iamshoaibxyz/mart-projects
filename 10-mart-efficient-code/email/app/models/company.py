from sqlmodel import Field, SQLModel, Relationship, TEXT
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import EmailStr

class CompanyModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = Field(sa_column=TEXT)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    def get_context_str(self, context: str = "PASSWORD_CONTEXT"):
        return f"{context}{self.password[-7:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"

