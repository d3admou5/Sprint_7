import pytest
import requests
from data.config_urls import LOGIN_COURIER_URL, DELETE_COURIER_URL

# 1. Фикстура для удаления курьера после теста
@pytest.fixture
def cleanup_courier():

    courier_id = None

    def _delete_courier(courier_login, courier_password):
        nonlocal courier_id
        login_resp = requests.post(LOGIN_COURIER_URL, json={"login": courier_login, "password": courier_password})
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            requests.delete(DELETE_COURIER_URL.replace(":id", str(courier_id)))

    yield _delete_courier
