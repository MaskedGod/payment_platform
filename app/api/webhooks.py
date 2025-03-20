from fastapi import APIRouter, Request, HTTPException

# import hmac
# import hashlib
import logging

# from app.config.settings import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/payment_status")
async def payment_status_webhook(request: Request):
    """
    Эндпоинт для обработки вебхуков от PayAdmit.
    """
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")

        payment_id = data.get("id")
        state = data.get("state")
        payment_type = data.get("paymentType")
        amount = data.get("amount")
        currency = data.get("currency")
        error_code = data.get("errorCode")

        logger.info(
            f"Payment ID: {payment_id}, State: {state}, Payment Type: {payment_type}, "
            f"Amount: {amount} {currency}, Error Code: {error_code}"
        )

        if state == "COMPLETED":
            logger.info(f"Payment {payment_id} completed successfully")
            # Обновить статус платежа в БД
            # Например: update_payment_status(payment_id, "COMPLETED")
        elif state == "FAILED" or state == "DECLINED":
            logger.warning(f"Payment {payment_id} failed or declined")
            # Уведомить пользователя о сбое
            # Например: notify_user(payment_id, "FAILED")
        else:
            logger.info(f"Payment {payment_id} has status: {state}")

        return {"message": "Webhook processed successfully"}

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# @router.post("/payment_state")
# async def payment_state_webhook(request: Request):
#     signature = request.headers.get("Signature")
#     body = await request.body()

#     # Верификация подписи
#     expected_signature = hmac.new(
#         key=settings.PAYADMIT_SIGN_KEY.encode(), msg=body, digestmod=hashlib.sha256
#     ).hexdigest()

#     if signature != expected_signature:
#         return {"error": "Invalid signature"}, 400


#     data = await request.json()
#     payment_id = data.get("payment_id")
#     state = data.get("state")
#     print(f"{payment_id=}\n{state=}")
#     print(data)

#     if state == "COMPLETED":
#         # Обновить статус платежа в БД
#         # Например, обновить запись в базе данных
#         pass
#     elif state == "DECLINED":
#         # Уведомить пользователя о сбое
#         # Например, отправить email или уведомление
#         pass

#     return {"message": "Webhook processed successfully"}
