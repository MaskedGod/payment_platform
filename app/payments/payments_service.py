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

    async def get_payments(self):
        """Получает список платежей."""
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при получении платежей",
                )
        return response.json()

    async def create_payment(self, user: User, amount: int, currency: str):
        """Создает новый платеж."""
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        payload = {
            "paymentType": "DEPOSIT",
            "amount": amount,
            "currency": currency,
            "customer": {
                "firstName": user.first_name or "Unknown",
                "lastName": user.last_name or "Unknown",
                "email": user.email,
                "phone": user.phone or "",
            },
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании платежа",
                )
        return response.json()

    async def create_payout(self, user: User, amount: int, currency: str):
        """Создает выплату."""
        url = f"{self.api_url}/payouts"
        headers = await self._get_headers()
        payload = {
            "paymentType": "WITHDRAWAL",
            "amount": amount,
            "currency": currency,
            "customer": {"email": user.email},
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании выплаты",
                )
        return response.json()

    async def create_refund(self, payment_id: int):
        """Создает возврат средств."""
        url = f"{self.api_url}/refunds"
        headers = await self._get_headers()
        payload = {"payment_id": payment_id}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании возврата",
                )
        return response.json()

    async def confirm_payout(self, payout_id: int):
        """Подтверждает выплату."""
        url = f"{self.api_url}/payouts/{payout_id}/confirm"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при подтверждении выплаты",
                )
        return response.json()

    async def check_status(self, payment_id: int):
        """Проверяет статус платежа."""
        url = f"{self.api_url}/payments/{payment_id}/status"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при проверке статуса платежа",
                )
        return response.json()

    async def get_operations(self):
        """Получает список всех операций."""
        url = f"{self.api_url}/operations"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при получении операций",
                )
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
