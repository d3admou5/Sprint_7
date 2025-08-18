import pytest

from helpers.auth_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, get_courier_id_by_credentials, delete_courier


# 1. Фикстура для очистки данных курьера после тестов
@pytest.fixture
def cleanup_courier():
    created_ids = []

    yield created_ids

    for courier_id in created_ids:
        if courier_id:
            delete_courier(courier_id)

# 2. Фикстура для генерации курьера
@pytest.fixture
def created_courier():

    courier_data = generate_courier_data()

    create_resp = create_courier(courier_data)
    assert create_resp.status_code == 201, f"Не удалось создать курьера, код {create_resp.status_code}"

    courier_id = get_courier_id_by_credentials(courier_data["login"], courier_data["password"])
    assert courier_id is not None, "Не удалось получить ID созданного курьера"

    return {"data": courier_data, "id": courier_id}
