import requests
from data.config_urls import BASE_URL

# 1. Создание курьера
def create_courier(courier_data):
    return requests.post(f"{BASE_URL}/api/v1/courier", json=courier_data)


# 2. Авторизация курьера
def login_courier(login, password):
    return requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={"login": login, "password": password}
    )


# 3. Удаление курьера
def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")


# 4. Получить id курьера из ответа логина
def get_courier_id(login_resp):
    return login_resp.json().get("id")


# 5. Получить id курьера по логину и паролю
def get_courier_id_by_credentials(login, password):
    login_resp = login_courier(login, password)
    assert login_resp.status_code == 200, f"Не удалось авторизоваться: {login_resp.text}"
    return login_resp.json().get("id")


# 6. Создать курьера и проверить успешный ответ
def create_and_assert(courier_data):
    resp = create_courier(courier_data)
    assert resp.status_code == 201, f"Курьер не создан: {resp.text}"
    return resp


# 7. Залогиниться и получить id курьера
def login_and_get_id(login, password):
    resp = login_courier(login, password)
    assert resp.status_code == 200, f"Логин не удался: {resp.text}"
    courier_id = get_courier_id(resp)
    assert courier_id, "В ответе нет id"
    return courier_id
