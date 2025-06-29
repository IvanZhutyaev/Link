import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from Database.DB_connection import engine, base
from Models.All_models import *

def recreate_tables():
    """Пересоздает все таблицы в базе данных"""
    
    # Удаляем все таблицы
    base.metadata.drop_all(engine)
    print("Все таблицы удалены")
    
    # Создаем все таблицы заново
    base.metadata.create_all(engine)
    print("Все таблицы созданы заново")
    
    # Добавляем новые столбцы если их нет
    with engine.connect() as conn:
        # Проверяем и добавляем столбцы для рейтинга квартир
        try:
            conn.execute(text("ALTER TABLE Properties ADD COLUMN rating FLOAT DEFAULT 0.0"))
            print("Добавлен столбец rating в таблицу Properties")
        except:
            print("Столбец rating уже существует в таблице Properties")
        
        try:
            conn.execute(text("ALTER TABLE Properties ADD COLUMN rating_count INTEGER DEFAULT 0"))
            print("Добавлен столбец rating_count в таблицу Properties")
        except:
            print("Столбец rating_count уже существует в таблице Properties")
        
        try:
            conn.execute(text("ALTER TABLE Properties ADD COLUMN has_error BOOLEAN DEFAULT FALSE"))
            print("Добавлен столбец has_error в таблицу Properties")
        except:
            print("Столбец has_error уже существует в таблице Properties")
        
        # Проверяем и добавляем столбцы для рейтинга ЖК
        try:
            conn.execute(text("ALTER TABLE residential_complexes ADD COLUMN rating FLOAT DEFAULT 0.0"))
            print("Добавлен столбец rating в таблицу residential_complexes")
        except:
            print("Столбец rating уже существует в таблице residential_complexes")
        
        try:
            conn.execute(text("ALTER TABLE residential_complexes ADD COLUMN rating_count INTEGER DEFAULT 0"))
            print("Добавлен столбец rating_count в таблицу residential_complexes")
        except:
            print("Столбец rating_count уже существует в таблице residential_complexes")
        
        conn.commit()
    
    print("База данных успешно обновлена!")

if __name__ == "__main__":
    recreate_tables() 