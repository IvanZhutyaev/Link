from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from Cruds.DeveloperRating_crud import (
    get_developer_rating,
    get_developer_stats,
    calculate_developer_rating,
    update_developer_rating,
    get_all_developer_ratings,
    create_developer_rating,
    get_top_developers
)
from Schemas.DeveloperRating_schema import (
    DeveloperRatingResponse,
    DeveloperStatsResponse,
    DeveloperRatingUpdate,
    DeveloperRatingCreate,
    TopDeveloperResponse
)
from Database.DB_connection import get_db

router = APIRouter(prefix="/developer-ratings", tags=["Рейтинг застройщиков"])


@router.get("/{law_face_id}", response_model=DeveloperRatingResponse)
def get_rating(law_face_id: int, db: Session = Depends(get_db)):
    """Получить рейтинг застройщика"""
    rating = get_developer_rating(db, law_face_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Рейтинг застройщика не найден")
    return rating


@router.post("/", response_model=DeveloperRatingResponse)
def create_rating(rating_data: DeveloperRatingCreate, db: Session = Depends(get_db)):
    """Создать рейтинг застройщика"""
    try:
        return create_developer_rating(
            db, 
            rating_data.law_face_id, 
            rating_data.rating, 
            rating_data.completed_projects, 
            rating_data.years_on_market
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{law_face_id}", response_model=DeveloperRatingResponse)
def update_rating(
    law_face_id: int, 
    rating_data: DeveloperRatingUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить рейтинг застройщика"""
    try:
        return update_developer_rating(
            db, 
            law_face_id, 
            rating_data.rating, 
            rating_data.completed_projects, 
            rating_data.years_on_market
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{law_face_id}/calculate")
def recalculate_rating(law_face_id: int, db: Session = Depends(get_db)):
    """Пересчитать рейтинг застройщика на основе его объектов"""
    try:
        new_rating = calculate_developer_rating(db, law_face_id)
        update_developer_rating(db, law_face_id, rating=new_rating)
        return {"message": "Рейтинг пересчитан", "new_rating": new_rating}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{law_face_id}/stats", response_model=DeveloperStatsResponse)
def get_stats(law_face_id: int, db: Session = Depends(get_db)):
    """Получить статистику застройщика"""
    try:
        stats = get_developer_stats(db, law_face_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top/", response_model=List[TopDeveloperResponse])
def get_top_developers_list(
    limit: int = Query(10, ge=1, le=50, description="Количество застройщиков"),
    db: Session = Depends(get_db)
):
    """Получить топ застройщиков по рейтингу"""
    try:
        top_developers = get_top_developers(db, limit)
        result = []
        for rating, law_face in top_developers:
            result.append({
                "id": law_face.id,
                "company_name": law_face.Company_name,
                "rating": rating.rating,
                "completed_projects": rating.completed_projects,
                "years_on_market": rating.years_on_market
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 