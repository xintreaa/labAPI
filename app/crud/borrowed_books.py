# app/crud/borrowed_books.py
from app.models.borrowed_books import BorrowedBook, BorrowedBookCreate, BorrowedBookUpdate
from app.crud.base import CRUDBase
from sqlmodel import Session
from datetime import datetime, timezone

class CRUDBorrowedBook(CRUDBase[BorrowedBook, BorrowedBookCreate, BorrowedBookUpdate]):
    def create(self, db: Session, *, obj_in: BorrowedBookCreate) -> BorrowedBook:
        db_obj = BorrowedBook(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: BorrowedBook, obj_in: BorrowedBookUpdate) -> BorrowedBook:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_borrowed_books = CRUDBorrowedBook(BorrowedBook)