# app/api/books.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.models.books import BookCreate, BookRead, BookUpdate
from app.crud.books import crud_books
from app.services import book_service

router = APIRouter()

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_session)
):
    # Check if a book with the same ISBN already exists
    existing_books = crud_books.search_books(db, title=None, author_id=None)
    for existing_book in existing_books:
        if existing_book.isbn == book.isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book.isbn} already exists"
            )

    created_book = crud_books.create_with_relations(db=db, obj_in=book)
    # Явне завантаження зв’язків
    created_book.authors  # Завантажуємо авторів
    created_book.categories  # Завантажуємо категорії
    return created_book

@router.get("/", response_model=List[BookRead])
def read_books(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    author_id: Optional[int] = None,
    category_id: Optional[int] = None
):
    books = crud_books.search_books(
        db=db,
        title=title,
        author_id=author_id,
        category_id=category_id,
        skip=skip,
        limit=limit
    )
    # Явне завантаження зв’язків для всіх книг
    for book in books:
        book.authors  # Завантажуємо авторів
        book.categories  # Завантажуємо категорії
    return books

@router.get("/{book_id}", response_model=BookRead)
def read_book(
    *,
    book_id: int,
    db: Session = Depends(get_session)
):
    book = crud_books.get(db=db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    # Явне завантаження зв’язків
    book.authors  # Завантажуємо авторів
    book.categories  # Завантажуємо категорії
    return book

@router.put("/{book_id}", response_model=BookRead)
def update_book(
    *,
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_session)
):
    db_book = crud_books.get(db=db, id=book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Check ISBN uniqueness if it's being updated
    if book.isbn and book.isbn != db_book.isbn:
        existing_books = crud_books.search_books(db, title=None, author_id=None, category_id=None)
        for existing_book in existing_books:
            if existing_book.isbn == book.isbn:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with ISBN {book.isbn} already exists"
                )

    updated_book = crud_books.update_with_relations(db=db, db_obj=db_book, obj_in=book)
    # Явне завантаження зв’язків
    updated_book.authors  # Завантажуємо авторів
    updated_book.categories  # Завантажуємо категорії
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    *,
    book_id: int,
    db: Session = Depends(get_session)
):
    book = crud_books.get(db=db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    # Check if the book has active borrows
    '''
    if book_service.has_active_borrows(db=db, book_id=book_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete book with ID {book_id} because it has active borrows"
        )
    '''
    crud_books.remove(db=db, id=book_id)
    return {"message": "Book deleted successfully"}  # Повертаємо відповідь для відповідності status_code


@router.get("/{book_id}/available", response_model=dict)
def check_book_availability(
    *,
    book_id: int,
    db: Session = Depends(get_session)
):
    book = crud_books.get(db=db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    available_copies = book_service.get_available_copies(db=db, book_id=book_id)

    return {
        "book_id": book_id,
        "total_copies": book.quantity,
        "available_copies": available_copies,
        "is_available": available_copies > 0
    }
