import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.DB_connection import engine
from sqlalchemy import text
import subprocess
import time

def fix_database_final():
    """Финальное исправление базы данных"""
    try:
        print("🔧 Исправляем базу данных...")
        
        with engine.connect() as conn:
            # 1. Исправляем тип столбца price
            print("1. Исправляем тип столбца price...")
            try:
                conn.execute(text('ALTER TABLE "Properties" ALTER COLUMN price TYPE bigint USING price::bigint;'))
                print("   ✅ Тип столбца price исправлен")
            except Exception as e:
                print(f"   ⚠️ Ошибка с price: {e}")
            
            # 2. Добавляем недостающие столбцы в Properties
            print("2. Проверяем столбцы Properties...")
            columns_to_add = [
                ('complex_id', 'INTEGER REFERENCES residential_complexes(id)'),
                ('zastroy_id', 'INTEGER REFERENCES "Law_faces"(id)')
            ]
            
            for col_name, col_type in columns_to_add:
                try:
                    result = conn.execute(text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = 'Properties' AND column_name = '{col_name}'
                    """))
                    if not result.fetchone():
                        conn.execute(text(f'ALTER TABLE "Properties" ADD COLUMN {col_name} {col_type};'))
                        print(f"   ✅ Добавлен столбец {col_name}")
                    else:
                        print(f"   ✅ Столбец {col_name} уже существует")
                except Exception as e:
                    print(f"   ⚠️ Ошибка с {col_name}: {e}")
            
            # 3. Исправляем таблицу Bookings
            print("3. Исправляем таблицу Bookings...")
            try:
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'Bookings' AND column_name = 'booking_date'
                """))
                if not result.fetchone():
                    conn.execute(text('ALTER TABLE "Bookings" ADD COLUMN booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;'))
                    print("   ✅ Добавлен столбец booking_date")
                else:
                    print("   ✅ Столбец booking_date уже существует")
            except Exception as e:
                print(f"   ⚠️ Ошибка с booking_date: {e}")
            
            # 4. Создаем таблицу apartment_events если её нет
            print("4. Проверяем таблицу apartment_events...")
            try:
                result = conn.execute(text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'apartment_events'
                """))
                if not result.fetchone():
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
                    print("   ✅ Создана таблица apartment_events")
                else:
                    print("   ✅ Таблица apartment_events уже существует")
            except Exception as e:
                print(f"   ⚠️ Ошибка с apartment_events: {e}")
            
            # 5. Добавляем недостающие столбцы в residential_complexes
            print("5. Проверяем столбцы residential_complexes...")
            try:
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'residential_complexes' AND column_name = 'zastroy_id'
                """))
                if not result.fetchone():
                    conn.execute(text('ALTER TABLE residential_complexes ADD COLUMN zastroy_id INTEGER REFERENCES "Law_faces"(id);'))
                    print("   ✅ Добавлен столбец zastroy_id в residential_complexes")
                else:
                    print("   ✅ Столбец zastroy_id уже существует в residential_complexes")
            except Exception as e:
                print(f"   ⚠️ Ошибка с zastroy_id в residential_complexes: {e}")
            
            conn.commit()
            print("✅ База данных успешно исправлена!")
            
    except Exception as e:
        print(f"❌ Критическая ошибка при исправлении базы данных: {e}")
        return False
    
    return True

def start_server():
    """Запускает сервер"""
    print("\n🚀 Запускаем сервер...")
    try:
        # Переходим в корневую директорию проекта
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Запускаем сервер
        process = subprocess.Popen([
            "uvicorn", "backend.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Сервер запущен на http://127.0.0.1:8000")
        print("📝 Логи сервера:")
        
        # Читаем вывод сервера
        while True:
            output = process.stdout.readline()
            if output:
                print(output.decode().strip())
            
            # Проверяем, не завершился ли процесс
            if process.poll() is not None:
                break
        
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")

if __name__ == "__main__":
    print("🔧 Финальное исправление системы DIMA")
    print("=" * 50)
    
    if fix_database_final():
        print("\n🎉 Все проблемы исправлены!")
        print("Теперь можно запускать сервер командой:")
        print("uvicorn backend.main:app --reload")
    else:
        print("\n❌ Есть проблемы с базой данных")
        print("Проверьте подключение к PostgreSQL") 