import pytest
from methods.auth_methods import create_courier, login_courier
from helpers.courier_data_helpers import generate_courier_data, get_invalid_login_cases


class TestCourierLogin:

# 1. Проверка успешной авторизации курьера
    def test_authorization_success(self, cleanup_courier):
        # Генерируем случайного курьера
        courier = generate_courier_data()

        # Создаем курьера через API
        create_resp = create_courier(courier)
        # Проверяем, что курьер успешно создан (201 Created)
        assert create_resp.status_code == 201, f"Курьер не создан: {create_resp.text}"

        # Пытаемся войти с корректными данными
        login_resp = login_courier(courier["login"], courier["password"])
        # Проверяем, что авторизация прошла успешно (200 OK)
        assert login_resp.status_code == 200, f"Не удалось войти: {login_resp.text}"

        # Получаем ID курьера для последующего удаления
        courier_id = login_resp.json().get("id")
        # Проверяем, что ID есть и это целое число
        assert courier_id is not None
        assert isinstance(courier_id, int)

        # Добавляем ID в cleanup_fixture для удаления после теста
        cleanup_courier.append(courier_id)

# 2. Проверка, что авторизация невозможна, если отсутствует обязательное поле
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_authorization_missing_required_field(self, cleanup_courier, missing_field):
        # Создаем курьера для теста
        courier = generate_courier_data()
        create_resp = create_courier(courier)
        assert create_resp.status_code == 201

        # Копируем данные и удаляем одно обязательное поле
        data = courier.copy()
        data.pop(missing_field)

        # Пытаемся авторизоваться без обязательного поля
        resp = login_courier(data.get("login"), data.get("password"))
        # Ожидаем ошибку 400 и соответствующее сообщение
        assert resp.status_code == 400
        assert resp.json().get("message") == "Недостаточно данных для входа"

        # Логинимся с корректными данными, чтобы получить ID для удаления
        login_resp = login_courier(courier["login"], courier["password"])
        courier_id = login_resp.json().get("id")
        cleanup_courier.append(courier_id)

# 3-4. Проверка, что авторизация не проходит для неверного логина или пароля
    @pytest.mark.parametrize("login,password", get_invalid_login_cases())
    def test_authorization_fails_invalid_or_nonexistent_user(self, login, password):
        # Пытаемся авторизоваться с неправильными данными
        resp = login_courier(login, password)
        # Ожидаем ошибку 404 и сообщение о том, что учетная запись не найдена
        assert resp.status_code == 404
        assert resp.json().get("message") == "Учетная запись не найдена"
