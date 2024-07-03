from datetime import datetime
from typing import List, Optional, TYPE_CHECKING, ForwardRef
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.order import OrderPlacedModel
    from app.models.user import UserModel
    from app.models.comment import CommentModel

class UserModel(SQLModel, table=True):
    __tablename__ = "user"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    first_name: str
    last_name: str
    password: str  # This should be hashed
    email: str = Field(unique=True, index=True)
    is_verified: bool = Field(default=False, nullable=True)
    verified_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tokens: Optional[List["UserTokenModel"]] = Relationship(back_populates="user")
    orders: Optional[List["OrderPlacedModel"]] = Relationship(back_populates="user")
    comments: Optional[List["CommentModel"]] = Relationship(back_populates="user")

    def get_context_str(self):
        return f"{"USER_CONTEXT"}{self.password[-6:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}"

class UserTokenModel(SQLModel, table=True):
    __tablename__ = "user_token"
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: Optional[UUID] = Field(None, foreign_key="user.id")
    token: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False )
    expired_at: datetime = Field(nullable=False) 
    user: "UserModel" = Relationship(back_populates="tokens")
