# app/api/borrowed_books.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models.books import Book
from app.db.database import get_session
from app.models.borrowed_books import BorrowedBookCreate, BorrowedBookRead, BorrowedBookUpdate
from app.crud.borrowed_books import crud_borrowed_books

router = APIRouter()

@router.post("/", response_model=BorrowedBookRead, status_code=status.HTTP_201_CREATED)
def create_borrowed_book(borrow: BorrowedBookCreate, db: Session = Depends(get_session)):
    # Додати логіку перевірки доступності книги (наприклад, quantity > 0)
    book = db.get(Book, borrow.book_id)
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Book with ID {borrow.book_id} is not available")
    book.quantity -= 1
    db.add(book)
    return crud_borrowed_books.create(db=db, obj_in=borrow)

@router.get("/", response_model=List[BorrowedBookRead])
def read_borrowed_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud_borrowed_books.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{borrow_id}", response_model=BorrowedBookRead)
def read_borrowed_book(borrow_id: int, db: Session = Depends(get_session)):
    borrow = crud_borrowed_books.get(db=db, id=borrow_id)
    if not borrow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Borrow with ID {borrow_id} not found")
    return borrow

@router.put("/{borrow_id}", response_model=BorrowedBookRead)
def update_borrowed_book(borrow_id: int, borrow: BorrowedBookUpdate, db: Session = Depends(get_session)):
    db_borrow = crud_borrowed_books.get(db=db, id=borrow_id)
    if not db_borrow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Borrow with ID {borrow_id} not found")
    if borrow.return_date and not db_borrow.return_date:
        book = db.get(Book, db_borrow.book_id)
        book.quantity += 1
        db.add(book)
    return crud_borrowed_books.update(db=db, db_obj=db_borrow, obj_in=borrow)

@router.delete("/{borrow_id}", response_model=BorrowedBookRead)
def delete_borrowed_book(borrow_id: int, db: Session = Depends(get_session)):
    borrow = crud_borrowed_books.get(db=db, id=borrow_id)
    if not borrow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Borrow with ID {borrow_id} not found")
    if not borrow.return_date:
        book = db.get(Book, borrow.book_id)
        book.quantity += 1
        db.add(book)
    return crud_borrowed_books.remove(db=db, id=borrow_id)