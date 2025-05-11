from typing import List
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.books import Book
from app.models.borrowed_books import BorrowedBook, BorrowStatus
from app.config import get_settings
from app.utils.exceptions import LibraryException
from app.utils.logger import setup_logging

logger = setup_logging()
settings = get_settings()


class BookService:
    def get_available_copies(self, db: Session, book_id: int) -> int:
        """
        Calculate how many copies of a book are available for borrowing
        """
        book = db.get(Book, book_id)
        if not book:
            raise LibraryException(f"Book with ID {book_id} not found")

        # Count active borrows
        stmt = select(BorrowedBook).where(
            BorrowedBook.book_id == book_id,
            BorrowedBook.status == BorrowStatus.ACTIVE
        )
        active_borrows = len(db.exec(stmt).all())

        return max(0, book.quantity - active_borrows)

    def has_active_borrows(self, db: Session, book_id: int) -> bool:
        """
        Check if a book has any active borrows
        """
        stmt = select(BorrowedBook).where(
            BorrowedBook.book_id == book_id,
            BorrowedBook.status == BorrowStatus.ACTIVE
        )
        return len(db.exec(stmt).all()) > 0

    def borrow_book(self, db: Session, book_id: int, user_id: int) -> BorrowedBook:
        """
        Create a new borrow record for a book
        """
        # Check if the book exists
        book = db.get(Book, book_id)
        if not book:
            raise LibraryException(f"Book with ID {book_id} not found")

        # Check if there are available copies
        available_copies = self.get_available_copies(db, book_id)
        if available_copies <= 0:
            raise LibraryException(f"No available copies of book with ID {book_id}")

        # Check if the user has reached the maximum borrow limit
        stmt = select(BorrowedBook).where(
            BorrowedBook.user_id == user_id,
            BorrowedBook.status == BorrowStatus.ACTIVE
        )
        user_active_borrows = len(db.exec(stmt).all())
        if user_active_borrows >= settings.MAX_BORROWS_PER_USER:
            raise LibraryException(f"User has reached the maximum borrow limit of {settings.MAX_BORROWS_PER_USER}")

        # Create a new borrow record
        borrow_date = datetime.utcnow()
        due_date = borrow_date + timedelta(days=settings.BORROW_DURATION_DAYS)

        borrow = BorrowedBook(
            book_id=book_id,
            user_id=user_id,
            borrow_date=borrow_date,
            due_date=due_date,
            status=BorrowStatus.ACTIVE
        )

        db.add(borrow)
        db.commit()
        db.refresh(borrow)

        logger.info(f"Book ID {book_id} borrowed by User ID {user_id} until {due_date}")
        return borrow

    def return_book(self, db: Session, borrow_id: int) -> BorrowedBook:
        """
        Mark a book as returned
        """
        borrow = db.get(BorrowedBook, borrow_id)
        if not borrow:
            raise LibraryException(f"Borrow record with ID {borrow_id} not found")

        if borrow.status != BorrowStatus.ACTIVE:
            raise LibraryException(f"Book has already been returned")

        borrow.status = BorrowStatus.RETURNED
        borrow.return_date = datetime.utcnow()

        # Check if the book is overdue
        if borrow.due_date < borrow.return_date:
            days_overdue = (borrow.return_date - borrow.due_date).days
            fine = days_overdue * settings.OVERDUE_FINE_RATE
            logger.info(f"Book returned {days_overdue} days late. Fine: {fine}")

        db.add(borrow)
        db.commit()
        db.refresh(borrow)

        logger.info(f"Book ID {borrow.book_id} returned by User ID {borrow.user_id}")
        return borrow

    def get_overdue_books(self, db: Session) -> List[BorrowedBook]:
        """
        Get all overdue books
        """
        now = datetime.utcnow()
        stmt = select(BorrowedBook).where(
            BorrowedBook.status == BorrowStatus.ACTIVE,
            BorrowedBook.due_date < now
        )
        overdue_books = db.exec(stmt).all()

        # Update their status to overdue
        for book in overdue_books:
            if book.status != BorrowStatus.OVERDUE:
                book.status = BorrowStatus.OVERDUE
                db.add(book)

        db.commit()
        return overdue_books