import requests
import json

def test_top_developers():
    """Тестирует эндпоинт топ застройщиков"""
    try:
        # Тестируем получение топ 5 застройщиков
        response = requests.get('http://localhost:8000/developer-ratings/top/?limit=5')
        
        if response.status_code == 200:
            developers = response.json()
            print(f"✅ Успешно получено {len(developers)} застройщиков:")
            for i, dev in enumerate(developers, 1):
                print(f"  {i}. {dev['company_name']} - Рейтинг: {dev['rating']}/10")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что бэкенд запущен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_top_developers() 