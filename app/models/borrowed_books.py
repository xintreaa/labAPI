# app/models/borrowed_books.py
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone, timedelta
from enum import Enum


class BorrowStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"


if TYPE_CHECKING:
    from app.models.users import User

class BorrowedBookBase(SQLModel):
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    borrow_date: datetime = Field(default_factory=datetime.utcnow)
    return_date: Optional[datetime] = None
    due_date: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=14))

class BorrowedBook(BorrowedBookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="borrowed_books")

class BorrowedBookCreate(BorrowedBookBase):
    pass

class BorrowedBookUpdate(SQLModel):
    return_date: Optional[datetime] = None

class BorrowedBookRead(BorrowedBookBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True