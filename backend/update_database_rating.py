from sqlalchemy import text
from backend.Database.DB_connection import engine, base, get_db
from backend.Models.All_models import DeveloperRating
from backend.Cruds.DeveloperRating_crud import create_developer_rating, calculate_developer_rating, update_developer_rating
from backend.Cruds.Law_crud import get_zastroys

def update_database_with_ratings():
    """Обновить базу данных, добавив таблицу рейтингов застройщиков"""
    
    # Создаем таблицу developer_ratings
    print("Создание таблицы developer_ratings...")
    base.metadata.create_all(engine, tables=[DeveloperRating.__table__])
    
    # Получаем сессию базы данных
    db = next(get_db())
    
    try:
        # Получаем всех застройщиков
        developers = get_zastroys(db, skip=0, limit=1000)
        
        print(f"Найдено {len(developers)} застройщиков")
        
        # Создаем рейтинги для каждого застройщика
        for developer in developers:
            try:
                # Проверяем, есть ли уже рейтинг
                existing_rating = db.query(DeveloperRating).filter(
                    DeveloperRating.law_face_id == developer.id
                ).first()
                
                if not existing_rating:
                    # Рассчитываем рейтинг
                    calculated_rating = calculate_developer_rating(db, developer.id)
                    
                    # Создаем рейтинг
                    create_developer_rating(
                        db, 
                        developer.id, 
                        calculated_rating,
                        completed_projects=(developer.INN % 20) + 5,  # Генерируем тестовые данные
                        years_on_market=(developer.INN % 25) + 5
                    )
                    print(f"Создан рейтинг для застройщика {developer.Company_name}: {calculated_rating}")
                else:
                    print(f"Рейтинг для застройщика {developer.Company_name} уже существует")
                    
            except Exception as e:
                print(f"Ошибка при создании рейтинга для застройщика {developer.Company_name}: {e}")
                continue
        
        print("Обновление базы данных завершено успешно!")
        
    except Exception as e:
        print(f"Ошибка при обновлении базы данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_database_with_ratings() 