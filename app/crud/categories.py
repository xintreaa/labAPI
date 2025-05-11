# app/crud/categories.py
from app.models.categories import Category, CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase
import datetime
from sqlmodel import Session
class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def create_with_relations(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_relations(self, db: Session, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db_obj.updated_at = datetime.now(datetime.timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_categories = CRUDCategory(Category)