import requests
import json

def test_search_api():
    """Тестируем API поиска ЖК"""
    base_url = "http://localhost:8000"
    
    # Тест 1: Получить все ЖК
    print("=== Тест 1: Получить все ЖК ===")
    response = requests.get(f"{base_url}/zastroys/residential-complexes/")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        complexes = response.json()
        print(f"Найдено ЖК: {len(complexes)}")
        if complexes:
            print(f"Первый ЖК: {complexes[0]['name']} - {complexes[0]['city']}")
    else:
        print(f"Ошибка: {response.text}")
    
    print("\n" + "="*50)
    
    # Тест 2: Поиск по городу
    print("=== Тест 2: Поиск по городу 'Москва' ===")
    response = requests.get(f"{base_url}/zastroys/residential-complexes/?city=Москва")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        complexes = response.json()
        print(f"Найдено ЖК в Москве: {len(complexes)}")
        for complex in complexes:
            print(f"- {complex['name']} ({complex['city']})")
    else:
        print(f"Ошибка: {response.text}")
    
    print("\n" + "="*50)
    
    # Тест 3: Поиск по классу жилья
    print("=== Тест 3: Поиск по классу 'комфорт' ===")
    response = requests.get(f"{base_url}/zastroys/residential-complexes/?housing_class=комфорт")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        complexes = response.json()
        print(f"Найдено ЖК класса 'комфорт': {len(complexes)}")
        for complex in complexes:
            print(f"- {complex['name']} ({complex['housing_class']})")
    else:
        print(f"Ошибка: {response.text}")
    
    print("\n" + "="*50)
    
    # Тест 4: Комбинированный поиск
    print("=== Тест 4: Поиск в Москве класса 'комфорт' ===")
    response = requests.get(f"{base_url}/zastroys/residential-complexes/?city=Москва&housing_class=комфорт")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        complexes = response.json()
        print(f"Найдено ЖК в Москве класса 'комфорт': {len(complexes)}")
        for complex in complexes:
            print(f"- {complex['name']} ({complex['city']}, {complex['housing_class']})")
    else:
        print(f"Ошибка: {response.text}")

if __name__ == "__main__":
    test_search_api() 