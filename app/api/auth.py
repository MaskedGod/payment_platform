from fastapi import APIRouter

from app.auth.schemas import TokenInfo


router = APIRouter()


@router.post("/login", response_model=TokenInfo)
def auth_jwt():
    pass
