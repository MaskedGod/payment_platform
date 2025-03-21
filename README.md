# Payment Platform


Платформа, предоставляющая удобный способ взаимодействия с партнёрским API для управления платежами, выплатами и пользователями.
Платформа интегрируется со следующей партнерской системой:
**RZ** — [Документация](https://api.payadmit.com/docs/)

## Описание

Payment Platform — это веб-сервис на базе **FastAPI**, который предоставляет API для работы с платёжной системой PayAdmit. Проект включает следующие возможности:
- Аутентификация пользователей через JWT.
- Создание и управление платежами, выплатами и возвратами средств.
- Получение информации о балансе и операциях.
- Обработка вебхуков от платёжной системы.
- Управление пользователями (создание, удаление).

Проект разработан с использованием современных технологий, таких как **SQLAlchemy**, **Pydantic**, **HTTPX**, и поддерживает асинхронную обработку запросов.

## Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Установка](#установка)
- [Использование](#использование)
- [API Документация](#api-документация)
- [Структура проекта](#структура-проекта)
- [Лицензия](#лицензия)

## Технологии

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **База данных**: PostgreSQL (асинхронный драйвер `asyncpg`)
- **ORM**: SQLAlchemy
- **Аутентификация**: JWT (RSA256)
- **HTTP-клиент**: HTTPX
- **Контейнеризация**: Docker
- **Миграции**: Alembic
- **Дополнительные инструменты**: Redis, RabbitMQ

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/MaskedGod/payment_platform.git
cd payment-platform
```

### 2. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните файл `.env` своими данными:

```env
PAYADMIT_API_URL=your_api_key_here
PAYADMIT_SIGN_KEY=your_sign_key_here
WEBHOOK_URL=your_webhook_url_here
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=redis
REDIS_PORT=61234
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=51234
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
alembic upgrade head
```

### 5. Запуск приложения

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Использование

### Авторизация

1. **Регистрация пользователя**:
   ```bash
   POST /users/
   Body:
   {
       "email": "user@example.com",
       "password": "securepassword"
   }
   ```

2. **Авторизация**:
   ```bash
   POST /auth/login
   Body:
   {
       "email": "user@example.com",
       "password": "securepassword"
   }
   Response:
   {
       "access_token": "your_jwt_token",
       "token_type": "Bearer"
   }
   ```

### Платежи

1. **Создание платежа**:
   ```bash
   POST /payments
   Headers:
   Authorization: Bearer your_jwt_token
   Body:
   {
       "amount": 100.0,
       "currency": "EUR",
       "customer": {
           "firstName": "John",
           "lastName": "Doe"
       }
   }
   ```

2. **Проверка статуса платежа**:
   ```bash
   GET /payments/status?payment_id=12345
   Headers:
   Authorization: Bearer your_jwt_token
   ```

### Вебхуки

Платформа поддерживает обработку вебхуков от PayAdmit. Пример эндпоинта:

```bash
POST /webhooks/payment_status
```

### Баланс

Получение текущего баланса:

```bash
GET /balance
Headers:
Authorization: Bearer your_jwt_token
```

## API Документация

Документация API доступна по адресу:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Структура проекта

```
payment_system/
├── app/
│   ├── api/               # Эндпоинты API
│   │   ├── auth.py        # Аутентификация
│   │   ├── health.py      # Проверка состояния сервиса
│   │   ├── payment.py     # Управление платежами
│   │   ├── user.py        # Управление пользователями
│   │   └── webhooks.py    # Обработка вебхуков
│   ├── auth/              # Логика аутентификации
│   ├── config/            # Конфигурация
│   ├── db/                # База данных
│   ├── payments/          # Логика платежей
│   ├── users/             # Логика пользователей
│   └── __init__.py
├── keys/                  # Ключи для JWT
├── migrations/            # Миграции Alembic
├── .env.example           # Пример файла переменных окружения
├── alembic.ini            # Конфигурация Alembic
├── docker-compose.yml     # Docker Compose
├── main.py                # Точка входа
└── README.md              # Документация
```
