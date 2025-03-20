# from enum import Enum
from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: float
    currency: str
    customer: dict


class CreateRefundRequest(BaseModel):
    amount: float
    currency: str
    parentPaymentId: str


# class ConfirmationType(Enum):
#     confirm: str = "PROCESS"
#     decline: str = "DECLINE"


class PaymentConfirmationType(BaseModel):
    payment_id: str
    # action: ConfirmationType
