# app/models/links.py
from typing import Optional
from sqlmodel import Field, SQLModel

class BookAuthorLink(SQLModel, table=True):
    __tablename__ = "book_author_link"
    __table_args__ = {"extend_existing": True}
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    author_id: Optional[int] = Field(default=None, foreign_key="author.id", primary_key=True)

class BookCategoryLink(SQLModel, table=True):
    __tablename__ = "book_category_link"
    __table_args__ = {"extend_existing": True}
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)