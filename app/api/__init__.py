from fastapi import APIRouter
from .health import router as health_router
from .payment import router as payment_router
from .auth import router as auth_router
from .user import router as user_router
from .webhooks import router as webhook_router

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(payment_router, prefix="/payments", tags=["Payment"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(webhook_router, prefix="/webhooks", tags=["Webhooks"])
