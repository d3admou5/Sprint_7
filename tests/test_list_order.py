import allure
from methods.order_methods import get_orders_list


@allure.feature("Заказы")
class TestOrdersList:

    @allure.title("Получение списка всех заказов")
    @allure.description("Проверяем, что API возвращает список заказов с корректным статус-кодом и структурой ответа")
    def test_orders_list_returns_orders(self):
        with allure.step("Запрос списка заказов через API"):
            response = get_orders_list()

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, а получен {response.status_code}"

        with allure.step("Проверка структуры ответа и наличия ключа 'orders'"):
            resp_json = response.json()
            assert "orders" in resp_json, f"Нет ключа 'orders' в ответе: {resp_json}"
            assert isinstance(resp_json["orders"], list), "'orders' должно быть списком"
