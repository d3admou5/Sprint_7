import pytest
from helpers.courier_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, login_courier


class TestCourierCreation:

    # 1. Курьера можно создать
    def test_create_courier_success(self, courier):
        login_resp = login_courier(courier["login"], courier["password"])

        assert login_resp.status_code == 200
        assert "id" in login_resp.json()
        assert isinstance(login_resp.json()["id"], int)

    # 2. Нельзя создать двух одинаковых курьеров
    def test_create_duplicate_courier(self, courier):
        duplicate_resp = create_courier(courier)

        assert duplicate_resp.status_code == 409
        assert duplicate_resp.json().get("message") == "Этот логин уже используется"

    # 3. Обязательные поля: login и password
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        courier_data = generate_courier_data()
        data = courier_data.copy()
        data.pop(missing_field)  # убираем обязательное поле

        resp = create_courier(data)

        assert resp.status_code == 400
        assert resp.json().get("message") == "Недостаточно данных для создания учетной записи"
