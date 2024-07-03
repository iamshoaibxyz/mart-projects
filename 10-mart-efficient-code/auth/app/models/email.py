from sqlalchemy import Column, TEXT
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, ForwardRef

class Email(SQLModel, table=True):
    __tablename__ = 'email'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    recipient_email: str = Field(nullable=False)
    subject: str = Field(nullable=False)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(nullable=False)
    
    contents: List["EmailContent"] = Relationship(ForwardRef("EmailContent"), back_populates="email")

class EmailContent(SQLModel, table=True):
    __tablename__ = 'email_content'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    content: str = Field(sa_column=Column(TEXT, nullable=False))
    email_id: UUID = Field(foreign_key='email.id')
    
    email: "Email" = Relationship(ForwardRef("Email"), back_populates="contents")
