from fastapi import APIRouter, Depends
from app.auth.auth_service import AuthService
from app.users.schemas import UserCreate, UserOut
from app.auth.schemas import TokenInfo

router = APIRouter()


@router.post("/login", response_model=TokenInfo)
async def login(credentials: UserCreate, service: AuthService = Depends()) -> TokenInfo:
    """Авторизация пользователя и получение JWT-токена."""
    user = await service.authenticate_user(credentials.email, credentials.password)
    token = service.create_access_token(user.id)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/me", response_model=UserOut)
async def get_current_user(
    current_user: UserOut = Depends(AuthService.get_current_user),
) -> UserOut:
    """Получает текущего пользователя по токену."""
    return current_user
