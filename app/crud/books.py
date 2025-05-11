# app/crud/books.py
from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from datetime import datetime

from app.models.books import Book, BookCreate, BookUpdate
from app.models.authors import Author
from app.models.categories import Category
from app.models.links import BookAuthorLink, BookCategoryLink
from app.crud.base import CRUDBase
from app.utils.exceptions import LibraryException

class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def create_with_relations(
            self, db: Session, *, obj_in: BookCreate
    ) -> Book:
        book = Book(
            title=obj_in.title,
            publication_year=obj_in.publication_year,
            isbn=obj_in.isbn,
            quantity=obj_in.quantity
        )
        db.add(book)
        db.flush()

        self._set_authors(db, book, obj_in.author_ids)

        if hasattr(obj_in, 'category_ids') and obj_in.category_ids is not None:
            self._set_categories(db, book, obj_in.category_ids)

        db.commit()
        db.refresh(book)
        return book

    def update_with_relations(
            self, db: Session, *, db_obj: Book, obj_in: BookUpdate
    ) -> Book:
        update_data = obj_in.model_dump(exclude_unset=True)
        simple_fields = ["title", "publication_year", "isbn", "quantity"]
        for field in simple_fields:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db_obj.updated_at = datetime.utcnow()

        if obj_in.author_ids is not None:
            self._set_authors(db, db_obj, obj_in.author_ids)

        if hasattr(obj_in, 'category_ids') and obj_in.category_ids is not None:
            self._set_categories(db, db_obj, obj_in.category_ids)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _set_authors(self, db: Session, book: Book, author_ids: List[int]) -> None:
        statement = select(BookAuthorLink).where(BookAuthorLink.book_id == book.id)
        existing_links = db.exec(statement).all()
        for link in existing_links:
            db.delete(link)
        db.flush()

        for author_id in author_ids:
            author = db.get(Author, author_id)
            if not author:
                raise LibraryException(f"Author with ID {author_id} not found")
            link = BookAuthorLink(book_id=book.id, author_id=author_id)
            db.add(link)

    def _set_categories(self, db: Session, book: Book, category_ids: List[int]) -> None:
        statement = select(BookCategoryLink).where(BookCategoryLink.book_id == book.id)
        existing_links = db.exec(statement).all()
        for link in existing_links:
            db.delete(link)
        db.flush()

        for category_id in category_ids:
            category = db.get(Category, category_id)
            if not category:
                raise LibraryException(f"Category with ID {category_id} not found")
            link = BookCategoryLink(book_id=book.id, category_id=category_id)
            db.add(link)

    def search_books(
            self,
            db: Session,
            *,
            title: Optional[str] = None,
            author_id: Optional[int] = None,
            category_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Book]:
        query = select(Book).options(
            selectinload(Book.authors),
            selectinload(Book.categories)
        )

        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))

        if author_id:
            query = query.join(BookAuthorLink).where(BookAuthorLink.author_id == author_id)

        if category_id:
            query = query.join(BookCategoryLink).where(BookCategoryLink.category_id == category_id)

        query = query.offset(skip).limit(limit)
        results = db.exec(query).all()
        # Додаткова перевірка: переконаємося, що зв’язки завантажені
        for book in results:
            if book.authors is None:
                book.authors = []
            if book.categories is None:
                book.categories = []
        return results

crud_books = CRUDBook(Book)