from fastapi import APIRouter, Depends
from app.db.models import User
from app.services.payment import PaymentService
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/create-payment")
async def create_payment(
    payment_data: dict,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(),
):
    """
    Создает новый депозит.
    """
    return await payment_service.create_payment(current_user.id, payment_data)


@router.post("/create-payout")
async def create_payout(
    payout_data: dict,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(),
):
    """
    Создает новую выплату.
    """
    return await payment_service.create_payout(current_user.id, payout_data)


@router.post("/create-refund")
async def create_refund(
    refund_data: dict,
    current_user: User = Depends(get_current_user),
    payment_service: PaymentService = Depends(),
):
    """
    Создает новый возврат средств.
    """
    return await payment_service.create_refund(current_user.id, refund_data)
