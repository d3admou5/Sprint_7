import pytest
from methods.auth_methods import login_courier
from helpers.courier_data_helpers import get_invalid_login_cases


class TestCourierLogin:

    # 1. Курьер может авторизоваться
    def test_authorization_success(self, courier):
        login_resp = login_courier(courier["login"], courier["password"])
        assert login_resp.status_code == 200
        assert "id" in login_resp.json()
        assert isinstance(login_resp.json()["id"], int)

    # 2. Для авторизации нужны обязательные поля
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_authorization_missing_required_field(self, courier, missing_field):
        data = courier.copy()
        data.pop(missing_field)  # убираем обязательное поле

        resp = login_courier(data.get("login"), data.get("password"))
        assert resp.status_code == 400
        assert resp.json().get("message") == "Недостаточно данных для входа"

    # 3. Авторизация не проходит, если неверный логин или пароль
    @pytest.mark.parametrize("login,password", get_invalid_login_cases())
    def test_authorization_fails_invalid_or_nonexistent_user(self, login, password):
        resp = login_courier(login, password)
        assert resp.status_code == 404
        assert resp.json().get("message") == "Учетная запись не найдена"
