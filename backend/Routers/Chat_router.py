from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import requests
import base64
import json
import os
import tempfile
import glob
import hashlib
from datetime import datetime, timedelta

router = APIRouter()

# Кэш для ответов
response_cache = {}
MAX_CACHE_SIZE = 100  # Максимальное количество кэшированных ответов


# Функция для создания хеша запроса
def create_request_hash(system: str, user: str) -> str:
    """Создает хеш для кэширования запросов"""
    content = f"{system}:{user}"
    return hashlib.md5(content.encode()).hexdigest()


# Функция для очистки кэша
def cleanup_cache():
    """Очищает кэш если он слишком большой"""
    if len(response_cache) > MAX_CACHE_SIZE:
        # Удаляем старые записи
        keys_to_remove = list(response_cache.keys())[:len(response_cache) - MAX_CACHE_SIZE + 10]
        for key in keys_to_remove:
            del response_cache[key]
        print(f"Очищен кэш, удалено {len(keys_to_remove)} записей")


# Функция для очистки старых аудио файлов
def cleanup_old_audio_files():
    """Удаляет аудио файлы старше 1 часа"""
    try:
        temp_dir = tempfile.gettempdir()
        audio_pattern = os.path.join(temp_dir, "audio_*.mp3")
        current_time = datetime.now()

        for audio_file in glob.glob(audio_pattern):
            file_time = datetime.fromtimestamp(os.path.getctime(audio_file))
            if current_time - file_time > timedelta(hours=1):
                try:
                    os.remove(audio_file)
                    print(f"Удален старый файл: {audio_file}")
                except Exception as e:
                    print(f"Ошибка удаления файла {audio_file}: {e}")
    except Exception as e:
        print(f"Ошибка очистки файлов: {e}")


# Загружаем данные о недвижимости
def load_real_estate_data():
    try:
        # Используем абсолютный путь к файлу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "real_estate_data.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"Загружено {len(data.get('застройщики', []))} застройщиков")
            return data
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return {"застройщики": []}


# Загружаем данные при запуске
real_estate_data = load_real_estate_data()

# Очищаем старые файлы при запуске
cleanup_old_audio_files()

FOLDER_ID = "b1gu5443n2mkggql04p5"
API_KEY = "AQVNxgt6EoH-vteCyRd3S-nsVSw4Y7Vgf3BQ_4XL"

YANDEX_GPT_API = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
YANDEX_TTS_API = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"


class Prompt(BaseModel):
    system: str
    user: str


@router.post("/ask")
def ask_ai(prompt: Prompt):
    try:
        # Проверяем кэш
        request_hash = create_request_hash(prompt.system, prompt.user)
        if request_hash in response_cache:
            print(f"Возвращаем ответ из кэша для: {prompt.user[:30]}...")
            return response_cache[request_hash]

        # Очищаем старые файлы перед обработкой
        cleanup_old_audio_files()
        cleanup_cache()

        # Отладочная информация
        print(f"Загружено застройщиков: {len(real_estate_data.get('застройщики', []))}")
        print(f"Данные о недвижимости: {real_estate_data}")

        # Создаем расширенный системный промпт с данными о недвижимости
        extended_system_prompt = f"""
{prompt.system}

ВАЖНО: Используй ТОЛЬКО следующие данные о недвижимости для ответов на вопросы:

{json.dumps(real_estate_data, ensure_ascii=False, indent=2)}

Правила работы с данными:
1. Отвечай ТОЛЬКО на основе предоставленных данных
2. Если в данных нет подходящих вариантов, честно скажи об этом
3. При поиске квартир учитывай: тип, площадь, цену, город, застройщика
4. Форматируй ответы структурированно и понятно
5. Указывай точные цены и характеристики из базы данных

ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:

📊 АНАЛИЗ ВЫГОДЫ ПОКУПКИ:
- Рассчитывай стоимость квадратного метра
- Сравнивай цены в разных районах
- Анализируй соотношение цена/качество
- Оценивай перспективы роста стоимости
- Учитывай инфраструктуру и транспортную доступность

💰 ИНВЕСТИЦИОННЫЕ СОВЕТЫ:
- Определяй ликвидность недвижимости
- Анализируй потенциал сдачи в аренду
- Оценивай риски и доходность
- Рекомендуй стратегии инвестирования
- Учитывай рыночные тренды

📋 ПОМОЩЬ С ДОКУМЕНТАМИ:
- Объясняй необходимые документы для покупки
- Рассказывай о порядке оформления сделки
- Информируй о налогах и сборах
- Объясняй ипотечные программы
- Консультируй по юридическим вопросам

🏠 ПОЛНЫЙ КОНСАЛТИНГ ПО ПОКУПКЕ:
- Помогай с выбором района
- Консультируй по планировке квартир
- Объясняй особенности застройщиков
- Рекомендуй оптимальные варианты
- Помогай с планированием бюджета

Всегда давай практические советы и конкретные рекомендации!
"""

        # Шаг 1 — Получаем ответ от YandexGPT
        gpt_payload = {
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.5,
                "maxTokens": 2000
            },
            "messages": [
                {"role": "system", "text": extended_system_prompt},
                {"role": "user", "text": prompt.user}
            ]
        }
        gpt_headers = {
            "Authorization": f"Api-Key {API_KEY}",
            "Content-Type": "application/json"
        }

        print(f"Отправляем запрос к YandexGPT: {prompt.user[:50]}...")
        gpt_response = requests.post(YANDEX_GPT_API, json=gpt_payload, headers=gpt_headers, timeout=60)
        gpt_response.raise_for_status()
        gpt_data = gpt_response.json()
        reply = gpt_data["result"]["alternatives"][0]["message"]["text"]
        print(f"Получен ответ от YandexGPT: {reply[:50]}...")

        # Шаг 2 — Синтезируем речь через SpeechKit
        tts_headers = {
            "Authorization": f"Api-Key {API_KEY}"
        }
        tts_data = {
            "text": reply,
            "lang": "ru-RU",
            "voice": "alena",
            "folderId": FOLDER_ID,
            "format": "mp3"
        }

        print("Отправляем запрос к SpeechKit...")
        tts_response = requests.post(YANDEX_TTS_API, data=tts_data, headers=tts_headers, timeout=60)
        tts_response.raise_for_status()
        print("Получен ответ от SpeechKit")

        # Сохраняем аудио во временный файл
        temp_dir = tempfile.gettempdir()
        audio_id = str(hash(reply) % 1000000)
        audio_filename = f"audio_{audio_id}.mp3"
        audio_path = os.path.join(temp_dir, audio_filename)

        with open(audio_path, "wb") as f:
            f.write(tts_response.content)

        tts_base64 = base64.b64encode(tts_response.content).decode("utf-8")

        response_cache[request_hash] = {
            "answer": reply,
            "audio": tts_base64,
            "audioFormat": "mp3",
            "audioUrl": f"/audio/{audio_id}"
        }
        return response_cache[request_hash]

    except Exception as e:
        print(f"Ошибка в ask_ai: {e}")
        return {"error": "Произошла внутренняя ошибка сервера"}


