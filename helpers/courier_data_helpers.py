from faker import Faker

fake = Faker()

# 1. Генерация валидных данных курьера
def generate_courier_data():
    return {
        "login": fake.user_name(),
        "password": fake.password(length=10),
        "firstName": fake.first_name()
    }

# 2. Набор негативных данных для логина
def get_invalid_login_cases():
    return [
        ("wrong_login", "12345"),
        ("valid_login", "wrong_password"),
        ("ghost_user", "ghost_pass")
    ]
