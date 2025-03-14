import httpx
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import List, Dict
from enum import Enum


from app.config.settings import settings
from app.db.database import get_db
from app.db.models import Payment


class PaymentType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    REFUND = "REFUND"


class PaymentState(Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    DECLINED = "DECLINED"
    ERROR = "ERROR"


class PaymentService:
    """Handles all payment-related operations."""

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.base_url = settings.PAYADMIT_API_URL
        self.auth_url = settings.PAYADMIT_AUTH_URL
        self.api_key = settings.API_KEY
        self.db = db

    async def _make_api_request(
        self, method: str, url: str, payload: dict = None
    ) -> dict:
        """
        Helper method to make API requests with retry logic and error handling.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            async with httpx.AsyncClient() as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, json=payload, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, detail=response.text
                    )

                return response.json()
        except Exception as e:
            print(f"Error during API request: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def create_payment(self, user_id: int, payment_data: dict) -> dict:
        """
        Create a new payment (DEPOSIT).
        """
        payment_data["paymentType"] = PaymentType.DEPOSIT.value
        response = await self._make_api_request("POST", self.base_url, payment_data)

        # Save payment details to the database
        payment = Payment(
            id=response["result"]["id"],
            user_id=user_id,
            reference_id=payment_data["referenceId"],
            payment_type=PaymentType.DEPOSIT.value,
            state=PaymentState.PENDING.value,
            amount=payment_data["amount"],
            currency=payment_data["currency"],
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def create_payout(self, user_id: int, payout_data: dict) -> dict:
        """
        Create a new payout (WITHDRAWAL).
        """
        payout_data["paymentType"] = PaymentType.WITHDRAWAL.value
        response = await self._make_api_request("POST", self.base_url, payout_data)

        # Save payout details to the database
        payout = Payment(
            id=response["result"]["id"],
            user_id=user_id,
            reference_id=payout_data["referenceId"],
            payment_type=PaymentType.WITHDRAWAL.value,
            state=PaymentState.PENDING.value,
            amount=payout_data["amount"],
            currency=payout_data["currency"],
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(payout)
        await self.db.commit()
        await self.db.refresh(payout)
        return payout

    async def create_refund(self, user_id: int, refund_data: dict) -> dict:
        """
        Create a new refund (REFUND).
        """
        refund_data["paymentType"] = PaymentType.REFUND.value
        response = await self._make_api_request("POST", self.base_url, refund_data)

        # Save refund details to the database
        refund = Payment(
            id=response["result"]["id"],
            user_id=user_id,
            reference_id=refund_data["referenceId"],
            payment_type=PaymentType.REFUND.value,
            state=PaymentState.PENDING.value,
            amount=refund_data["amount"],
            currency=refund_data["currency"],
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(refund)
        await self.db.commit()
        await self.db.refresh(refund)
        return refund

    async def confirm_payout(self, payout_id: str, action: str) -> dict:
        """
        Confirm or decline a payout.
        """
        payload = {"id": payout_id, "action": action}
        url = f"{self.base_url}/confirmPayout"
        return await self._make_api_request("POST", url, payload)

    async def check_status(self, payment_id: str) -> dict:
        """
        Check the status of a specific payment.
        """
        url = f"{self.base_url}/{payment_id}"
        return await self._make_api_request("GET", url)

    async def get_operations(self, payment_id: str) -> List[Dict]:
        """
        Get a list of operations performed during payment processing.
        """
        url = f"{self.base_url}/{payment_id}/operations"
        return await self._make_api_request("GET", url)

    async def get_balance(self, terminal_id: int, currency: str = None) -> dict:
        """
        Get the merchant's balance for a specific terminal ID.
        """
        url = f"{self.base_url}/terminals/getBalance/{terminal_id}"
        if currency:
            url += f"?currency={currency}"
        return await self._make_api_request("GET", url)
