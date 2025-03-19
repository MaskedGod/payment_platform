import httpx
from fastapi import HTTPException
from app.config.settings import settings
from app.users.models import User


class PayAdmitService:
    """
    Сервис для работы с API партнера PayAdmit.
    Использует API-ключ для аутентификации и выполняет операции с платежами, выплатами и списками.
    """

    def __init__(self):
        self.api_url = settings.PAYADMIT_API_URL
        self.api_key = settings.API_KEY

    async def _get_headers(self):
        """Заголовки с API-ключом для авторизации."""
        return {"Authorization": f"Bearer {self.api_key}"}

    async def get_payments(self, limit: int = 10, offset: int = 0):
        """
        Получает список платежей с учетом лимита и смещения.

        Параметры:
        - limit (int): Количество элементов для возврата (по умолчанию 10).
        - offset (int): Количество элементов для пропуска (по умолчанию 0).

        Возвращает:
        - JSON-ответ от API.
        """
        if not (1 <= limit <= 1000):
            raise ValueError("Параметр 'limit' должен быть в диапазоне [1, 1000].")
        if offset < 0:
            raise ValueError("Параметр 'offset' не может быть отрицательным.")

        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        params = {
            "limit": limit,
            "offset": offset,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
        return response.json()

    async def create_payment(
        self, user: User, amount: int, currency: str, customer: dict
    ):
        """Создает новый платеж."""
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        payload = {
            "paymentType": "DEPOSIT",
            "amount": amount,
            "currency": currency,
            "customer": {
                "firstName": customer["firstName"],
                "lastName": customer["lastName"],
                "email": user.email,
            },
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        return response.json()

    async def create_payout(
        self, user: User, amount: int, currency: str, customer: dict
    ):
        """Создает выплату."""
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        payload = {
            "paymentType": "WITHDRAWAL",
            "amount": amount,
            "currency": currency,
            "customer": {
                "firstName": customer["firstName"],
                "lastName": customer["lastName"],
                "email": user.email,
            },
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        return response.json()

    async def confirm_payout(self, payment_id: str):
        """Подтверждает выплату."""
        url = f"{self.api_url}payments/confirmPayout"
        headers = await self._get_headers()
        payload = {"id": payment_id, "action": "PROCESS"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        return response.json()

    async def create_refund(
        self, user: User, amount: int, currency: str, parent_id: str
    ):
        print(amount, currency, parent_id)
        """Создает выплату."""
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        payload = {
            "paymentType": "REFUND",
            "amount": amount,
            "currency": currency,
            "parentPaymentId": parent_id,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        return response.json()

    async def check_status(self, payment_id: str):
        """Проверяет статус платежа."""
        url = f"{self.api_url}/payments/{payment_id}"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        return response.json()

    async def get_operations(self, payment_id: str):
        """Получает список всех операций."""
        url = f"{self.api_url}/{payment_id}/operations"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        return response.json()

    async def get_balance(self):
        """Получает текущий баланс."""
        url = f"{self.api_url}/balance"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при получении баланса",
                )
        return response.json()
