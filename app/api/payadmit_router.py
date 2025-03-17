from fastapi import APIRouter, HTTPException, Depends
from app.payadmit_integration.payadmit_service import PayAdmitService

router = APIRouter()


@router.get("/payments")
async def get_payments(payadmit_service: PayAdmitService = Depends()):
    """
    Получает список всех платежей через API PayAdmit.
    Возвращает:
    - Список платежей в формате JSON.
    Исключения:
    - HTTPException: если произошла ошибка при выполнении запроса к API.
    """
    try:
        return await payadmit_service.get_payments()
    except HTTPException as e:
        raise e


@router.post("/payments")
async def create_payment(
    amount: int, currency: str, payadmit_service: PayAdmitService = Depends()
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
        return await payadmit_service.create_payment(amount, currency)
    except HTTPException as e:
        raise e


@router.post("/payouts")
async def create_payout(
    amount: int, currency: str, payadmit_service: PayAdmitService = Depends()
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
        return await payadmit_service.create_payout(amount, currency)
    except HTTPException as e:
        raise e


@router.post("/refunds")
async def create_refund(payment_id: int, payadmit_service: PayAdmitService = Depends()):
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
        return await payadmit_service.create_refund(payment_id)
    except HTTPException as e:
        raise e


@router.post("/payouts/{payout_id}/confirm")
async def confirm_payout(payout_id: int, payadmit_service: PayAdmitService = Depends()):
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
        return await payadmit_service.confirm_payout(payout_id)
    except HTTPException as e:
        raise e


@router.get("/payments/{payment_id}/status")
async def check_status(payment_id: int, payadmit_service: PayAdmitService = Depends()):
    """
    Проверяет статус конкретного платежа через API PayAdmit.
    Параметры:
    - payment_id (int): идентификатор платежа для проверки статуса.
    Возвращает:
    - Информацию о текущем статусе платежа.
    Исключения:
    - HTTPException: если произошла ошибка при проверке статуса.
    """
    try:
        return await payadmit_service.check_status(payment_id)
    except HTTPException as e:
        raise e


@router.get("/operations")
async def get_operations(payadmit_service: PayAdmitService = Depends()):
    """
    Получает список всех операций через API PayAdmit.
    Возвращает:
    - Список операций в формате JSON.
    Исключения:
    - HTTPException: если произошла ошибка при получении списка операций.
    """
    try:
        return await payadmit_service.get_operations()
    except HTTPException as e:
        raise e


@router.get("/balance")
async def get_balance(payadmit_service: PayAdmitService = Depends()):
    """
    Получает текущий баланс через API PayAdmit.
    Возвращает:
    - Информацию о балансе аккаунта.
    Исключения:
    - HTTPException: если произошла ошибка при получении баланса.
    """
    try:
        return await payadmit_service.get_balance()
    except HTTPException as e:
        raise e


@router.post("/blacklist")
async def update_blacklist(
    blacklist: list, payadmit_service: PayAdmitService = Depends()
):
    """
    Обновляет черный список через API PayAdmit.
    Параметры:
    - blacklist (list): список объектов для черного списка.
    Возвращает:
    - Результат обновления черного списка.
    Исключения:
    - HTTPException: если произошла ошибка при обновлении черного списка.
    """
    try:
        return await payadmit_service.update_blacklist(blacklist)
    except HTTPException as e:
        raise e


@router.post("/whitelist")
async def update_whitelist(
    whitelist: list, payadmit_service: PayAdmitService = Depends()
):
    """
    Обновляет белый список через API PayAdmit.
    Параметры:
    - whitelist (list): список объектов для белого списка.
    Возвращает:
    - Результат обновления белого списка.
    Исключения:
    - HTTPException: если произошла ошибка при обновлении белого списка.
    """
    try:
        return await payadmit_service.update_whitelist(whitelist)
    except HTTPException as e:
        raise e
