from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.auth import AuthService, get_current_user
from app.db.models import User

router = APIRouter()


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register_user(user_data: UserRegister, auth_service: AuthService = Depends()):
    """
    Регистрация нового пользователя.
    """
    return await auth_service.register_user(user_data.email, user_data.password)


@router.post("/login")
async def login_user(user_data: UserLogin, auth_service: AuthService = Depends()):
    """
    Вход пользователя.
    """
    return await auth_service.authenticate_user(user_data.email, user_data.password)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.
    """
    return {"email": current_user.email, "user_id": current_user.id}
