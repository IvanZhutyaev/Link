#!/usr/bin/env python3
"""
Тест для проверки, что поиск по умолчанию показывает только квартиры
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from .Database.DB_connection import get_db
from .Models.All_models import Property, ResidentialComplex, Law_Face
from .Cruds.Property_crud import search_properties, get_properties
from .Schemas.Property_schema import PropertySearch

def test_search_only_apartments():
    """Тест, что поиск по умолчанию показывает только квартиры"""
    db = next(get_db())
    
    try:
        # Создаем тестового застройщика
        developer = Law_Face(
            Company_name="Тестовый застройщик",
            INN=1234567891,
            OGRN=1234567890124,
            Adress="Тестовый адрес",
            User_name="test_developer2",
            password="password123"
        )
        db.add(developer)
        db.commit()
        db.refresh(developer)
        
        # Создаем тестовый ЖК
        complex_obj = ResidentialComplex(
            name="Тестовый ЖК 2",
            address="Тестовый адрес ЖК 2",
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
            name="Квартира 2",
            address="Тестовый адрес, кв. 2",
            price=6000000,
            city="Тестовый город",
            is_available=True,
            zastroy_id=developer.id,
            complex_id=complex_obj.id,
            area=85.5,
            rooms=3,
            floor=7
        )
        db.add(apartment)
        db.commit()
        db.refresh(apartment)
        
        # Создаем ЖК как объект недвижимости (без complex_id)
        complex_as_property = Property(
            name="ЖК как объект 2",
            address="Тестовый адрес ЖК 2",
            price=200000000,
            city="Тестовый город",
            is_available=True,
            zastroy_id=developer.id,
            # complex_id = None (ЖК)
            area=2000.0,
            rooms=200,
            floor=1
        )
        db.add(complex_as_property)
        db.commit()
        db.refresh(complex_as_property)
        
        print(f"Созданы объекты:")
        print(f"- Квартира ID: {apartment.id}, complex_id: {apartment.complex_id}")
        print(f"- ЖК как объект ID: {complex_as_property.id}, complex_id: {complex_as_property.complex_id}")
        
        # Тест 1: Поиск без параметров (должен показать только квартиры)
        print("\n=== Тест 1: Поиск без параметров ===")
        search_params = PropertySearch()
        results = search_properties(db, search_params)
        print(f"Найдено объектов: {len(results)}")
        for prop in results:
            print(f"- {prop.name} (ID: {prop.id}, complex_id: {prop.complex_id})")
        
        # Проверяем, что все результаты - это квартиры
        all_apartments = all(prop.complex_id is not None for prop in results)
        if all_apartments:
            print("✅ Тест 1 ПРОЙДЕН: Поиск без параметров показывает только квартиры")
        else:
            print("❌ Тест 1 ПРОВАЛЕН: Поиск без параметров показал не только квартиры")
        
        # Тест 2: Поиск с complex_id='any' (должен показать только квартиры)
        print("\n=== Тест 2: Поиск с complex_id='any' ===")
        search_params = PropertySearch(complex_id='any')
        results = search_properties(db, search_params)
        print(f"Найдено объектов: {len(results)}")
        for prop in results:
            print(f"- {prop.name} (ID: {prop.id}, complex_id: {prop.complex_id})")
        
        # Проверяем, что все результаты - это квартиры
        all_apartments = all(prop.complex_id is not None for prop in results)
        if all_apartments:
            print("✅ Тест 2 ПРОЙДЕН: Поиск с complex_id='any' показывает только квартиры")
        else:
            print("❌ Тест 2 ПРОВАЛЕН: Поиск с complex_id='any' показал не только квартиры")
        
        # Тест 3: Поиск с конкретным complex_id
        print("\n=== Тест 3: Поиск с конкретным complex_id ===")
        search_params = PropertySearch(complex_id=str(complex_obj.id))
        results = search_properties(db, search_params)
        print(f"Найдено объектов: {len(results)}")
        for prop in results:
            print(f"- {prop.name} (ID: {prop.id}, complex_id: {prop.complex_id})")
        
        # Проверяем, что все результаты принадлежат указанному ЖК
        all_in_complex = all(prop.complex_id == complex_obj.id for prop in results)
        if all_in_complex:
            print("✅ Тест 3 ПРОЙДЕН: Поиск с конкретным complex_id показывает квартиры только из этого ЖК")
        else:
            print("❌ Тест 3 ПРОВАЛЕН: Поиск с конкретным complex_id показал квартиры не из этого ЖК")
        
        # Тест 4: Функция get_properties без параметров
        print("\n=== Тест 4: get_properties без параметров ===")
        results = get_properties(db)
        print(f"Найдено объектов: {len(results)}")
        for prop in results:
            print(f"- {prop.name} (ID: {prop.id}, complex_id: {prop.complex_id})")
        
        # Проверяем, что все результаты - это квартиры
        all_apartments = all(prop.complex_id is not None for prop in results)
        if all_apartments:
            print("✅ Тест 4 ПРОЙДЕН: get_properties без параметров показывает только квартиры")
        else:
            print("❌ Тест 4 ПРОВАЛЕН: get_properties без параметров показал не только квартиры")
        
        print("\n🎉 Все тесты завершены!")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении тестов: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_search_only_apartments() 