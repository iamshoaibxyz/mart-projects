from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
 
class UserModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    first_name: str
    last_name: str
    password: str  # This should be hashed
    email: str = Field(unique=True, index=True)
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    
    def get_context_str(self, context: str = "PASSWORD_CONTEXT"):
        return f"{context}{self.password[-3:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"
