import pytest
from helpers.courier_data_helpers import generate_courier_data, get_invalid_login_cases
from methods.auth_methods import create_and_assert, login_and_get_id, login_courier


class TestCourierLogin:

    # 1. Успешная авторизация курьера
    def test_authorization_success(self, cleanup_courier):
        courier = generate_courier_data()
        create_and_assert(courier)

        courier_id = login_and_get_id(courier["login"], courier["password"])
        cleanup_courier.append(courier_id)

    # 2. Ошибка при пустом login или password
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_authorization_empty_field(self, cleanup_courier, empty_field):
        courier = generate_courier_data()
        create_and_assert(courier)

        # логинимся один раз, чтобы получить id для удаления
        courier_id = login_and_get_id(courier["login"], courier["password"])
        cleanup_courier.append(courier_id)

        # готовим данные с пустым значением
        data = courier.copy()
        data[empty_field] = ""

        resp = login_courier(data.get("login"), data.get("password"))
        assert resp.status_code == 400
        assert "Недостаточно данных" in resp.json().get("message", "")

    # 3-4. Авторизация не проходит для неверного логина или пароля
    @pytest.mark.parametrize("login,password", get_invalid_login_cases())
    def test_authorization_fails_invalid_or_nonexistent_user(self, login, password):
        resp = login_courier(login, password)
        assert resp.status_code == 404
        assert "Учетная запись не найдена" in resp.json().get("message", "")
