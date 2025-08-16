import pytest

from methods.auth_methods import delete_courier


# 1. Фикстура для очистки данных курьера после тестов
@pytest.fixture
def cleanup_courier():
    created_ids = []

    yield created_ids

    for courier_id in created_ids:
        if courier_id:
            delete_courier(courier_id)
