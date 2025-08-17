# Sprint_7
# Тестирование API Курьера и Заказов

## Описание

В этом проекте протестирован API учебного сервиса [Яндекс Самокат](https://qa-scooter.praktikum-services.ru/). 

Документация доступна по [ссылке](https://qa-scooter.praktikum-services.ru/api/v1/docs).

---
##  Тестируемые сценарии
### 1. Создание курьера (`POST /api/v1/courier`)

`test_create_courier_success` Создать нового курьера	`HTTP 201 Created`, тело: `{"ok": true}`.

`test_create_courier_duplicate` Создать курьера с уже существующим логином	`HTTP 409 Сonflict`, тело: `"Этот логин уже используется"`.

`test_create_courier_missing_required_field` Попытка создать курьера без одного из обязательных полей (`login, password`)	`HTTP 400 Bad Request`, тело: `Недостаточно данных для создания учетной записи`.
### 2. Авторизация курьера (`POST /api/v1/courier/login`)
`test_authorization_success`	Авторизация существующего курьера	`HTTP 200`, тело: `id:`.

`test_authorization_empty_field` Попытка авторизации с пустым login или password     `HTTP 400 Bad Request`, тело: `Недостаточно данных для входа`.

`test_authorization_fails_invalid_or_nonexistent_user` Попытка авторизации с несуществующим логином или паролем	`HTTP 404 Not Found`, тело: `Учетная запись не найдена`.

### 3. Создание заказа (`POST /api/v1/orders`)
`test_create_order_with_different_colors` Создание заказа с разными вариантами цветов: только BLACK, только GREY, оба цвета или без цвета `HTTP 201 Created` , тело ответа содержит непустое поле `track`.

### 4. Получение списка заказов (`GET /api/v1/orders`)
`test_orders_list_returns_orders` Проверка получения списка заказов `HTTP 200`, тело ответа содержит ключ `orders`, который является списком.

---

###  Структура проекта

````
.
├── data/                                   
│   └── config_urls.py                      # URL'ы для тестов
│ 
├── helpers/                               
│   ├── auth_data_helpers.py                # Хелперы для работы с данными авторизации
│   └── order_data_helpers.py               # Хелперы для работы с данными заказов
│ 
├── methods/                                  
│   ├── auth_methods.py                     # Методы для работы с авторизацией курьера
│   └── order_methods.py                    # Методы для работы с заказами
│ 
├── tests/                                 
│   ├── test_create_courier.py              # Тесты для создания курьера
│   ├── test_create_order.py                # Тесты для создания заказов
│   ├── test_list_order.py                  # Тесты для получения списка заказов
│   └── test_login_courier.py               # Тесты для авторизации курьера
│ 
├── conftest.py                             # Фикстуры
├── requirements.txt                        # Зависимости проекта
└── README.md                               # Документация проекта
````
---
### Запуск тестов
```
pytest tests/ --alluredir=allure-results
```
### Просмотр отчетов
Для просмотра отчетов Allure, выполните следующие команды:
```
allure serve allure-results
```