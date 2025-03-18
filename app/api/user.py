from fastapi import APIRouter, Depends, HTTPException, status

from app.users.schemas import UserCreate, UserOut
from app.users.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate, service: UserService = Depends()
) -> UserOut:
    """Создать нового пользователя."""
    return await service.create_user(user_data)


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, service: UserService = Depends()) -> UserOut:
    """Получить пользователя по его ID."""
    user: UserOut | None = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user
