# app/models/authors.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from app.models.links import BookAuthorLink  # Імпортуємо напряму

if TYPE_CHECKING:
    from app.models.books import Book

class AuthorBase(SQLModel):
    first_name: str
    last_name: str

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    books: List["Book"] = Relationship(
        back_populates="authors",
        link_model=BookAuthorLink
    )

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(AuthorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AuthorRead(AuthorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True