from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.Cruds.Law_crud import check_zastroy_credentials
from backend.Schemas.User_schema import UserModel, UserResponse, UserLogin
from backend.Cruds.User_crud import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user,
    check_user_credentials,
    get_user_by_phone
)
from backend.Database.DB_connection import get_db
from backend.Schemas.Zastroy_schema import ZastroyLogin

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserModel, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def user_login(
        credentials: UserLogin,
        db: Session = Depends(get_db)
):
    if check_user_credentials(db, credentials.phone, credentials.password):
        return {"status": "success", "message": "Аутентификация прошла успешно"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный Телефон или пароль"
    )


@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    user: UserModel,
    db: Session = Depends(get_db)
):
    try:
        return update_user(db, user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return delete_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))