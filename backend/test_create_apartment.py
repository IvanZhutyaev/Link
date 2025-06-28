import requests
import json

# URL API
BASE_URL = "http://localhost:8000"

def test_create_apartment():
    """Тестируем создание квартиры"""
    
    # Данные для создания квартиры
    apartment_data = {
        "name": "Тестовая квартира 1",
        "address": "г. Москва, ул. Тестовая, 1, кв. 1",
        "price": 5000000,
        "description": "Тестовая квартира для проверки API",
        "image_url": "https://via.placeholder.com/300x200/007aff/ffffff?text=Тест",
        "city": "Москва",
        "is_available": True,
        "zastroy_id": 1,
        "complex_id": 1,
        "area": 75.5,
        "rooms": 2,
        "floor": 5,
        "status": "available"
    }
    
    try:
        # Отправляем запрос на создание квартиры
        response = requests.post(
            f"{BASE_URL}/properties/",
            json=apartment_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {response.headers}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Квартира успешно создана: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"Ошибка создания квартиры: {response.text}")
            
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")

def test_get_properties():
    """Тестируем получение списка недвижимости"""
    
    try:
        response = requests.get(f"{BASE_URL}/properties/")
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            properties = response.json()
            print(f"Найдено объектов недвижимости: {len(properties)}")
            for prop in properties:
                print(f"- {prop['name']} (ID: {prop['id']})")
        else:
            print(f"Ошибка получения недвижимости: {response.text}")
            
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")

if __name__ == "__main__":
    print("Тестируем создание квартиры...")
    test_create_apartment()
    
    print("\nТестируем получение списка недвижимости...")
    test_get_properties() 