from Database.DB_connection import engine
from sqlalchemy import inspect, text

def check_properties_table():
    """Проверяем структуру таблицы Properties"""
    
    inspector = inspect(engine)
    
    # Получаем список всех таблиц
    tables = inspector.get_table_names()
    print("Таблицы в базе данных:")
    for table in tables:
        print(f"- {table}")
    
    print("\n" + "="*50)
    
    # Проверяем структуру таблицы Properties
    if 'Properties' in tables:
        columns = inspector.get_columns('Properties')
        print("Колонки в таблице Properties:")
        for col in columns:
            print(f"- {col['name']}: {col['type']} (nullable: {col['nullable']})")
    else:
        print("Таблица Properties не найдена!")

def check_residential_complexes_table():
    """Проверяем структуру таблицы residential_complexes"""
    
    inspector = inspect(engine)
    
    if 'residential_complexes' in inspector.get_table_names():
        columns = inspector.get_columns('residential_complexes')
        print("\nКолонки в таблице residential_complexes:")
        for col in columns:
            print(f"- {col['name']}: {col['type']} (nullable: {col['nullable']})")
    else:
        print("Таблица residential_complexes не найдена!")

def check_law_faces_table():
    """Проверяем структуру таблицы Law_faces"""
    
    inspector = inspect(engine)
    
    if 'Law_faces' in inspector.get_table_names():
        columns = inspector.get_columns('Law_faces')
        print("\nКолонки в таблице Law_faces:")
        for col in columns:
            print(f"- {col['name']}: {col['type']} (nullable: {col['nullable']})")
    else:
        print("Таблица Law_faces не найдена!")

if __name__ == "__main__":
    check_properties_table()
    check_residential_complexes_table()
    check_law_faces_table() 