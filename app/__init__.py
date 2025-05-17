# app/api/__init__.py
from app.api.books import router as books
from app.api.authors import router as authors
from app.api.categories import router as categories
from app.api.users import users
from app.api.borrowed_books import router as borrowed_books
