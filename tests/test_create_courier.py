import pytest
from helpers.courier_data_helpers import generate_courier_data
from methods.auth_methods import create_courier, login_courier


class TestCourierCreation:

# 1. Проверка: курьера можно создать
    def test_create_courier_success(self, cleanup_courier):
        # Генерируем случайного курьера с валидными данными
        courier = generate_courier_data()

        # Создаем курьера через API
        create_resp = create_courier(courier)
        # Проверяем, что API вернул статус 201 (Created)
        assert create_resp.status_code == 201
        # Проверяем тело ответа, должно быть {"ok": True}
        assert create_resp.json() == {"ok": True}

        # Логинимся с новыми данными, чтобы получить ID курьера
        login_resp = login_courier(courier["login"], courier["password"])
        courier_id = login_resp.json().get("id")
        # Проверяем, что ID вернулся
        assert courier_id is not None

        # Сохраняем ID курьера в фикстуру cleanup_courier для последующего удаления
        cleanup_courier.append(courier_id)

# 2. Проверка: нельзя создать двух одинаковых курьеров
    def test_create_duplicate_courier(self, cleanup_courier):
        # Сначала создаем нового курьера — шаг теста
        courier = generate_courier_data()
        create_resp = create_courier(courier)
        assert create_resp.status_code == 201

        # Проверяем, что создание дубликата возвращает ошибку
        duplicate_resp = create_courier(courier)
        # Ожидаем статус 409 (Conflict)
        assert duplicate_resp.status_code == 409
        # Сообщение должно указывать, что логин уже используется
        assert duplicate_resp.json().get("message") == "Этот логин уже используется"

        # Получаем ID оригинального курьера для удаления после теста
        courier_id = login_courier(courier["login"], courier["password"]).json().get("id")
        cleanup_courier.append(courier_id)

# 3-4. Проверка обязательных полей: login и password
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):
        # Генерируем валидного курьера
        courier_data = generate_courier_data()
        data = courier_data.copy()
        # Убираем одно из обязательных полей
        data.pop(missing_field)

        # Пытаемся создать курьера без обязательного поля
        resp = create_courier(data)
        # Проверяем, что API вернул ошибку 400 (Bad Request)
        assert resp.status_code == 400
        # Проверяем сообщение ошибки
        assert resp.json().get("message") == "Недостаточно данных для создания учетной записи"
