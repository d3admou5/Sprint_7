from faker import Faker
import random

fake = Faker()

def generate_order_data(color=None):
    data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": str(random.randint(1, 10)),
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2025-08-18",
        "comment": fake.text(max_nb_chars=20),
    }
    if color is not None:
        data["color"] = color
    return data
