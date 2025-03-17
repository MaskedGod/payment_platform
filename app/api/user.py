from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.users.schemas import UserCreate, UserUpdate, UserOut
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


@router.get("/", response_model=List[UserOut])
async def get_all_users(service: UserService = Depends()) -> list[UserOut]:
    """Получить всех пользователей."""
    return await service.get_all_users()


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, user_data: UserUpdate, service: UserService = Depends()
) -> UserOut:
    """Обновить данные пользователя."""
    user: UserOut | None = await service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends()):
    """Удалить пользователя по его ID."""
    deleted: bool = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return {"Пользователь удалён": deleted}


@router.post("/login", response_model=UserOut)
async def login_user(
    credentials: UserCreate, service: UserService = Depends()
) -> UserOut:
    """Аутентифицировать пользователя по email и паролю."""
    return await service.authenticate_user(
        credentials.email,
        credentials.hashed_password,
    )
