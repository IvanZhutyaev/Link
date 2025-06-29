from .Database.DB_connection import engine, get_db
from sqlalchemy import inspect, text
from .Models.All_models import ResidentialComplex
from sqlalchemy.orm import Session

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

def check_residential_complexes():
    """Проверяем данные в таблице residential_complexes"""
    db = next(get_db())
    
    try:
        # Получаем все ЖК
        complexes = db.query(ResidentialComplex).all()
        
        print(f"Всего ЖК в базе: {len(complexes)}")
        
        if complexes:
            print("\nПервые 5 ЖК:")
            for i, complex in enumerate(complexes[:5]):
                print(f"{i+1}. {complex.name} - {complex.city} - {complex.housing_class}")
        
        # Проверяем фильтрацию по городу
        moscow_complexes = db.query(ResidentialComplex).filter(
            ResidentialComplex.city.ilike("%москва%")
        ).all()
        print(f"\nЖК в Москве: {len(moscow_complexes)}")
        
        # Проверяем фильтрацию по классу жилья
        comfort_complexes = db.query(ResidentialComplex).filter(
            ResidentialComplex.housing_class.ilike("%комфорт%")
        ).all()
        print(f"ЖК класса 'комфорт': {len(comfort_complexes)}")
        
        # Проверяем уникальные города
        cities = db.query(ResidentialComplex.city).distinct().all()
        print(f"\nУникальные города: {[city[0] for city in cities]}")
        
        # Проверяем уникальные классы жилья
        housing_classes = db.query(ResidentialComplex.housing_class).distinct().all()
        print(f"Уникальные классы жилья: {[cls[0] for cls in housing_classes if cls[0]]}")
        
    except Exception as e:
        print(f"Ошибка при проверке: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_properties_table()
    check_residential_complexes_table()
    check_law_faces_table()
    check_residential_complexes() 