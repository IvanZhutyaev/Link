from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from Schemas.Property_schema import (
    PropertyModel, 
    PropertyResponse, 
    PropertySearch, 
    BookingModel, 
    BookingResponse,
    PurchaseModel,
    PurchaseResponse,
    MortgageModel,
    MortgageResponse,
    MortgageCalculationModel,
    MortgageCalculationResponse,
    RatingModel
)
from Cruds.Property_crud import (
    create_property,
    get_properties,
    get_property,
    search_properties,
    create_booking,
    get_user_bookings,
    cancel_booking,
    purchase_property,
    update_user_profile,
    create_purchase,
    get_user_purchases,
    create_mortgage,
    get_user_mortgages,
    approve_mortgage,
    reject_mortgage,
    calculate_mortgage_details,
    rate_property,
    mark_property_error
)
from Database.DB_connection import get_db
from Models.All_models import Property

router = APIRouter(prefix="/properties", tags=["Недвижимость"])


@router.get("/", response_model=List[PropertyResponse])
def read_properties(
    skip: int = 0, 
    limit: int = 100, 
    zastroy_id: int = None,
    complex_id: int = None,
    db: Session = Depends(get_db)
):
    """Получить список всей недвижимости или по застройщику/ЖК"""
    return get_properties(db, skip=skip, limit=limit, zastroy_id=zastroy_id, complex_id=complex_id)


@router.get("/search", response_model=List[PropertyResponse])
def search_properties_endpoint(
    city: Optional[str] = Query(None, description="Город"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    is_available: Optional[bool] = Query(True, description="Доступность"),
    complex_id: Optional[int] = Query(None, description="ID ЖК"),
    db: Session = Depends(get_db)
):
    """Поиск недвижимости по параметрам"""
    search_params = PropertySearch(
        city=city,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available,
        complex_id=complex_id
    )
    return search_properties(db, search_params)


@router.get("/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретной недвижимости"""
    db_property = get_property(db, property_id)
    if not db_property:
        raise HTTPException(status_code=404, detail="Недвижимость не найдена")
    return db_property


@router.post("/", response_model=PropertyResponse)
def create_new_property(property_data: PropertyModel, db: Session = Depends(get_db)):
    """Создать новую недвижимость (для застройщиков)"""
    try:
        return create_property(db, property_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Роуты для рейтингов
@router.post("/{property_id}/rate")
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


@router.post("/{property_id}/mark-error")
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


# Роуты для бронирований
@router.post("/book", response_model=BookingResponse)
def book_property(
    booking_data: BookingModel,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Забронировать недвижимость"""
    try:
        return create_booking(db, user_id, booking_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bookings/{user_id}", response_model=List[BookingResponse])
def get_bookings(user_id: int, db: Session = Depends(get_db)):
    """Получить все брони пользователя"""
    return get_user_bookings(db, user_id)


@router.post("/bookings/{booking_id}/cancel")
def cancel_booking_endpoint(
    booking_id: int,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Отменить бронь"""
    try:
        cancel_booking(db, booking_id, user_id)
        return {"message": "Бронь успешно отменена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bookings/{booking_id}/purchase")
def purchase_property_endpoint(
    booking_id: int,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Купить забронированную недвижимость"""
    try:
        purchase_property(db, booking_id, user_id)
        return {"message": "Недвижимость успешно куплена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Роуты для покупок
@router.post("/purchase", response_model=PurchaseResponse)
def purchase_property_direct(
    purchase_data: PurchaseModel,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Купить недвижимость напрямую"""
    try:
        return create_purchase(db, user_id, purchase_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/purchases/{user_id}", response_model=List[PurchaseResponse])
def get_purchases(user_id: int, db: Session = Depends(get_db)):
    """Получить все покупки пользователя"""
    return get_user_purchases(db, user_id)


# Роуты для ипотеки
@router.post("/mortgage", response_model=MortgageResponse)
def apply_mortgage(
    mortgage_data: MortgageModel,
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    """Подать заявку на ипотеку"""
    try:
        return create_mortgage(db, user_id, mortgage_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mortgages/{user_id}", response_model=List[MortgageResponse])
def get_mortgages(user_id: int, db: Session = Depends(get_db)):
    """Получить все ипотечные заявки пользователя"""
    return get_user_mortgages(db, user_id)


@router.post("/mortgages/{mortgage_id}/approve")
def approve_mortgage_endpoint(
    mortgage_id: int,
    db: Session = Depends(get_db)
):
    """Одобрить ипотечную заявку (для администраторов)"""
    try:
        approve_mortgage(db, mortgage_id)
        return {"message": "Ипотечная заявка одобрена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mortgages/{mortgage_id}/reject")
def reject_mortgage_endpoint(
    mortgage_id: int,
    db: Session = Depends(get_db)
):
    """Отклонить ипотечную заявку (для администраторов)"""
    try:
        reject_mortgage(db, mortgage_id)
        return {"message": "Ипотечная заявка отклонена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mortgage/calculate", response_model=MortgageCalculationResponse)
def calculate_mortgage(
    calculation_data: MortgageCalculationModel,
    db: Session = Depends(get_db)
):
    """Рассчитать ипотеку"""
    try:
        return calculate_mortgage_details(calculation_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 