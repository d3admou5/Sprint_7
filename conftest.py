import pytest
from helpers.courier_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, login_courier, delete_courier

# 1. Фикстура для создания курьера и его удаления после тестов
@pytest.fixture
def courier():
    data = generate_courier_data()
    resp = create_courier(data)
    courier_id = None

    if resp.status_code == 201:
        login_resp = login_courier(data["login"], data["password"])
        courier_id = login_resp.json().get("id")

    yield data

    if courier_id:
        delete_courier(courier_id)
