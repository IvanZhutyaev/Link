from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from backend.Models.All_models import ApartmentEvent, Property
from backend.Schemas.Analytics_schema import EventCreate
from typing import List, Dict, Any
from datetime import datetime, timedelta

class AnalyticsCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event: EventCreate) -> ApartmentEvent:
        """Создать новое событие"""
        db_event = ApartmentEvent(
            apartment_id=event.apartment_id,
            user_id=event.user_id,
            event_type=event.event_type,
            event_value=event.event_value,
            created_at=datetime.utcnow()
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_events_by_apartment(self, apartment_id: int) -> List[ApartmentEvent]:
        """Получить все события для конкретной квартиры"""
        return self.db.query(ApartmentEvent).filter(
            ApartmentEvent.apartment_id == apartment_id
        ).order_by(desc(ApartmentEvent.created_at)).all()

    def get_events_by_user(self, user_id: str) -> List[ApartmentEvent]:
        """Получить все события конкретного пользователя"""
        return self.db.query(ApartmentEvent).filter(
            ApartmentEvent.user_id == user_id
        ).order_by(desc(ApartmentEvent.created_at)).all()

    def get_events_by_type(self, event_type: str) -> List[ApartmentEvent]:
        """Получить все события определенного типа"""
        return self.db.query(ApartmentEvent).filter(
            ApartmentEvent.event_type == event_type
        ).order_by(desc(ApartmentEvent.created_at)).all()

    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Получить сводку аналитики за последние N дней"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Общее количество событий
        total_events = self.db.query(func.count(ApartmentEvent.id)).filter(
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Количество уникальных пользователей
        unique_users = self.db.query(func.count(func.distinct(ApartmentEvent.user_id))).filter(
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # События по типам
        events_by_type = self.db.query(
            ApartmentEvent.event_type,
            func.count(ApartmentEvent.id).label('count')
        ).filter(
            ApartmentEvent.created_at >= start_date
        ).group_by(ApartmentEvent.event_type).all()
        
        events_by_type_dict = {event_type: count for event_type, count in events_by_type}
        
        # Среднее время на странице
        avg_time = self.db.query(func.avg(ApartmentEvent.event_value)).filter(
            ApartmentEvent.event_type == 'time_on_page',
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Самые просматриваемые квартиры
        most_viewed = self.db.query(
            ApartmentEvent.apartment_id,
            func.count(ApartmentEvent.id).label('views')
        ).filter(
            ApartmentEvent.event_type == 'view_apartment',
            ApartmentEvent.created_at >= start_date
        ).group_by(ApartmentEvent.apartment_id).order_by(
            desc(func.count(ApartmentEvent.id))
        ).limit(10).all()
        
        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "events_by_type": events_by_type_dict,
            "average_time_on_page": float(avg_time) if avg_time else None,
            "most_viewed_apartments": [
                {"apartment_id": apt_id, "views": views} 
                for apt_id, views in most_viewed
            ]
        }

    def get_apartment_analytics(self, apartment_id: int, days: int = 30) -> Dict[str, Any]:
        """Получить аналитику для конкретной квартиры"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Общее количество просмотров
        total_views = self.db.query(func.count(ApartmentEvent.id)).filter(
            ApartmentEvent.apartment_id == apartment_id,
            ApartmentEvent.event_type == 'view_apartment',
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Количество уникальных посетителей
        unique_visitors = self.db.query(func.count(func.distinct(ApartmentEvent.user_id))).filter(
            ApartmentEvent.apartment_id == apartment_id,
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Количество кликов по 3D туру
        clicks_3d_tour = self.db.query(func.count(ApartmentEvent.id)).filter(
            ApartmentEvent.apartment_id == apartment_id,
            ApartmentEvent.event_type == 'click_3d_tour',
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Количество кликов по бронированию
        clicks_book = self.db.query(func.count(ApartmentEvent.id)).filter(
            ApartmentEvent.apartment_id == apartment_id,
            ApartmentEvent.event_type == 'click_book',
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        # Среднее время на странице
        avg_time = self.db.query(func.avg(ApartmentEvent.event_value)).filter(
            ApartmentEvent.apartment_id == apartment_id,
            ApartmentEvent.event_type == 'time_on_page',
            ApartmentEvent.created_at >= start_date
        ).scalar()
        
        return {
            "apartment_id": apartment_id,
            "total_views": total_views,
            "unique_visitors": unique_visitors,
            "clicks_3d_tour": clicks_3d_tour,
            "clicks_book": clicks_book,
            "average_time_on_page": float(avg_time) if avg_time else None,
            "conversion_rate": (clicks_book / total_views * 100) if total_views > 0 else 0
        } 