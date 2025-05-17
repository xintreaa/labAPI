import os
from sqlmodel import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/library_db")
engine = create_engine(DATABASE_URL, echo=True)