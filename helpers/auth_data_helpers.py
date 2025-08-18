from faker import Faker
import uuid

fake = Faker()

# 1. Генерация валидных данных курьера
def generate_courier_data():
    unique_suffix = str(uuid.uuid4())[:8]
    return {
        "login": fake.user_name() + unique_suffix,
        "password": fake.password(),
        "firstName": fake.first_name()
    }

# 2. Набор негативных данных для логина
def get_invalid_login_cases():
    return [
        ("wrong_login", "12345"),
        ("valid_login", "wrong_password"),
    ]
