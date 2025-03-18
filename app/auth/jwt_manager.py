import jwt
from datetime import datetime, timedelta, timezone
from app.config.settings import settings


class JWTManager:
    def __init__(self):
        self.private_key = settings.AUTH_JWT.private_key_path.read_text()
        self.public_key = settings.AUTH_JWT.public_key_path.read_text()
        self.algorithm = settings.AUTH_JWT.algorithm
        self.token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    def create_token(self, user_id: int) -> str:
        """Создаёт JWT-токен для пользователя."""
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + self.token_expiry,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.private_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        """Декодирует и валидирует JWT-токен."""
        return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
