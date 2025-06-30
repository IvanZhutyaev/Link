#!/usr/bin/env python3
"""
Тест для проверки ограничений бронирования
Проверяет, что пользователи могут бронировать только квартиры, а не ЖК
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from backend.Database.DB_connection import get_db
from backend.Models.All_models import Property, ResidentialComplex, Law_Face
from backend.Cruds.Property_crud import create_booking
from backend.Schemas.Property_schema import BookingModel

def test_booking_restrictions():
    """Тест ограничений бронирования"""
    db = next(get_db())
    
    try:
        # Создаем тестового застройщика
        developer = Law_Face(
            Company_name="Тестовый застройщик",
            INN=1234567890,
            OGRN=1234567890123,
            Adress="Тестовый адрес",
            User_name="test_developer",
            password="password123"
        )
        db.add(developer)
        db.commit()
        db.refresh(developer)
        
        # Создаем тестовый ЖК
        complex_obj = ResidentialComplex(
            name="Тестовый ЖК",
            address="Тестовый адрес ЖК",
            developer_name="Тестовый застройщик",
            zastroy_id=developer.id,
            city="Тестовый город",
            commissioning_date="2025",
            housing_class="Комфорт",
            status="Строится"
        )
        db.add(complex_obj)
        db.commit()
        db.refresh(complex_obj)
        
        # Создаем квартиру (с complex_id)
        apartment = Property(
            name="Квартира 1",
            address="Тестовый адрес, кв. 1",
            price=5000000,
            city="Тестовый город",
            is_available=True,
            zastroy_id=developer.id,
            complex_id=complex_obj.id,
            area=75.5,
            rooms=2,
            floor=5
        )
        db.add(apartment)
        db.commit()
        db.refresh(apartment)
        
        # Создаем ЖК как объект недвижимости (без complex_id)
        complex_as_property = Property(
            name="ЖК как объект",
            address="Тестовый адрес ЖК",
            price=100000000,
            city="Тестовый город",
            is_available=True,
            zastroy_id=developer.id,
            # complex_id = None (ЖК)
            area=1000.0,
            rooms=100,
            floor=1
        )
        db.add(complex_as_property)
        db.commit()
        db.refresh(complex_as_property)
        
        # Тест 1: Попытка забронировать квартиру (должно работать)
        try:
            booking_data = BookingModel(property_id=apartment.id)
            result = create_booking(db, user_id=1, booking_data=booking_data)
            print("✅ Тест 1 ПРОЙДЕН: Квартира успешно забронирована")
        except Exception as e:
            print(f"❌ Тест 1 ПРОВАЛЕН: Не удалось забронировать квартиру - {e}")
        
        # Тест 2: Попытка забронировать ЖК (должно не работать)
        try:
            booking_data = BookingModel(property_id=complex_as_property.id)
            result = create_booking(db, user_id=1, booking_data=booking_data)
            print("❌ Тест 2 ПРОВАЛЕН: ЖК забронирован, хотя не должен был")
        except ValueError as e:
            if "Можно бронировать только квартиры" in str(e):
                print("✅ Тест 2 ПРОЙДЕН: ЖК не удалось забронировать (ожидаемое поведение)")
            else:
                print(f"❌ Тест 2 ПРОВАЛЕН: Неожиданная ошибка - {e}")
        except Exception as e:
            print(f"❌ Тест 2 ПРОВАЛЕН: Неожиданная ошибка - {e}")
        
        print("\n🎉 Все тесты завершены!")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении тестов: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_booking_restrictions() 