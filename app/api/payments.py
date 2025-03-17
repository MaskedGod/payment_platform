from fastapi import APIRouter, Depends


from app.services.payment import PaymentService


router = APIRouter()


@router.post("/create-payment")
async def create_payment(
    user_id: int, payment_data: dict, payment_service: PaymentService = Depends()
):
    """
    Создает новый депозит.
    """
    return await payment_service.create_payment(user_id, payment_data)


@router.post("/create-payout")
async def create_payout(
    user_id: int, payout_data: dict, payment_service: PaymentService = Depends()
):
    """
    Создает новую выплату.
    """
    return await payment_service.create_payout(user_id, payout_data)


@router.post("/create-refund")
async def create_refund(
    user_id: int, refund_data: dict, payment_service: PaymentService = Depends()
):
    """
    Создает новый возврат средств.
    """
    return await payment_service.create_refund(user_id, refund_data)
