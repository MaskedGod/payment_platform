import httpx
from fastapi import HTTPException
from app.config.settings import settings


class PayAdmitService:
    """
    Сервис для работы с API партнера PayAdmit.
    Использует API-ключ для аутентификации и выполняет операции с платежами, выплатами и списками.
    """

    def __init__(self):
        self.api_url = settings.PAYADMIT_API_URL
        self.api_key = settings.API_KEY

    async def _get_headers(self):
        """
        Получает заголовки с API-ключом для авторизации.
        Возвращает словарь с заголовком Authorization.
        """
        return {"Authorization": f"Bearer {self.api_key}"}

    async def get_payments(self):
        """
        Получает список всех платежей.
        Возвращает JSON с информацией о платежах.
        """
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

    async def create_payment(self, amount: int, currency: str):
        """
        Создает новый платеж.
        Параметры:
        - amount (int): сумма платежа.
        - currency (str): валюта платежа.
        Возвращает информацию о созданном платеже.
        """
        url = f"{self.api_url}/payments"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"amount": amount, "currency": currency}
            )
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании платежа",
                )
            return response.json()

    async def create_payout(self, amount: int, currency: str):
        """
        Создает новую выплату.
        Параметры:
        - amount (int): сумма выплаты.
        - currency (str): валюта выплаты.
        Возвращает информацию о созданной выплате.
        """
        url = f"{self.api_url}/payouts"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"amount": amount, "currency": currency}
            )
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании выплаты",
                )
            return response.json()

    async def create_refund(self, payment_id: int):
        """
        Создает возврат средств для платежа.
        Параметры:
        - payment_id (int): идентификатор платежа для возврата.
        Возвращает информацию о возврате.
        """
        url = f"{self.api_url}/refunds"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"payment_id": payment_id}
            )
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при создании возврата",
                )
            return response.json()

    async def confirm_payout(self, payout_id: int):
        """
        Подтверждает выплату.
        Параметры:
        - payout_id (int): идентификатор выплаты для подтверждения.
        Возвращает информацию о подтверждении.
        """
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
        """
        Проверяет статус платежа.
        Параметры:
        - payment_id (int): идентификатор платежа.
        Возвращает информацию о статусе платежа.
        """
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
        """
        Получает список всех операций.
        Возвращает информацию о совершенных операциях.
        """
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
        """
        Получает текущий баланс аккаунта.
        Возвращает информацию о балансе.
        """
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

    async def update_blacklist(self, blacklist: list):
        """
        Обновляет черный список.
        Параметры:
        - blacklist (list): список объектов для черного списка.
        Возвращает результат обновления.
        """
        url = f"{self.api_url}/blacklist"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"blacklist": blacklist}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при обновлении черного списка",
                )
            return response.json()

    async def update_whitelist(self, whitelist: list):
        """
        Обновляет белый список.
        Параметры:
        - whitelist (list): список объектов для белого списка.
        Возвращает результат обновления.
        """
        url = f"{self.api_url}/whitelist"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, headers=headers, json={"whitelist": whitelist}
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка при обновлении белого списка",
                )
            return response.json()
