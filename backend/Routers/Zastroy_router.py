from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from typing import List, Optional

from Cruds.RC_crud import create_residential_complex, get_residential_complexes_by_developer, get_all_residential_complexes, get_residential_complexes_by_zastroy_id, get_residential_complex, rate_residential_complex
from Cruds.Property_crud import get_properties_by_complex, rate_property, mark_property_error
from Cruds.DeveloperRating_crud import get_developer_rating, get_developer_stats, calculate_developer_rating, update_developer_rating
from Schemas.RC_schema import ResidentialComplexCreate, ResidentialComplexResponse, RatingModel
from Schemas.Property_schema import PropertyResponse
from Schemas.Zastroy_schema import ZastroyModel, ZastroyResponse, ZastroyLogin, ZastroyWithStatsResponse
from Schemas.DeveloperRating_schema import DeveloperRatingResponse, DeveloperStatsResponse
from Cruds.Law_crud import (
    create_zastroy,
    get_zastroy,
    get_zastroys,
    update_zastroy,
    delete_zastroy, 
    check_zastroy_credentials
)
from Database.DB_connection import get_db

router = APIRouter(prefix="/zastroys", tags=["Застройщики"])

@router.post("/", response_model=ZastroyResponse)
def create_new_zastroy(zastroy: ZastroyModel, db: Session = Depends(get_db)):
    try:
        return create_zastroy(db, zastroy)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def zastroy_login(credentials: ZastroyLogin, db: Session = Depends(get_db)):
    if check_zastroy_credentials(db, credentials.inn, credentials.password):
        return {"status": "success", "message": "Аутентификация прошла успешно"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный ИНН или пароль"
    )

@router.get("/", response_model=list[ZastroyResponse])
def read_zastroys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_zastroys(db, skip=skip, limit=limit)

@router.get("/{zastroy_id}", response_model=ZastroyResponse)
def read_zastroy(zastroy_id: int, db: Session = Depends(get_db)):
    db_zastroy = get_zastroy(db, zastroy_id)
    if not db_zastroy:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    return db_zastroy

@router.get("/{zastroy_id}/with-stats", response_model=ZastroyWithStatsResponse)
def read_zastroy_with_stats(zastroy_id: int, db: Session = Depends(get_db)):
    """Получить застройщика с рейтингом и статистикой"""
    db_zastroy = get_zastroy(db, zastroy_id)
    if not db_zastroy:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    # Получаем рейтинг
    rating = get_developer_rating(db, zastroy_id)
    
    # Получаем статистику
    stats = get_developer_stats(db, zastroy_id)
    
    # Формируем ответ
    response_data = {
        "id": db_zastroy.id,
        "Company_name": db_zastroy.Company_name,
        "INN": db_zastroy.INN,
        "OGRN": db_zastroy.OGRN,
        "Adress": db_zastroy.Adress,
        "User_name": db_zastroy.User_name,
        "password": db_zastroy.password,
        "rating": rating,
        "stats": stats
    }
    
    return response_data

@router.put("/{zastroy_id}", response_model=ZastroyResponse)
def update_existing_zastroy(zastroy_id: int, zastroy: ZastroyModel, db: Session = Depends(get_db)):
    try:
        return update_zastroy(db, zastroy_id, zastroy)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{zastroy_id}")
def remove_zastroy(zastroy_id: int, db: Session = Depends(get_db)):
    try:
        return delete_zastroy(db, zastroy_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Новые эндпоинты для рейтинга застройщиков
@router.get("/{zastroy_id}/rating", response_model=DeveloperRatingResponse)
def get_zastroy_rating(zastroy_id: int, db: Session = Depends(get_db)):
    """Получить рейтинг застройщика"""
    rating = get_developer_rating(db, zastroy_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Рейтинг застройщика не найден")
    return rating

@router.get("/{zastroy_id}/stats", response_model=DeveloperStatsResponse)
def get_zastroy_stats(zastroy_id: int, db: Session = Depends(get_db)):
    """Получить статистику застройщика"""
    try:
        stats = get_developer_stats(db, zastroy_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{zastroy_id}/recalculate-rating")
def recalculate_zastroy_rating(zastroy_id: int, db: Session = Depends(get_db)):
    """Пересчитать рейтинг застройщика"""
    try:
        new_rating = calculate_developer_rating(db, zastroy_id)
        update_developer_rating(db, zastroy_id, rating=new_rating)
        return {"message": "Рейтинг пересчитан", "new_rating": new_rating}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/residential-complexes/", response_model=ResidentialComplexResponse)
def add_residential_complex(
    complex_data: ResidentialComplexCreate,
    db: Session = Depends(get_db)
):
    return create_residential_complex(db, complex_data)

@router.get("/residential-complexes/", response_model=List[ResidentialComplexResponse])
def get_residential_complexes(
    zastroy_id: Optional[int] = Query(None, description="ID застройщика"),
    city: Optional[str] = Query(None, description="Город"),
    housing_class: Optional[str] = Query(None, description="Класс жилья"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if zastroy_id:
        return get_residential_complexes_by_zastroy_id(db, zastroy_id, skip=skip, limit=limit)
    else:
        return get_all_residential_complexes(db, skip=skip, limit=limit)

@router.get("/residential-complexes/{complex_id}", response_model=ResidentialComplexResponse)
def get_residential_complex_detail(complex_id: int, db: Session = Depends(get_db)):
    """Получить детальную информацию о ЖК"""
    complex_data = get_residential_complex(db, complex_id)
    if not complex_data:
        raise HTTPException(status_code=404, detail="Жилой комплекс не найден")
    return complex_data

@router.get("/residential-complexes/{complex_id}/apartments", response_model=List[PropertyResponse])
def get_apartments_in_complex(
    complex_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить квартиры в конкретном ЖК"""
    return get_properties_by_complex(db, complex_id, skip=skip, limit=limit)

@router.post("/residential-complexes/{complex_id}/rate")
def rate_complex(
    complex_id: int,
    rating_data: RatingModel,
    db: Session = Depends(get_db)
):
    """Оценить ЖК"""
    try:
        rate_residential_complex(db, complex_id, rating_data.rating)
        return {"message": "Рейтинг успешно добавлен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/properties/{property_id}/rate")
def rate_property_endpoint(
    property_id: int,
    rating_data: RatingModel,
    db: Session = Depends(get_db)
):
    """Оценить квартиру"""
    try:
        rate_property(db, property_id, rating_data.rating)
        return {"message": "Рейтинг успешно добавлен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/properties/{property_id}/mark-error")
def mark_property_error_endpoint(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Пометить квартиру как имеющую ошибку"""
    try:
        mark_property_error(db, property_id)
        return {"message": "Квартира помечена как имеющая ошибку"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))