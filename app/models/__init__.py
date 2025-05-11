# app/models/__init__.py
# Імпортуємо лише те, що потрібно, і уникаємо імпорту самих моделей
from .links import BookAuthorLink, BookCategoryLink

# Імпортуємо моделі в кінці, щоб уникнути циклічних імпортів
from .authors import Author, AuthorCreate, AuthorUpdate, AuthorRead
from .books import Book, BookCreate, BookUpdate, BookRead
from .categories import Category, CategoryCreate, CategoryUpdate, CategoryRead
# Додайте інші моделі, якщо вони є (наприклад, User, BorrowedBook)