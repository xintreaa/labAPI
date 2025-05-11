# app/models/categories.py
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from app.models import BookCategoryLink


class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    books: List["Book"] = Relationship(
        back_populates="categories",
        link_model=BookCategoryLink
    )

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Оновлено з orm_mode