from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserOut
from app.users.utils import hash_password, verify_password


class UserService:
    """
    Сервис для работы с пользователями.
    Обеспечивает CRUD-операции для пользователей и проверку учетных данных.
    """

    def __init__(self, session: AsyncSession = Depends(get_db)):
        """
        Инициализирует сервис с сессией базы данных.

        :param session: Асинхронная сессия SQLAlchemy для работы с базой данных.
        """
        self.session = session

    async def create_user(self, user_data: UserCreate) -> UserOut:
        """
        Создаёт нового пользователя в базе данных.

        :param user_data: Данные для создания пользователя (email и пароль).
        :return: Созданный пользователь в формате UserOut.
        """
        hashed_password = hash_password(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_password)

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return UserOut(id=new_user.id, email=new_user.email)

    async def verify_user_credentials(
        self, email: str, password: str
    ) -> UserOut | None:
        """
        Проверяет учетные данные пользователя (email и пароль).

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: Данные пользователя в формате UserOut, если учетные данные верны.
                 Возвращает None, если пользователь не найден или пароль неверный.
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if user and verify_password(password, user.hashed_password):
            return UserOut(id=user.id, email=user.email)
        return None

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получает пользователя по его ID.

        :param user_id: ID пользователя.
        :return: Объект пользователя, если найден. В противном случае None.
        """
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя из базы данных.

        :param user_id: ID пользователя, которого нужно удалить.
        :raises HTTPException: Если пользователь не найден.
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        await self.session.delete(user)
        await self.session.commit()
