from fastapi import APIRouter
from .health import router as health_router
from .payments import router as payments_router


router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(payments_router, prefix="/payments", tags=["Payments"])
