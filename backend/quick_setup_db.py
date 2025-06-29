#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый скрипт для создания базы данных
Использование: python quick_setup_db.py
"""

import sys
import os
from sqlalchemy import text

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.DB_connection import engine, base
from Models.All_models import *

def quick_setup():
    """Быстрая настройка базы данных"""
    print("🚀 Быстрая настройка базы данных...")
    
    try:
        # Создаем все таблицы
        print("🔨 Создаю таблицы...")
        base.metadata.create_all(engine)
        print("✅ Таблицы созданы")
        
        # Добавляем недостающие столбцы
        print("🔧 Добавляю недостающие столбцы...")
        with engine.connect() as conn:
            # Столбцы для Properties
            try:
                conn.execute(text("ALTER TABLE Properties ADD COLUMN rating FLOAT DEFAULT 0.0"))
                print("✅ Добавлен столбец rating в Properties")
            except:
                pass
                
            try:
                conn.execute(text("ALTER TABLE Properties ADD COLUMN rating_count INTEGER DEFAULT 0"))
                print("✅ Добавлен столбец rating_count в Properties")
            except:
                pass
                
            try:
                conn.execute(text("ALTER TABLE Properties ADD COLUMN has_error BOOLEAN DEFAULT FALSE"))
                print("✅ Добавлен столбец has_error в Properties")
            except:
                pass
                
            try:
                conn.execute(text("ALTER TABLE Properties ADD COLUMN status VARCHAR DEFAULT 'available'"))
                print("✅ Добавлен столбец status в Properties")
            except:
                pass
            
            # Столбцы для residential_complexes
            try:
                conn.execute(text("ALTER TABLE residential_complexes ADD COLUMN rating FLOAT DEFAULT 0.0"))
                print("✅ Добавлен столбец rating в residential_complexes")
            except:
                pass
                
            try:
                conn.execute(text("ALTER TABLE residential_complexes ADD COLUMN rating_count INTEGER DEFAULT 0"))
                print("✅ Добавлен столбец rating_count в residential_complexes")
            except:
                pass
            
            # Столбцы для Bookings
            try:
                conn.execute(text("ALTER TABLE Bookings ADD COLUMN expires_at DATETIME"))
                print("✅ Добавлен столбец expires_at в Bookings")
            except:
                pass
            
            # Столбцы для Purchases
            try:
                conn.execute(text("ALTER TABLE Purchases ADD COLUMN booking_id INTEGER REFERENCES Bookings(id)"))
                print("✅ Добавлен столбец booking_id в Purchases")
            except:
                pass
            
            # Столбцы для Mortgages
            try:
                conn.execute(text("ALTER TABLE Mortgages ADD COLUMN booking_id INTEGER REFERENCES Bookings(id)"))
                print("✅ Добавлен столбец booking_id в Mortgages")
            except:
                pass
                
            try:
                conn.execute(text("ALTER TABLE Mortgages ADD COLUMN approved_date DATETIME"))
                print("✅ Добавлен столбец approved_date в Mortgages")
            except:
                pass
            
            conn.commit()
        
        # Создаем индексы
        print("📊 Создаю индексы...")
        with engine.connect() as conn:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_properties_city ON Properties(city)",
                "CREATE INDEX IF NOT EXISTS idx_properties_price ON Properties(price)",
                "CREATE INDEX IF NOT EXISTS idx_properties_zastroy_id ON Properties(zastroy_id)",
                "CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON Bookings(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_bookings_property_id ON Bookings(property_id)",
                "CREATE INDEX IF NOT EXISTS idx_purchases_user_id ON Purchases(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_mortgages_user_id ON Mortgages(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_apartment_events_apartment_id ON apartment_events(apartment_id)",
                "CREATE INDEX IF NOT EXISTS idx_apartment_events_created_at ON apartment_events(created_at)"
            ]
            
            for index_sql in indexes:
                try:
                    conn.execute(text(index_sql))
                except:
                    pass
            
            conn.commit()
        
        print("🎉 База данных успешно настроена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = quick_setup()
    if not success:
        sys.exit(1) 