import requests
from data.config_urls import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL


# 1. Создание курьера
def create_courier(payload):
    return requests.post(CREATE_COURIER_URL, json=payload)


# 2. Логин курьера
def login_courier(login, password):
    return requests.post(LOGIN_COURIER_URL, json={"login": login, "password": password})


# 3. Удаление курьера по id
def delete_courier(courier_id):
    return requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")
