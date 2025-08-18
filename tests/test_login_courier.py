import pytest
import allure
from helpers.auth_data_helpers import generate_courier_data, get_invalid_login_cases
from methods.auth_methods import create_and_assert, login_and_get_id, login_courier


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер с валидными данными может авторизоваться и получить ID")
    def test_authorization_success(self, cleanup_courier):
        with allure.step("Генерация нового курьера"):
            courier = generate_courier_data()

        with allure.step("Создание курьера через API и проверка успешного ответа"):
            create_and_assert(courier)

        with allure.step("Авторизация курьера и получение его ID"):
            courier_id = login_and_get_id(courier["login"], courier["password"])

        with allure.step("Сохранение ID для последующего удаления"):
            cleanup_courier.append(courier_id)

    @allure.title("Ошибка авторизации при пустом login или password")
    @allure.description("Проверяем, что API возвращает 400 при попытке авторизоваться с пустым полем")
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_authorization_empty_field(self, cleanup_courier, empty_field):
        with allure.step("Генерация и создание курьера"):
            courier = generate_courier_data()
            create_and_assert(courier)

        with allure.step("Авторизация курьера для получения ID"):
            courier_id = login_and_get_id(courier["login"], courier["password"])
            cleanup_courier.append(courier_id)

        with allure.step(f"Подготовка данных с пустым полем {empty_field}"):
            data = courier.copy()
            data[empty_field] = ""

        with allure.step("Попытка авторизации с неполными данными"):
            resp = login_courier(data.get("login"), data.get("password"))
            assert resp.status_code == 400
            assert "Недостаточно данных" in resp.json().get("message", "")

    @allure.title("Ошибка авторизации для несуществующего логина или пароля")
    @allure.description("Проверяем, что API возвращает 404 при попытке авторизации с неверными данными")
    @pytest.mark.parametrize("login,password", get_invalid_login_cases())
    def test_authorization_fails_invalid_or_nonexistent_user(self, login, password):
        with allure.step(f"Попытка авторизации с login={login}, password={password}"):
            resp = login_courier(login, password)
            assert resp.status_code == 404
            assert "Учетная запись не найдена" in resp.json().get("message", "")
