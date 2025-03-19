from fastapi import APIRouter, HTTPException, Depends

from app.auth.auth_service import AuthService
from app.payments.payments_service import PayAdmitService
from app.payments.schemas import (
    CreatePaymentRequest,
    CreateRefundRequest,
    PaymentConfirmationType,
)
from app.users.models import User

router = APIRouter()


@router.get("/payments")
async def get_payments(
    limit: int = 10,
    offset: int = 0,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Получает список всех платежей через API PayAdmit.

    Параметры:
    - limit (int): Количество элементов для возврата (по умолчанию 10).
    - offset (int): Количество элементов для пропуска (по умолчанию 0).

    Возвращает:
    - Список платежей в формате JSON.

    Исключения:
    - HTTPException: если произошла ошибка при выполнении запроса к API.
    """
    try:
        return await payadmit_service.get_payments(limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e


@router.post("/payments")
async def create_payment(
    request: CreatePaymentRequest,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Создает новый платеж через API PayAdmit.
    Параметры:
    - amount (int): сумма платежа.
    - currency (str): валюта платежа.
    Возвращает:
    - Информацию о созданном платеже.
    Исключения:
    - HTTPException: если произошла ошибка при создании платежа.
    """
    try:
        return await payadmit_service.create_payment(
            user,
            request.amount,
            request.currency,
            request.customer,
        )
    except HTTPException as e:
        raise e


@router.post("/payouts")
async def create_payout(
    request: CreatePaymentRequest,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Создает новую выплату через API PayAdmit.
    Параметры:
    - amount (int): сумма выплаты.
    - currency (str): валюта выплаты.
    Возвращает:
    - Информацию о созданной выплате.
    Исключения:
    - HTTPException: если произошла ошибка при создании выплаты.
    """
    try:
        return await payadmit_service.create_payment(
            user,
            request.amount,
            request.currency,
            request.customer,
        )
    except HTTPException as e:
        raise e


@router.post("/payouts/confirm")
async def confirm_payout(
    request: PaymentConfirmationType,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Подтверждает выплату через API PayAdmit.
    Параметры:
    - payout_id (int): идентификатор выплаты для подтверждения.
    Возвращает:
    - Информацию о подтверждении выплаты.
    Исключения:
    - HTTPException: если произошла ошибка при подтверждении выплаты.
    """
    try:
        return await payadmit_service.confirm_payout(request.payment_id)
    except HTTPException as e:
        raise e


@router.post("/payments/refund")
async def create_refund(
    request: CreateRefundRequest,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Создает возврат средств для конкретного платежа через API PayAdmit.
    Параметры:
    - payment_id (int): идентификатор платежа для возврата.
    Возвращает:
    - Информацию о возврате средств.
    Исключения:
    - HTTPException: если произошла ошибка при создании возврата.
    """
    try:
        return await payadmit_service.create_refund(
            user, request.amount, request.currency, request.parentPaymentId
        )
    except HTTPException as e:
        raise e


@router.get("/payments/status")
async def check_status(
    payment_id: str,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Проверяет статус конкретного платежа через API PayAdmit.
    Параметры:
    - payment_id (int): идентификатор платежа для проверки статуса.
    Возвращает:
    - Информацию о текущем статусе платежа.
    Исключения:
    - HTTPException: если произошла ошибка при проверке статуса.
    """
    print(payment_id)
    try:
        return await payadmit_service.check_status(payment_id)
    except HTTPException as e:
        raise e


@router.get("/operations")
async def get_operations(
    payment_id: str,
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Получает список всех операций через API PayAdmit.
    Возвращает:
    - Список операций в формате JSON.
    Исключения:
    - HTTPException: если произошла ошибка при получении списка операций.
    """
    try:
        return await payadmit_service.get_operations(payment_id)
    except HTTPException as e:
        raise e


@router.get("/balance")
async def get_balance(
    user: User = Depends(AuthService.get_current_user),
    payadmit_service: PayAdmitService = Depends(),
):
    """
    Получает текущий баланс через API PayAdmit.
    Возвращает:
    - Информацию о балансе аккаунта.
    Исключения:
    - HTTPException: если произошла ошибка при получении баланса.
    """
    try:
        return await payadmit_service.get_balance(user)
    except HTTPException as e:
        raise e
