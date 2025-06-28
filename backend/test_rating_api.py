import requests
import json

BASE_URL = "http://localhost:8000"

def test_developer_rating_api():
    """Тестирование API рейтинга застройщиков"""
    
    print("=== Тестирование API рейтинга застройщиков ===\n")
    
    # 1. Получить топ застройщиков
    print("1. Получение топ застройщиков:")
    try:
        response = requests.get(f"{BASE_URL}/developer-ratings/top/?limit=5")
        if response.status_code == 200:
            developers = response.json()
            print(f"✅ Успешно получено {len(developers)} застройщиков:")
            for i, dev in enumerate(developers, 1):
                print(f"   {i}. {dev['company_name']} - Рейтинг: {dev['rating']}/10")
        else:
            print(f"❌ Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print()
    
    # 2. Получить застройщика с рейтингом и статистикой
    print("2. Получение застройщика с рейтингом и статистикой:")
    try:
        response = requests.get(f"{BASE_URL}/zastroys/1/with-stats")
        if response.status_code == 200:
            developer = response.json()
            print(f"✅ Застройщик: {developer['Company_name']}")
            if developer.get('rating'):
                rating = developer['rating']
                print(f"   Рейтинг: {rating['rating']}/10")
                print(f"   Завершенных проектов: {rating['completed_projects']}")
                print(f"   Лет на рынке: {rating['years_on_market']}")
            if developer.get('stats'):
                stats = developer['stats']
                print(f"   Объектов недвижимости: {stats['properties_count']}")
                print(f"   Жилых комплексов: {stats['complexes_count']}")
                print(f"   Средний рейтинг квартир: {stats['avg_property_rating']}")
                print(f"   Средний рейтинг ЖК: {stats['avg_complex_rating']}")
        else:
            print(f"❌ Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print()
    
    # 3. Пересчитать рейтинг застройщика
    print("3. Пересчет рейтинга застройщика:")
    try:
        response = requests.post(f"{BASE_URL}/zastroys/1/recalculate-rating")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Рейтинг пересчитан: {result['new_rating']}")
        else:
            print(f"❌ Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print()
    
    # 4. Получить статистику застройщика
    print("4. Получение статистики застройщика:")
    try:
        response = requests.get(f"{BASE_URL}/zastroys/1/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Статистика застройщика:")
            print(f"   Объектов недвижимости: {stats['properties_count']}")
            print(f"   Жилых комплексов: {stats['complexes_count']}")
            print(f"   Средний рейтинг квартир: {stats['avg_property_rating']}")
            print(f"   Средний рейтинг ЖК: {stats['avg_complex_rating']}")
            print(f"   Общий рейтинг: {stats['overall_rating']}")
        else:
            print(f"❌ Ошибка: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    test_developer_rating_api() 