from fastapi import APIRouter, Depends, status

from app.auth.auth_service import AuthService
from app.users.schemas import UserCreate, UserOut
from app.users.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, service: UserService = Depends()
) -> UserOut:
    """Создать нового пользователя."""
    return await service.create_user(user_data)


@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_user(
    service: UserService = Depends(),
    current_user: UserOut = Depends(AuthService.get_current_user),
):
    """Удалить текущего пользователя."""
    await service.delete_user(current_user.id)
    return {"message": "Пользователь успешно удален"}
