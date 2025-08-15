from faker import Faker
import requests
from data.config_urls import CREATE_COURIER_URL

fake = Faker()

# 1. Функция для генерации данных курьера
def generate_courier_data():
    return {
        "login": fake.user_name(),
        "password": fake.password(length=10),
        "firstName": fake.first_name()
    }

def create_courier(payload):
    response = requests.post(CREATE_COURIER_URL, json=payload)
    return response
