from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.jwt_manager import JWTManager
from app.db.database import get_db
from app.users.user_service import UserService
from app.users.schemas import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session
        self.jwt_manager = JWTManager()

    async def authenticate_user(self, email: str, password: str) -> UserOut:
        """Проверяет учетные данные пользователя и возвращает его данные."""
        user_service = UserService(self.session)
        user = await user_service.verify_user_credentials(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )
        return user

    def create_access_token(self, user_id: int) -> str:
        """Создаёт и возвращает JWT-токен."""
        return self.jwt_manager.create_token(user_id)

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db),
    ) -> UserOut:
        """Получает текущего пользователя из JWT-токена."""
        jwt_manager = JWTManager()
        try:
            payload = jwt_manager.decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
                )
            user_service = UserService(session)
            user = await user_service.get_user_by_id(int(user_id))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Пользователь не найден",
                )
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен истёк")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен")
