from fastapi import APIRouter
from .health import router as health_router
from .payadmit_router import router as payadmit_router
from .auth import router as auth_router
from .user import router as user_router

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(payadmit_router, prefix="/payment", tags=["Payment"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/users", tags=["Users"])
