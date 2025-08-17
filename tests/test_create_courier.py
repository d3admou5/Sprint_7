import pytest
import allure
from helpers.auth_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, get_courier_id_by_credentials


@allure.feature("Курьер")
class TestCourierCreation:

    @allure.title("Создание нового курьера с валидными данными")
    @allure.description("Проверяем, что можно создать курьера с уникальными логином и паролем, "
                        "а затем получить его ID через API")
    def test_create_courier_success(self, cleanup_courier):
        with allure.step("Генерация валидного курьера"):
            courier = generate_courier_data()

        with allure.step("Создание курьера через API"):
            create_resp = create_courier(courier)
            assert create_resp.status_code == 201, f"Ожидали 201, получили {create_resp.status_code}"
            assert create_resp.json().get("ok") is True

        with allure.step("Получение ID созданного курьера"):
            courier_id = get_courier_id_by_credentials(courier["login"], courier["password"])
            assert courier_id is not None

        with allure.step("Сохранение ID для последующего удаления"):
            cleanup_courier.append(courier_id)

    @allure.title("Попытка создать дубликат курьера")
    @allure.description("Проверяем, что повторная попытка создать курьера с тем же логином возвращает 409")
    def test_create_duplicate_courier(self, cleanup_courier):
        with allure.step("Генерация нового курьера"):
            courier = generate_courier_data()

        with allure.step("Создание курьера через API"):
            create_resp = create_courier(courier)
            assert create_resp.status_code == 201

        with allure.step("Попытка создать дубликат курьера"):
            duplicate_resp = create_courier(courier)
            assert duplicate_resp.status_code == 409
            assert "логин" in duplicate_resp.json().get("message")

        with allure.step("Сохранение ID оригинального курьера для удаления"):
            courier_id = get_courier_id_by_credentials(courier["login"], courier["password"])
            cleanup_courier.append(courier_id)


@allure.feature("Курьер")
@allure.title("Создание курьера с отсутствующими обязательными полями")
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_required_field(missing_field):
    with allure.step(f"Генерация курьера и удаление поля {missing_field}"):
        courier_data = generate_courier_data()
        data = courier_data.copy()
        data.pop(missing_field)

    with allure.step("Попытка создать курьера с неполными данными"):
        resp = create_courier(data)
        assert resp.status_code == 400
        assert "Недостаточно данных" in resp.json().get("message", "")
