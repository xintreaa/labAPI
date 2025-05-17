from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.utils.logger import setup_logging
from app.api import books, authors, categories, borrowed_books
from api.users import users
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_time = time.time()
    logger.info("Starting application...")
    logger.info(f"Application started in {time.time() - start_time:.2f} seconds")
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Library API",
    description="API for managing a library system",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books, prefix="/api/books", tags=["books"])
app.include_router(authors, prefix="/api/authors", tags=["authors"])
app.include_router(categories, prefix="/api/categories", tags=["categories"])
app.include_router(users, prefix="/api/users", tags=["users"])
app.include_router(borrowed_books, prefix="/api/borrowed-books", tags=["borrowed-books"])

@app.get("/", status_code=status.HTTP_200_OK)
async def root(request: Request):
    return {"message": "Welcome to the Library API"}