from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "keys" / "jwt-public.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    PAYADMIT_API_URL: str
    API_KEY: str
    SIGN_KEY: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    AUTH_JWT: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
