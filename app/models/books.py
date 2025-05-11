# app/models/books.py
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from app.models.links import BookAuthorLink, BookCategoryLink
# Явно імпортуємо AuthorRead і CategoryRead
from app.models.authors import Author, AuthorRead
from app.models.categories import Category, CategoryRead

class BookBase(SQLModel):
    title: str = Field(index=True)
    publication_year: int = Field(default=None)
    isbn: str = Field(unique=True, index=True)
    quantity: int = Field(default=1)

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    authors: List[Author] = Relationship(
        back_populates="books",
        link_model=BookAuthorLink
    )
    categories: List[Category] = Relationship(
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
    authors: List[AuthorRead] = []  # Використовуємо AuthorRead напряму
    categories: List[CategoryRead] = []  # Використовуємо CategoryRead напряму

    class Config:
        from_attributes = True