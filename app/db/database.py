from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import settings


engine = create_async_engine(settings.DATABASE_URL)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    "Dependency to get database session"
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase):
    pass
