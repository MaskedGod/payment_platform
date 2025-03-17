from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.db.models import User
from app.db.database import get_db
from app.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    """Обслуживание аутентификации пользователей."""

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def register_user(self, email: str, password: str):
        """
        Регистрация нового пользователя.
        """
        try:
            user = (
                await self.db.execute(select(User).where(User.email == email))
            ).scalar_one()
        except NoResultFound:
            user = None

        if user:
            raise HTTPException(
                status_code=400, detail="Пользователь с таким email уже существует"
            )

        hashed_password = self._hash_password(password)
        internal_token = self._generate_jwt(email)

        new_user = User(
            email=email, hashed_password=hashed_password, internal_token=internal_token
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return {
            "message": "Пользователь успешно зарегистрирован",
            "user_id": new_user.id,
        }

    async def authenticate_user(self, email: str, password: str):
        """
        Аутентификация пользователя.
        """
        try:
            user = (
                await self.db.execute(select(User).where(User.email == email))
            ).scalar_one()
        except NoResultFound:
            user = None

        if not user or not self._verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверные учетные данные")

        return {"access_token": user.internal_token, "token_type": "bearer"}

    def _hash_password(self, password: str) -> str:
        """Хэширует пароль."""
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль."""
        return pwd_context.verify(plain_password, hashed_password)

    def _generate_jwt(self, email: str) -> str:
        """Генерирует JWT токен."""
        payload = {
            "sub": email,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Проверяет JWT токен и возвращает текущего пользователя.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Недействительный токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен")

    try:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
