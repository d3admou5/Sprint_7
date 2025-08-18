import pytest
import allure
from methods.order_methods import create_order
from helpers.order_data_helpers import generate_order_data


@allure.feature("Заказ")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description(
        "Проверяем, что можно создать заказ с разными вариантами цветов: "
        "только чёрный, только серый, оба цвета или без цвета"
    )
    @pytest.mark.parametrize("color", [
        ["BLACK"],         # только чёрный
        ["GREY"],          # только серый
        ["BLACK", "GREY"], # оба цвета
        None               # без указания цвета
    ])
    def test_create_order_with_different_colors(self, color):
        with allure.step(f"Генерация данных заказа с цветом: {color}"):
            order_data = generate_order_data(color)

        with allure.step("Создание заказа через API"):
            response = create_order(order_data)

        with allure.step("Проверка успешного статуса ответа"):
            assert response.status_code == 201, f"Не удалось создать заказ: {response.text}"

        with allure.step("Проверка наличия поля 'track' в ответе"):
            response_json = response.json()
            assert "track" in response_json, f"В ответе нет 'track': {response_json}"
            assert response_json["track"], "Поле 'track' пустое"
