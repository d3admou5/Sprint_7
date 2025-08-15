import requests
import random
import string

from data.config_urls import CREATE_COURIER_URL

# метод регистрации нового курьера возвращает список из логина, пароля и имени
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(CREATE_COURIER_URL, json=payload)

    if response.status_code == 201:
        login_pass.extend([login, password, first_name])

    return login_pass
