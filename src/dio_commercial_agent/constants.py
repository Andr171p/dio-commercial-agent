from pathlib import Path


# Директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"  # Переменные окружения


# Индексы векторной БД
SERVICES_INDEX_NAME = "services"  # Сервисы 1С ИТС
PRICE_LIST_INDEX_NAME = "price-list"  # Прайс-лист сервисов 1С

# YandexGPT LLM
YANDEX_GPT_MODEL = "yandexgpt"

TOP_K = 10  # Количество извлекаемых записей
