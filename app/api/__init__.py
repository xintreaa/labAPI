# app/api/__init__.py
from .authors import router as authors
from .books import router as books
from .categories import router as categories
from .users import APIRouter as users
from .borrowed_books import router as borrowed_books