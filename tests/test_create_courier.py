import pytest
from helpers.courier_helper import generate_courier_data, create_courier


required_fields = ["login", "password"]

# 1. Курьера можно создать
def test_create_courier_success(cleanup_courier):
    courier_data = generate_courier_data()
    response = create_courier(courier_data)

    assert response.status_code == 201
    assert response.json() == {"ok": True}

    cleanup_courier(courier_data["login"], courier_data["password"])

# 2. Нельзя создать двух одинаковых курьеров
def test_create_duplicate_courier(cleanup_courier):
    courier_data = generate_courier_data()
    create_courier(courier_data)                # первый раз
    response = create_courier(courier_data)     # второй раз

    assert response.status_code == 409
    assert "логин" in response.json()["message"].lower()

    cleanup_courier(courier_data["login"], courier_data["password"])

# 3. Нельзя создать курьера без обязательных полей
@pytest.mark.parametrize("missing_field", required_fields)
def test_create_courier_missing_required_field(missing_field, cleanup_courier):
    courier_data = generate_courier_data()
    data = {k: v for k, v in courier_data.items() if k != missing_field}
    response = create_courier(data)

    assert response.status_code == 400
    assert "недостаточно данных" in response.json()["message"].strip().lower()
