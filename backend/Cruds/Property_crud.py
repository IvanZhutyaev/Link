from sqlalchemy.orm import Session
from sqlalchemy import and_
from Models.All_models import Property, Booking, User, Purchase, Mortgage
from Schemas.Property_schema import (
    PropertyModel, PropertySearch, BookingModel, 
    PurchaseModel, MortgageModel, MortgageCalculationModel
)
from typing import List, Optional
from datetime import datetime, timedelta
import math


def create_property(db: Session, property_data: PropertyModel) -> Property:
    try:
        print(f"Создание недвижимости с данными: {property_data.dict()}")
        
        data = property_data.dict()
        # Если complex_id или zastroy_id есть в data, добавляем их явно
        if 'complex_id' in data:
            data['complex_id'] = data['complex_id']
        if 'zastroy_id' in data:
            data['zastroy_id'] = data['zastroy_id']
        
        print(f"Подготовленные данные для создания: {data}")
        
        db_property = Property(**data)
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        
        print(f"Недвижимость успешно создана с ID: {db_property.id}")
        return db_property
        
    except Exception as e:
        print(f"Ошибка при создании недвижимости: {e}")
        print(f"Тип ошибки: {type(e)}")
        import traceback
        print(f"Стек ошибки: {traceback.format_exc()}")
        db.rollback()
        raise ValueError(f"Ошибка при создании недвижимости: {str(e)}")


def get_properties(db: Session, skip: int = 0, limit: int = 100, zastroy_id: int = None, complex_id: int = None) -> List[Property]:
    query = db.query(Property)
    if zastroy_id is not None:
        query = query.filter(Property.zastroy_id == zastroy_id)
    if complex_id is not None:
        query = query.filter(Property.complex_id == complex_id)
    return query.offset(skip).limit(limit).all()


def get_properties_by_complex(db: Session, complex_id: int, skip: int = 0, limit: int = 100) -> List[Property]:
    """Получить квартиры в конкретном ЖК"""
    return db.query(Property).filter(
        and_(
            Property.complex_id == complex_id,
            Property.is_available == True,
            Property.has_error == False
        )
    ).offset(skip).limit(limit).all()


def get_property(db: Session, property_id: int) -> Optional[Property]:
    return db.query(Property).filter(Property.id == property_id).first()


def search_properties(db: Session, search_params: PropertySearch) -> List[Property]:
    query = db.query(Property)
    
    # Фильтр по городу
    if search_params.city:
        query = query.filter(Property.city.ilike(f"%{search_params.city}%"))
    
    # Фильтр по цене
    if search_params.min_price is not None:
        query = query.filter(Property.price >= search_params.min_price)
    if search_params.max_price is not None:
        query = query.filter(Property.price <= search_params.max_price)
    
    # Фильтр по количеству комнат
    if search_params.rooms is not None:
        query = query.filter(Property.rooms == search_params.rooms)
    
    # Фильтр по площади
    if search_params.min_area is not None:
        query = query.filter(Property.area >= search_params.min_area)
    if search_params.max_area is not None:
        query = query.filter(Property.area <= search_params.max_area)
    
    # Фильтр по доступности
    if search_params.is_available is not None:
        query = query.filter(Property.is_available == search_params.is_available)
    
    # Фильтр по ЖК (complex_id)
    if search_params.complex_id is not None:
        if search_params.complex_id == 'any':
            # Ищем только квартиры (объекты с complex_id)
            query = query.filter(Property.complex_id.isnot(None))
        else:
            # Ищем квартиры в конкретном ЖК
            query = query.filter(Property.complex_id == search_params.complex_id)
    
    return query.all()


def rate_property(db: Session, property_id: int, rating: float) -> bool:
    """Оценить квартиру"""
    property_obj = get_property(db, property_id)
    if not property_obj:
        raise ValueError("Квартира не найдена")
    
    if rating < 1.0 or rating > 5.0:
        raise ValueError("Рейтинг должен быть от 1 до 5")
    
    # Обновляем рейтинг
    if property_obj.rating is None:
        property_obj.rating = rating
        property_obj.rating_count = 1
    else:
        total_rating = property_obj.rating * property_obj.rating_count + rating
        property_obj.rating_count += 1
        property_obj.rating = total_rating / property_obj.rating_count
    
    db.commit()
    return True


