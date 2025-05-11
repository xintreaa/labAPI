# app/models/__init__.py
from .authors import Author, AuthorCreate, AuthorUpdate, AuthorRead
from .books import Book, BookCreate, BookUpdate, BookRead
from .categories import Category, CategoryCreate, CategoryUpdate, CategoryRead
from .users import User, UserCreate, UserUpdate, UserRead
from .borrowed_books import BorrowedBook, BorrowedBookCreate, BorrowedBookUpdate, BorrowedBookRead
from .links import BookAuthorLink, BookCategoryLink