@router.get("/stats")
def get_stats():
    """Получить статистику по данным о недвижимости"""
    total_builders = len(real_estate_data["застройщики"])
    total_complexes = sum(len(builder["жк"]) for builder in real_estate_data["застройщики"])
    total_apartments = 0
    cities = set()

    for builder in real_estate_data["застройщики"]:
        for complex in builder["жк"]:
            cities.add(complex["город"])
            total_apartments += len(complex["квартиры"])

    return {
        "застройщиков": total_builders,
        "жилых_комплексов": total_complexes,
        "квартир": total_apartments,
        "городов": len(cities),
        "список_городов": list(cities)
    }


@router.get("/analysis/{complex_id}")
def analyze_investment(complex_id: int):
    """Анализ инвестиционной привлекательности ЖК"""
    try:
        # Находим ЖК по ID
        for builder in real_estate_data["застройщики"]:
            for complex in builder["жк"]:
                if complex.get("id") == complex_id:
                    # Анализируем данные
                    apartments = complex["квартиры"]
                    avg_price = sum(apt["цена"] for apt in apartments) / len(apartments)
                    avg_area = sum(apt["площадь"] for apt in apartments) / len(apartments)
                    price_per_sqm = avg_price / avg_area

                    return {
                        "жк": complex["название"],
                        "город": complex["город"],
                        "застройщик": builder["название"],
                        "анализ": {
                            "средняя_цена": round(avg_price, 2),
                            "средняя_площадь": round(avg_area, 2),
                            "цена_за_кв_м": round(price_per_sqm, 2),
                            "количество_вариантов": len(apartments),
                            "диапазон_цен": f"{min(apt['цена'] for apt in apartments)} - {max(apt['цена'] for apt in apartments)}"
                        }
                    }
        return {"error": "ЖК не найден"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/documents")
def get_documents_info():
    """Информация о необходимых документах"""
    return {
        "документы_для_покупки": [
            "Паспорт РФ",
            "Свидетельство о браке (если в браке)",
            "Согласие супруга на покупку",
            "Справка о доходах",
            "Справка из банка о состоянии счета",
            "Документы на продажу имеющейся недвижимости (если есть)"
        ],
        "документы_для_ипотеки": [
            "Паспорт РФ",
            "Справка 2-НДФЛ за последние 6 месяцев",
            "Трудовая книжка",
            "Справка с места работы",
            "Документы на залоговое имущество",
            "Справка о кредитной истории"
        ],
        "налоги_и_сборы": [
            "НДФЛ при продаже недвижимости (если владение менее 5 лет)",
            "Налог на имущество физических лиц",
            "Госпошлина за регистрацию права собственности",
            "Нотариальные услуги",
            "Услуги риэлтора (если привлекается)"
        ]
    }


@router.get("/investment-tips")
def get_investment_tips():
    """Советы по инвестициям в недвижимость"""
    return {
        "общие_принципы": [
            "Изучите район и инфраструктуру",
            "Оцените транспортную доступность",
            "Проверьте репутацию застройщика",
            "Анализируйте цены за кв.м в районе",
            "Учитывайте перспективы развития района"
        ],
        "критерии_выбора": [
            "Ликвидность недвижимости",
            "Потенциал роста стоимости",
            "Возможность сдачи в аренду",
            "Состояние рынка недвижимости",
            "Экономическая стабильность региона"
        ],
        "риски": [
            "Изменение рыночных цен",
            "Задержки в строительстве",
            "Проблемы с застройщиком",
            "Изменение законодательства",
            "Экономические кризисы"
        ]
    }


@router.get("/audio/{audio_id}")
def get_audio_file(audio_id: str):
    """Получить аудио файл по ID"""
    try:
        # Проверяем ID на валидность
        if not audio_id.isdigit():
            return {"error": "Неверный ID файла"}

        # Ищем файл в временной директории
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.join(temp_dir, f"audio_{audio_id}.mp3")

        # Проверяем, существует ли файл
        if not os.path.exists(audio_path):
            return {"error": "Файл не найден"}

        # Проверяем размер файла
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            return {"error": "Файл пустой"}

        # Возвращаем файл
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            headers={"Cache-Control": "no-cache"}
        )
    except Exception as e:
        print(f"Ошибка в get_audio_file: {e}")
        return {"error": "Ошибка при получении файла"}