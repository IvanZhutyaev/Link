#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания всех таблиц и столбцов в базе данных
Автор: AI Assistant
Дата создания: 2024
"""

import sys
import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from environs import Env

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.DB_connection import engine, base
from Models.All_models import *

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_creation.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Проверяет подключение к базе данных"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Подключение к базе данных успешно")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        return False

def get_existing_tables():
    """Получает список существующих таблиц"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"📋 Найдено существующих таблиц: {len(tables)}")
        for table in tables:
            logger.info(f"   - {table}")
        return tables
    except Exception as e:
        logger.error(f"❌ Ошибка при получении списка таблиц: {e}")
        return []

def create_all_tables():
    """Создает все таблицы в базе данных"""
    try:
        logger.info("🔨 Начинаю создание всех таблиц...")
        base.metadata.create_all(engine)
        logger.info("✅ Все таблицы успешно созданы")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при создании таблиц: {e}")
        return False

def drop_all_tables():
    """Удаляет все таблицы из базы данных"""
    try:
        logger.warning("🗑️ Удаляю все существующие таблицы...")
        base.metadata.drop_all(engine)
        logger.info("✅ Все таблицы удалены")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка при удалении таблиц: {e}")
        return False

def add_missing_columns():
    """Добавляет недостающие столбцы в существующие таблицы"""
    logger.info("🔧 Проверяю и добавляю недостающие столбцы...")
    
    columns_to_add = {
        'Properties': [
            ('rating', 'FLOAT DEFAULT 0.0'),
            ('rating_count', 'INTEGER DEFAULT 0'),
            ('has_error', 'BOOLEAN DEFAULT FALSE'),
            ('status', 'VARCHAR DEFAULT \'available\'')
        ],
        'residential_complexes': [
            ('rating', 'FLOAT DEFAULT 0.0'),
            ('rating_count', 'INTEGER DEFAULT 0')
        ],
        'Bookings': [
            ('expires_at', 'DATETIME')
        ],
        'Purchases': [
            ('booking_id', 'INTEGER REFERENCES Bookings(id)')
        ],
        'Mortgages': [
            ('booking_id', 'INTEGER REFERENCES Bookings(id)'),
            ('approved_date', 'DATETIME')
        ]
    }
    
    try:
        with engine.connect() as conn:
            for table_name, columns in columns_to_add.items():
                for column_name, column_definition in columns:
                    try:
                        # Проверяем, существует ли столбец
                        result = conn.execute(text(f"""
                            SELECT COUNT(*) FROM pragma_table_info('{table_name}') 
                            WHERE name = '{column_name}'
                        """))
                        column_exists = result.scalar() > 0
                        
                        if not column_exists:
                            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"))
                            logger.info(f"✅ Добавлен столбец {column_name} в таблицу {table_name}")
                        else:
                            logger.info(f"ℹ️ Столбец {column_name} уже существует в таблице {table_name}")
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Не удалось добавить столбец {column_name} в таблицу {table_name}: {e}")
            
            conn.commit()
            logger.info("✅ Проверка и добавление столбцов завершены")
            
    except Exception as e:
        logger.error(f"❌ Ошибка при добавлении столбцов: {e}")

def verify_table_structure():
    """Проверяет структуру созданных таблиц"""
    logger.info("🔍 Проверяю структуру созданных таблиц...")
    
    expected_tables = [
        'Law_faces', 'Users', 'Properties', 'Bookings', 'Purchases', 
        'Mortgages', 'residential_complexes', 'apartment_events', 'developer_ratings'
    ]
    
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        for table in expected_tables:
            if table in existing_tables:
                columns = inspector.get_columns(table)
                logger.info(f"✅ Таблица {table} создана с {len(columns)} столбцами")
                for col in columns:
                    logger.info(f"   - {col['name']}: {col['type']}")
            else:
                logger.warning(f"⚠️ Таблица {table} не найдена")
                
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке структуры таблиц: {e}")

def create_indexes():
    """Создает индексы для улучшения производительности"""
    logger.info("📊 Создаю индексы для улучшения производительности...")
    
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
    
    try:
        with engine.connect() as conn:
            for index_sql in indexes:
                try:
                    conn.execute(text(index_sql))
                    logger.info(f"✅ Создан индекс: {index_sql.split('ON')[1].strip()}")
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось создать индекс: {e}")
            conn.commit()
            
    except Exception as e:
        logger.error(f"❌ Ошибка при создании индексов: {e}")

def main():
    """Основная функция создания базы данных"""
    logger.info("🚀 Начинаю процесс создания базы данных...")
    logger.info(f"📅 Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Проверяем подключение к базе данных
    if not check_database_connection():
        logger.error("❌ Не удалось подключиться к базе данных. Завершение работы.")
        return False
    
    # Получаем список существующих таблиц
    existing_tables = get_existing_tables()
    
    # Спрашиваем пользователя о действии
    if existing_tables:
        print("\n" + "="*60)
        print("В базе данных уже существуют таблицы:")
        for table in existing_tables:
            print(f"  - {table}")
        print("="*60)
        
        choice = input("\nВыберите действие:\n"
                      "1. Пересоздать все таблицы (удалить существующие и создать новые)\n"
                      "2. Создать только недостающие таблицы\n"
                      "3. Только добавить недостающие столбцы\n"
                      "4. Отмена\n"
                      "Введите номер (1-4): ").strip()
        
        if choice == "1":
            if not drop_all_tables():
                return False
            if not create_all_tables():
                return False
        elif choice == "2":
            if not create_all_tables():
                return False
        elif choice == "3":
            add_missing_columns()
        elif choice == "4":
            logger.info("❌ Операция отменена пользователем")
            return False
        else:
            logger.error("❌ Неверный выбор")
            return False
    else:
        # Создаем все таблицы, если их нет
        if not create_all_tables():
            return False
    
    # Добавляем недостающие столбцы
    add_missing_columns()
    
    # Создаем индексы
    create_indexes()
    
    # Проверяем структуру
    verify_table_structure()
    
    logger.info("🎉 База данных успешно создана и настроена!")
    logger.info("📝 Лог сохранен в файл: database_creation.log")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ База данных успешно создана!")
        else:
            print("\n❌ Произошла ошибка при создании базы данных")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("❌ Операция прервана пользователем")
        print("\n❌ Операция прервана пользователем")
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}")
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1) 