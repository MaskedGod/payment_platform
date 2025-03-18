from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserOut
from app.users.utils import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> UserOut:
        """Создаёт нового пользователя."""
        hashed_password = hash_password(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_password)

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserOut(id=new_user.id, email=new_user.email)

    async def get_user_by_id(self, user_id: int) -> UserOut | None:
        """Возвращает пользователя по ID, если он существует."""
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return UserOut(id=user.id, email=user.email) if user else None

    async def verify_user_credentials(
        self, email: str, password: str
    ) -> UserOut | None:
        """Проверяет email и пароль пользователя."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user and verify_password(password, user.hashed_password):
            return UserOut(id=user.id, email=user.email)
        return None
