import requests
from data.config_urls import BASE_URL

# Создание заказа
def create_order(order_data):
    return requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)

# Получение списка заказов
def get_orders_list():
    return requests.get(f"{BASE_URL}/api/v1/orders")
