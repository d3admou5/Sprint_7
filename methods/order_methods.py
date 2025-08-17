import requests
from data.config_urls import CREATE_ORDER_URL, LIST_ORDERS_URL

# 1. Создание заказа
def create_order(order_data):
    return requests.post(CREATE_ORDER_URL, json=order_data)

# 2. Получение списка заказов
def get_orders_list():
    return requests.get(LIST_ORDERS_URL)
