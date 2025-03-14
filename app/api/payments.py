from fastapi import APIRouter, Depends


from app.services.payment import PaymentService


router = APIRouter()


@router.post("/create-payment")
async def create_payment(
    user_id: int,
    payment_data: dict,
    payment_service: PaymentService = Depends(PaymentService),
):
    """
    Endpoint to create a new payment (DEPOSIT).
    """
    payment = await payment_service.create_payment(user_id, payment_data)
    return {"message": "Payment created successfully", "payment": payment}


@router.post("/create-payout")
async def create_payout(
    user_id: int,
    payout_data: dict,
    payment_service: PaymentService = Depends(PaymentService),
):
    """
    Endpoint to create a new payout (WITHDRAWAL).
    """
    payout = await payment_service.create_payout(user_id, payout_data)
    return {"message": "Payout created successfully", "payout": payout}


@router.post("/create-refund")
async def create_refund(
    user_id: int,
    refund_data: dict,
    payment_service: PaymentService = Depends(PaymentService),
):
    """
    Endpoint to create a new refund (REFUND).
    """
    refund = await payment_service.create_refund(user_id, refund_data)
    return {"message": "Refund created successfully", "refund": refund}
