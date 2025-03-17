from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate, UserOut
from app.users.utils import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> UserOut:
        """Создать нового пользователя."""
        hashed_password = hash_password(user_data.hashed_password)

        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return UserOut(id=new_user.id, email=new_user.email)

    async def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        """Получить пользователя по его ID."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user:
            return UserOut(id=user.id, email=user.email)
        return None

    async def get_all_users(self) -> List[UserOut]:
        """Получить всех пользователей."""
        query = select(User)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [UserOut(id=user.id, email=user.email) for user in users]

    async def update_user(
        self, user_id: int, user_data: UserUpdate
    ) -> Optional[UserOut]:
        """Обновить данные пользователя."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            return None

        user.email = user_data.email
        await self.session.commit()
        await self.session.refresh(user)
        return UserOut(id=user.id, email=user.email)

    async def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя по его ID."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True

    async def authenticate_user(self, email: str, password: str) -> Optional[UserOut]:
        """Аутентифицировать пользователя по email и паролю."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        return UserOut(id=user.id, email=user.email)
