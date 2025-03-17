from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, Enum, ForeignKey
from enum import Enum as PyEnum
from typing import List

from app.db.database import Base


# Define Enums for Payment Type and State
class PaymentType(PyEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    REFUND = "REFUND"
    CARDVERIFY = "CARDVERIFY"


class PaymentState(PyEnum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    DECLINED = "DECLINED"
    CHECKOUT = "CHECKOUT"
    ERROR = "ERROR"
    RECONCILIATION = "RECONCILIATION"
    AWAITING_WEBHOOK = "AWAITING_WEBHOOK"
    AWAITING_REDIRECT = "AWAITING_REDIRECT"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    AWAITING_RETURN = "AWAITING_RETURN"
    CASCADING_CONFIRMATION = "CASCADING_CONFIRMATION"


class User(Base):
    """Представляет пользователя в системе."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    internal_token: Mapped[str] = mapped_column(String, nullable=False)

    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="user")


class Payment(Base):
    """Представляет платежную транзакцию."""

    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True
    )  # ID платежа от PayAdmit
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reference_id: Mapped[str] = mapped_column(String, nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(Enum(PaymentType), nullable=False)
    state: Mapped[PaymentState] = mapped_column(Enum(PaymentState), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="payments")
