# app/db/database.py
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session, inspect
from app.config import get_settings
from app.utils.logger import setup_logging

settings = get_settings()
logger = setup_logging(log_level_str=settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO")

logger.info("DATABASE_URL: %s", settings.DATABASE_URL)

# Налаштування для PostgreSQL
engine = create_engine(
    settings.DATABASE_URL  # Очікуємо URL типу postgresql://user:password@host:port/dbname
)

def create_db_and_tables():
    try:
        # Імпорт моделей для реєстрації
        from app.models import authors, books, categories, borrowed_books, links
        from app.models import users

        # Тест з’єднання
        with engine.connect() as conn:
            logger.info("Database connection successful")

        # Створення таблиць
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")

        # Перевірка таблиць
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info("Existing tables: %s", existing_tables)

        expected_tables = ["author", "book", "book_author_link", "book_category_link", "category", "user", "borrowedbook"]
        for table in expected_tables:
            if table not in existing_tables:
                logger.error(f"Table '{table}' was not created")
            else:
                logger.info(f"Table '{table}' exists")

    except Exception as e:
        logger.error("Error creating tables: %s", str(e))
        raise

def get_session() -> Generator[Session, Session, None]:
    with Session(engine) as session:
        yield session