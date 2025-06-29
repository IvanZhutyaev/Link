import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.DB_connection import engine
from sqlalchemy import inspect, text
from Models.All_models import ResidentialComplex
from sqlalchemy.orm import Session

def fix_database():
    """Исправляет проблемы с базой данных"""
    try:
        with engine.connect() as conn:
            # Изменяем тип столбца price на bigint
            print("Изменяем тип столбца price...")
            conn.execute(text('ALTER TABLE "Properties" ALTER COLUMN price TYPE bigint USING price::bigint;'))
            
            # Добавляем столбец booking_date если его нет
            print("Проверяем столбец booking_date...")
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'Bookings' AND column_name = 'booking_date'
            """))
            if not result.fetchone():
                print("Добавляем столбец booking_date...")
                conn.execute(text('ALTER TABLE "Bookings" ADD COLUMN booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;'))
            
            # Добавляем столбцы complex_id и zastroy_id если их нет
            print("Проверяем столбцы complex_id и zastroy_id...")
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'Properties' AND column_name = 'complex_id'
            """))
            if not result.fetchone():
                print("Добавляем столбец complex_id...")
                conn.execute(text('ALTER TABLE "Properties" ADD COLUMN complex_id INTEGER REFERENCES residential_complexes(id);'))
            
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'Properties' AND column_name = 'zastroy_id'
            """))
            if not result.fetchone():
                print("Добавляем столбец zastroy_id...")
                conn.execute(text('ALTER TABLE "Properties" ADD COLUMN zastroy_id INTEGER REFERENCES "Law_faces"(id);'))
            
            # Проверяем таблицу apartment_events
            print("Проверяем таблицу apartment_events...")
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_name = 'apartment_events'
            """))
            if not result.fetchone():
                print("Создаем таблицу apartment_events...")
                conn.execute(text('''
                    CREATE TABLE apartment_events (
                        id SERIAL PRIMARY KEY,
                        apartment_id INTEGER NOT NULL,
                        user_id VARCHAR(255) NOT NULL,
                        event_type VARCHAR(100) NOT NULL,
                        event_value FLOAT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                '''))
            
            conn.commit()
            print("База данных успешно исправлена!")
            
    except Exception as e:
        print(f"Ошибка при исправлении базы данных: {e}")
        print(f"Тип ошибки: {type(e)}")

def add_avaline_url_column():
    with engine.connect() as conn:
        # Проверяем, есть ли уже столбец
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name='residential_complexes' AND column_name='avaline_url'
        """))
        if result.fetchone() is None:
            print("Добавляю столбец avaline_url в residential_complexes...")
            conn.execute(text("""
                ALTER TABLE residential_complexes ADD COLUMN avaline_url VARCHAR;
            """))
            print("Готово!")
        else:
            print("Столбец avaline_url уже существует.")

if __name__ == "__main__":
    fix_database()
    add_avaline_url_column() 