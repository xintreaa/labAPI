# app/crud/users.py
from app.models.users import User, UserCreate, UserUpdate
from app.crud.base import CRUDBase
from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        try:
            db_obj = User(**obj_in.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise ValueError("Email already exists")

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "email" in update_data:
            # Перевіряємо, чи email вже існує для іншого користувача
            existing_user = db.exec(
                select(User).where(User.email == update_data["email"]).where(User.id != db_obj.id)
            ).first()
            if existing_user:
                raise ValueError(f"Email {update_data['email']} already exists for another user")
        try:
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            db_obj.updated_at = datetime.now(timezone.utc)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise ValueError("Failed to update user due to database constraint (e.g., duplicate email)")

crud_users = CRUDUser(User)