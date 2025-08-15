# Базовый URL сервиса
BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Эндпоинты
CREATE_COURIER_URL = f"{BASE_URL}/api/v1/courier"        # Создание курьера
LOGIN_COURIER_URL = f"{BASE_URL}/api/v1/courier/login"   # Авторизация курьера
CREATE_ORDER_URL = f"{BASE_URL}/api/v1/orders"           # Создание заказа
LIST_ORDERS_URL = f"{BASE_URL}/api/v1/orders"            # Получение списка заказов
