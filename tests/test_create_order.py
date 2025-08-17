import pytest
from methods.order_methods import create_order
from helpers.order_data_helpers import generate_order_data


class TestCreateOrder:
# 1. Тестирование создания заказа с разными цветами
    @pytest.mark.parametrize("color", [
        ["BLACK"],         # только чёрный
        ["GREY"],          # только серый
        ["BLACK", "GREY"], # оба цвета
        None               # без указания цвета
    ])
    def test_create_order_with_different_colors(self, color):
        # 1. Генерация данных заказа
        order_data = generate_order_data(color)

        # 2. Отправляем запрос на создание заказа
        response = create_order(order_data)

        # 3. Проверяем успешный статус
        assert response.status_code == 201, f"Не удалось создать заказ: {response.text}"

        # 4. Проверяем, что в ответе есть track
        response_json = response.json()
        assert "track" in response_json, f"В ответе нет 'track': {response_json}"
        assert response_json["track"], "Поле 'track' пустое"
