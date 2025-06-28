from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from Database.DB_connection import get_db
from Cruds.Analytics_crud import AnalyticsCRUD
from Cruds.Property_crud import get_properties
from Schemas.Analytics_schema import EventCreate, EventResponse, AnalyticsSummary
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["analytics"])

@router.post("/track-event", response_model=EventResponse)
async def track_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Отслеживание события пользователя
    
    Типы событий:
    - view_apartment: просмотр квартиры
    - click_3d_tour: клик по 3D туру
    - click_book: клик по кнопке бронирования
    - time_on_page: время проведенное на странице (в секундах)
    - search_property: поиск недвижимости
    - filter_applied: применение фильтров
    """
    try:
        analytics_crud = AnalyticsCRUD(db)
        db_event = analytics_crud.create_event(event)
        # Явно преобразуем в схему Pydantic
        return EventResponse.model_validate(db_event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении события: {str(e)}")

@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = Query(30, description="Количество дней для анализа"),
    db: Session = Depends(get_db)
):
    """Получить общую сводку аналитики"""
    try:
        analytics_crud = AnalyticsCRUD(db)
        return analytics_crud.get_analytics_summary(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении аналитики: {str(e)}")

@router.get("/analytics/apartment/{apartment_id}")
async def get_apartment_analytics(
    apartment_id: int,
    days: int = Query(30, description="Количество дней для анализа"),
    db: Session = Depends(get_db)
):
    """Получить аналитику для конкретной квартиры"""
    try:
        analytics_crud = AnalyticsCRUD(db)
        return analytics_crud.get_apartment_analytics(apartment_id, days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении аналитики квартиры: {str(e)}")

@router.get("/analytics/events/apartment/{apartment_id}", response_model=List[EventResponse])
async def get_apartment_events(
    apartment_id: int,
    db: Session = Depends(get_db)
):
    """Получить все события для конкретной квартиры"""
    try:
        analytics_crud = AnalyticsCRUD(db)
        events = analytics_crud.get_events_by_apartment(apartment_id)
        return [EventResponse.model_validate(event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении событий: {str(e)}")

@router.get("/analytics/events/user/{user_id}", response_model=List[EventResponse])
async def get_user_events(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Получить все события конкретного пользователя"""
    try:
        analytics_crud = AnalyticsCRUD(db)
        events = analytics_crud.get_events_by_user(user_id)
        return [EventResponse.model_validate(event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении событий пользователя: {str(e)}")

@router.get("/analytics/events/type/{event_type}", response_model=List[EventResponse])
async def get_events_by_type(
    event_type: str,
    db: Session = Depends(get_db)
):
    """Получить все события определенного типа"""
    try:
        analytics_crud = AnalyticsCRUD(db)
        events = analytics_crud.get_events_by_type(event_type)
        return [EventResponse.model_validate(event) for event in events]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении событий по типу: {str(e)}")

@router.get("/analytics/developer/{developer_id}")
async def get_developer_analytics(
    developer_id: int,
    days: int = Query(30, description="Количество дней для анализа"),
    db: Session = Depends(get_db)
):
    """Получить аналитику для всех квартир застройщика"""
    try:
        # Получаем все квартиры застройщика
        properties = get_properties(db, zastroy_id=developer_id)
        
        analytics_crud = AnalyticsCRUD(db)
        developer_analytics = {
            "developer_id": developer_id,
            "total_properties": len(properties),
            "properties_analytics": []
        }
        
        for property in properties:
            property_analytics = analytics_crud.get_apartment_analytics(property.id, days)
            developer_analytics["properties_analytics"].append(property_analytics)
        
        return developer_analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении аналитики застройщика: {str(e)}") 