import requests
import json

def test_avaline_integration():
    """Тестируем интеграцию с AvaLine"""
    base_url = "http://localhost:8000"
    
    # Тест 1: Создание ЖК с ссылкой на AvaLine
    print("=== Тест 1: Создание ЖК с ссылкой на AvaLine ===")
    
    complex_data = {
        "name": "Тестовый ЖК с AvaLine",
        "address": "г. Москва, ул. Тестовая, 1",
        "developer_name": "Тестовый застройщик",
        "zastroy_id": 1,
        "city": "Москва",
        "commissioning_date": "2025",
        "housing_class": "комфорт",
        "status": "строится",
        "avaline_url": "https://avaline.ru/tour/test-complex",
        "avatar_url": "https://example.com/test-image.jpg"
    }
    
    try:
        response = requests.post(f"{base_url}/zastroys/residential-complexes/", json=complex_data)
        print(f"Статус создания: {response.status_code}")
        if response.status_code == 200:
            created_complex = response.json()
            print(f"Создан ЖК: {created_complex['name']}")
            print(f"Ссылка на AvaLine: {created_complex.get('avaline_url', 'Не указана')}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка при создании: {e}")
    
    print("\n" + "="*50)
    
    # Тест 2: Получение ЖК с ссылкой на AvaLine
    print("=== Тест 2: Получение ЖК с ссылкой на AvaLine ===")
    
    try:
        response = requests.get(f"{base_url}/zastroys/residential-complexes/")
        print(f"Статус получения: {response.status_code}")
        if response.status_code == 200:
            complexes = response.json()
            print(f"Всего ЖК: {len(complexes)}")
            
            # Ищем ЖК с ссылкой на AvaLine
            complexes_with_avaline = [c for c in complexes if c.get('avaline_url')]
            print(f"ЖК с ссылкой на AvaLine: {len(complexes_with_avaline)}")
            
            for complex in complexes_with_avaline[:3]:  # Показываем первые 3
                print(f"- {complex['name']}: {complex.get('avaline_url')}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка при получении: {e}")

if __name__ == "__main__":
    test_avaline_integration() 