def mark_property_error(db: Session, property_id: int) -> bool:
    """Пометить квартиру как имеющую ошибку"""
    property_obj = get_property(db, property_id)
    if not property_obj:
        raise ValueError("Квартира не найдена")
    
    property_obj.has_error = True
    property_obj.is_available = False
    db.commit()
    return True


def create_booking(db: Session, user_id: int, booking_data: BookingModel) -> Booking:
    # Проверяем, что недвижимость доступна
    property_obj = get_property(db, booking_data.property_id)
    if not property_obj or not property_obj.is_available or property_obj.has_error:
        raise ValueError("Недвижимость недоступна для бронирования")
    
    # Проверяем, что это квартира (должна быть привязана к ЖК)
    if not property_obj.complex_id:
        raise ValueError("Можно бронировать только квартиры, а не жилые комплексы")
    
    # Проверяем, что у пользователя нет активной брони на эту недвижимость
    existing_booking = db.query(Booking).filter(
        and_(
            Booking.user_id == user_id,
            Booking.property_id == booking_data.property_id,
            Booking.status == "booked"
        )
    ).first()
    
    if existing_booking:
        raise ValueError("У вас уже есть активная бронь на эту квартиру")
    
    # Устанавливаем срок действия брони (например, 7 дней)
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    db_booking = Booking(
        user_id=user_id,
        property_id=booking_data.property_id,
        status="booked",
        expires_at=expires_at
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_user_bookings(db: Session, user_id: int) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def cancel_booking(db: Session, booking_id: int, user_id: int) -> bool:
    booking = db.query(Booking).filter(
        and_(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == "booked"
        )
    ).first()
    
    if not booking:
        raise ValueError("Бронь не найдена или уже отменена")
    
    booking.status = "cancelled"
    db.commit()
    return True


def create_purchase(db: Session, user_id: int, purchase_data: PurchaseModel) -> Purchase:
    # Проверяем, что недвижимость доступна
    property_obj = get_property(db, purchase_data.property_id)
    if not property_obj or not property_obj.is_available or property_obj.has_error:
        raise ValueError("Недвижимость недоступна для покупки")
    
    # Проверяем, что это квартира (должна быть привязана к ЖК)
    if not property_obj.complex_id:
        raise ValueError("Можно покупать только квартиры, а не жилые комплексы")
    
    # Проверяем, что у пользователя нет активной покупки на эту недвижимость
    existing_purchase = db.query(Purchase).filter(
        and_(
            Purchase.user_id == user_id,
            Purchase.property_id == purchase_data.property_id,
            Purchase.status.in_(["pending", "completed"])
        )
    ).first()
    
    if existing_purchase:
        raise ValueError("У вас уже есть активная покупка на эту квартиру")
    
    # Создаем покупку
    db_purchase = Purchase(
        user_id=user_id,
        property_id=purchase_data.property_id,
        purchase_price=purchase_data.purchase_price,
        payment_method=purchase_data.payment_method,
        status="completed",
        booking_id=purchase_data.booking_id
    )
    
    # Делаем недвижимость недоступной и устанавливаем владельца
    property_obj.is_available = False
    property_obj.owner_id = user_id
    
    # Если есть бронирование, обновляем его статус
    if purchase_data.booking_id:
        booking = db.query(Booking).filter(Booking.id == purchase_data.booking_id).first()
        if booking:
            booking.status = "converted_to_purchase"
    
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_user_purchases(db: Session, user_id: int) -> List[Purchase]:
    return db.query(Purchase).filter(Purchase.user_id == user_id).all()


def create_mortgage(db: Session, user_id: int, mortgage_data: MortgageModel) -> Mortgage:
    # Проверяем, что недвижимость доступна
    property_obj = get_property(db, mortgage_data.property_id)
    if not property_obj or not property_obj.is_available or property_obj.has_error:
        raise ValueError("Недвижимость недоступна для ипотеки")
    
    # Проверяем, что это квартира (должна быть привязана к ЖК)
    if not property_obj.complex_id:
        raise ValueError("Можно оформить ипотеку только на квартиры, а не на жилые комплексы")
    
    # Проверяем, что у пользователя нет активной ипотечной заявки на эту недвижимость
    existing_mortgage = db.query(Mortgage).filter(
        and_(
            Mortgage.user_id == user_id,
            Mortgage.property_id == mortgage_data.property_id,
            Mortgage.status.in_(["pending", "approved", "active"])
        )
    ).first()
    
    if existing_mortgage:
        raise ValueError("У вас уже есть активная ипотечная заявка на эту квартиру")
    
    # Рассчитываем ежемесячный платеж
    monthly_payment = calculate_monthly_payment(
        mortgage_data.loan_amount,
        mortgage_data.interest_rate,
        mortgage_data.loan_term_years
    )
    
    # Создаем ипотечную заявку
    db_mortgage = Mortgage(
        user_id=user_id,
        property_id=mortgage_data.property_id,
        loan_amount=mortgage_data.loan_amount,
        down_payment=mortgage_data.down_payment,
        interest_rate=mortgage_data.interest_rate,
        loan_term_years=mortgage_data.loan_term_years,
        monthly_payment=monthly_payment,
        status="pending",
        bank_name=mortgage_data.bank_name,
        application_notes=mortgage_data.application_notes,
        booking_id=mortgage_data.booking_id
    )
    
    db.add(db_mortgage)
    db.commit()
    db.refresh(db_mortgage)
    return db_mortgage


def get_user_mortgages(db: Session, user_id: int) -> List[Mortgage]:
    return db.query(Mortgage).filter(Mortgage.user_id == user_id).all()


def approve_mortgage(db: Session, mortgage_id: int) -> bool:
    mortgage = db.query(Mortgage).filter(Mortgage.id == mortgage_id).first()
    if not mortgage:
        raise ValueError("Ипотечная заявка не найдена")
    
    mortgage.status = "approved"
    mortgage.approved_date = datetime.utcnow()
    db.commit()
    return True


def reject_mortgage(db: Session, mortgage_id: int) -> bool:
    mortgage = db.query(Mortgage).filter(Mortgage.id == mortgage_id).first()
    if not mortgage:
        raise ValueError("Ипотечная заявка не найдена")
    
    mortgage.status = "rejected"
    db.commit()
    return True


def calculate_monthly_payment(loan_amount: int, interest_rate: float, loan_term_years: int) -> float:
    """Рассчитать ежемесячный платеж по ипотеке"""
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term_years * 12
    
    if monthly_rate == 0:
        return loan_amount / num_payments
    
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return round(monthly_payment, 2)


def calculate_mortgage_details(calculation_data: MortgageCalculationModel) -> dict:
    """Рассчитать детали ипотеки"""
    down_payment = int(calculation_data.property_price * calculation_data.down_payment_percent / 100)
    loan_amount = calculation_data.property_price - down_payment
    monthly_payment = calculate_monthly_payment(
        loan_amount,
        calculation_data.interest_rate,
        calculation_data.loan_term_years
    )
    
    total_payment = monthly_payment * calculation_data.loan_term_years * 12
    total_interest = total_payment - loan_amount
    
    return {
        "loan_amount": loan_amount,
        "down_payment": down_payment,
        "monthly_payment": monthly_payment,
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }


def purchase_property(db: Session, booking_id: int, user_id: int) -> bool:
    """Купить забронированную недвижимость"""
    booking = db.query(Booking).filter(
        and_(
            Booking.id == booking_id,
            Booking.user_id == user_id,
            Booking.status == "booked"
        )
    ).first()
    
    if not booking:
        raise ValueError("Бронь не найдена или уже отменена")
    
    # Создаем покупку
    property_obj = get_property(db, booking.property_id)
    if not property_obj or not property_obj.is_available:
        raise ValueError("Квартира недоступна для покупки")
    
    # Проверяем, что это квартира (должна быть привязана к ЖК)
    if not property_obj.complex_id:
        raise ValueError("Можно покупать только квартиры, а не жилые комплексы")
    
    db_purchase = Purchase(
        user_id=user_id,
        property_id=booking.property_id,
        purchase_price=property_obj.price,  # Используем цену из объекта недвижимости
        payment_method="cash",  # По умолчанию наличные
        status="completed",
        booking_id=booking_id
    )
    
    # Делаем недвижимость недоступной и устанавливаем владельца
    property_obj.is_available = False
    property_obj.owner_id = user_id
    
    # Обновляем статус брони
    booking.status = "converted_to_purchase"
    
    db.add(db_purchase)
    db.commit()
    return True


def update_user_profile(db: Session, user_id: int, name: str, phone: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Пользователь не найден")
    
    user.User_name = name
    user.Phone_number = phone
    db.commit()
    db.refresh(user)
    return user 