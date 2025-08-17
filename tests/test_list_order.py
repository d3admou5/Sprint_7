from methods.order_methods import get_orders_list


class TestOrdersList:
# 1. Тестирование получения списка заказов
    def test_orders_list_returns_orders(self):
        # 1. Получаем список заказов
        response = get_orders_list()

        # 2. Проверяем статус-код
        assert response.status_code == 200, f"Ожидался статус 200, а получен {response.status_code}"

        # 3. Проверяем, что в ответе есть список заказов
        resp_json = response.json()
        assert "orders" in resp_json, f"Нет ключа 'orders' в ответе: {resp_json}"
        assert isinstance(resp_json["orders"], list), "'orders' должно быть списком"
