# app/models/books.py
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from app.models.links import BookAuthorLink, BookCategoryLink  # Імпортуємо з links.py

if TYPE_CHECKING:
    from app.models.authors import Author
    from app.models.categories import Category

class BookBase(SQLModel):
    title: str = Field(index=True)
    publication_year: int = Field(default=None)
    isbn: str = Field(unique=True, index=True)
    quantity: int = Field(default=1)

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    authors: List["Author"] = Relationship(
        back_populates="books",
        link_model=BookAuthorLink
    )
    categories: List["Category"] = Relationship(
        back_populates="books",
        link_model=BookCategoryLink
    )

class BookCreate(BookBase):
    author_ids: List[int] = []
    category_ids: List[int] = []

class BookUpdate(SQLModel):
    title: Optional[str] = None
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: Optional[int] = None
    author_ids: Optional[List[int]] = None
    category_ids: Optional[List[int]] = None

class BookRead(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Оновлено з orm_mode