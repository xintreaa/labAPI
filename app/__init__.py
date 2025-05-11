# app/api/__init__.py
from api.books import router as books
from api.authors import router as authors
from api.categories import router as categories
from api.users import users
from api.borrowed_books import router as borrowed_books