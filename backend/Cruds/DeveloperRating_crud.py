from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.Models.All_models import DeveloperRating, Law_Face, Property, ResidentialComplex


def get_developer_rating(db: Session, law_face_id: int):
    """Получить рейтинг застройщика"""
    return db.query(DeveloperRating).filter(DeveloperRating.law_face_id == law_face_id).first()


def create_developer_rating(db: Session, law_face_id: int, rating: float = 0.0, completed_projects: int = 0, years_on_market: int = 0):
    """Создать рейтинг застройщика"""
    db_rating = DeveloperRating(
        law_face_id=law_face_id,
        rating=rating,
        completed_projects=completed_projects,
        years_on_market=years_on_market
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def update_developer_rating(db: Session, law_face_id: int, rating: float = None, completed_projects: int = None, years_on_market: int = None):
    """Обновить рейтинг застройщика"""
    db_rating = get_developer_rating(db, law_face_id)
    if not db_rating:
        return create_developer_rating(db, law_face_id, rating or 0.0, completed_projects or 0, years_on_market or 0)
    
    if rating is not None:
        db_rating.rating = rating
    if completed_projects is not None:
        db_rating.completed_projects = completed_projects
    if years_on_market is not None:
        db_rating.years_on_market = years_on_market
    
    db.commit()
    db.refresh(db_rating)
    return db_rating


def calculate_developer_rating(db: Session, law_face_id: int):
    """Рассчитать рейтинг застройщика на основе его объектов"""
    # Получаем все объекты застройщика
    properties = db.query(Property).filter(Property.zastroy_id == law_face_id).all()
    complexes = db.query(ResidentialComplex).filter(ResidentialComplex.zastroy_id == law_face_id).all()
    
    # Рассчитываем средний рейтинг объектов
    total_rating = 0
    rating_count = 0
    
    # Рейтинг квартир
    for property in properties:
        if property.rating and property.rating > 0:
            total_rating += property.rating
            rating_count += 1
    
    # Рейтинг ЖК
    for complex in complexes:
        if complex.rating and complex.rating > 0:
            total_rating += complex.rating
            rating_count += 1
    
    # Базовый рейтинг застройщика
    base_rating = 8.0
    
    # Если есть оценки объектов, учитываем их
    if rating_count > 0:
        average_object_rating = total_rating / rating_count
        # Взвешенный рейтинг: 70% от объектов + 30% базовый
        final_rating = (average_object_rating * 0.7) + (base_rating * 0.3)
    else:
        final_rating = base_rating
    
    # Ограничиваем рейтинг от 0 до 10
    final_rating = max(0.0, min(10.0, final_rating))
    
    return round(final_rating, 1)


def get_developer_stats(db: Session, law_face_id: int):
    """Получить статистику застройщика"""
    # Количество объектов
    properties_count = db.query(Property).filter(Property.zastroy_id == law_face_id).count()
    complexes_count = db.query(ResidentialComplex).filter(ResidentialComplex.zastroy_id == law_face_id).count()
    
    # Средний рейтинг объектов
    avg_property_rating = db.query(func.avg(Property.rating)).filter(
        Property.zastroy_id == law_face_id,
        Property.rating > 0
    ).scalar() or 0.0
    
    avg_complex_rating = db.query(func.avg(ResidentialComplex.rating)).filter(
        ResidentialComplex.zastroy_id == law_face_id,
        ResidentialComplex.rating > 0
    ).scalar() or 0.0
    
    # Общий средний рейтинг
    total_ratings = []
    if avg_property_rating > 0:
        total_ratings.append(avg_property_rating)
    if avg_complex_rating > 0:
        total_ratings.append(avg_complex_rating)
    
    overall_rating = sum(total_ratings) / len(total_ratings) if total_ratings else 0.0
    
    return {
        "properties_count": properties_count,
        "complexes_count": complexes_count,
        "avg_property_rating": round(avg_property_rating, 1),
        "avg_complex_rating": round(avg_complex_rating, 1),
        "overall_rating": round(overall_rating, 1)
    }


def get_top_developers(db: Session, limit: int = 10):
    """Получить топ застройщиков по рейтингу"""
    return db.query(DeveloperRating, Law_Face).join(
        Law_Face, DeveloperRating.law_face_id == Law_Face.id
    ).order_by(DeveloperRating.rating.desc()).limit(limit).all() 