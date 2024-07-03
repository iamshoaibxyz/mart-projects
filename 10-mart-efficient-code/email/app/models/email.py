from sqlmodel import SQLModel, Field, Relationship, TEXT
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

class EmailContentLink(SQLModel, table=True):
    __tablename__ = 'email_content_link'
    email_id: UUID = Field(foreign_key='email.id', primary_key=True)
    content_id: UUID = Field(foreign_key='email_content.id', primary_key=True)

class Email(SQLModel, table=True):
    __tablename__ = 'email'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    recipient_email: str = Field(nullable=False)
    subject: str = Field(nullable=False)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(nullable=False)

    contents: List["EmailContent"] = Relationship(
        back_populates="emails"
    )

class EmailContent(SQLModel, table=True):
    __tablename__ = 'email_content'
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    content: str = Field(nullable=False, sa_column=TEXT)

    emails: List[Email] = Relationship(
        back_populates="contents"
    )
