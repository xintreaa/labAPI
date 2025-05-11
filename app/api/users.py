# app/api/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.database import get_session
from app.models.users import UserCreate, UserRead, UserUpdate
from app.crud.users import crud_users

users = APIRouter()

@users.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    try:
        return crud_users.create(db=db, obj_in=user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@users.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return crud_users.get_multi(db=db, skip=skip, limit=limit)

@users.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = crud_users.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
    return user

@users.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    db_user = crud_users.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
    try:
        updated_user = crud_users.update(db=db, db_obj=db_user, obj_in=user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update user: {str(e)}")

@users.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    user = crud_users.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
    if user.borrowed_books:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot delete user with ID {user_id} because they have active borrows")
    return crud_users.remove(db=db, id=user_id)