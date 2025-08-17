import pytest
from helpers.auth_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, get_courier_id_by_credentials


class TestCourierCreation:

    # 1. Проверка: курьера можно создать
    def test_create_courier_success(self, cleanup_courier):
        # Генерируем случайного курьера с валидными данными
        courier = generate_courier_data()

        # Создаем курьера через API
        create_resp = create_courier(courier)
        assert create_resp.status_code == 201, f"Ожидали 201, получили {create_resp.status_code}"
        assert create_resp.json().get("ok") is True

        # Получаем ID через вспомогательный метод
        courier_id = get_courier_id_by_credentials(courier["login"], courier["password"])
        assert courier_id is not None

        # Сохраняем ID курьера для удаления после теста
        cleanup_courier.append(courier_id)

    # 2. Проверка: нельзя создать двух одинаковых курьеров
    def test_create_duplicate_courier(self, cleanup_courier):
        courier = generate_courier_data()
        create_resp = create_courier(courier)
        assert create_resp.status_code == 201

        # Повторная попытка должна вернуть 409
        duplicate_resp = create_courier(courier)
        assert duplicate_resp.status_code == 409
        assert "логин" in duplicate_resp.json().get("message")

        # Сохраняем ID оригинального курьера для удаления
        courier_id = get_courier_id_by_credentials(courier["login"], courier["password"])
        cleanup_courier.append(courier_id)


# 3. Проверка обязательных полей: login, password
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_required_field(missing_field):
    courier_data = generate_courier_data()
    data = courier_data.copy()
    data.pop(missing_field)

    resp = create_courier(data)

    assert resp.status_code == 400
    assert "Недостаточно данных" in resp.json().get("message", "")
