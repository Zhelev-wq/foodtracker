from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

DATABASE_URL = URL.create(
    drivername=f"{settings.db}+asyncpg",
    username=settings.username.get_secret_value(),
    password=settings.password.get_secret_value(),
    host=str(settings.host_address),
    port=settings.port,
    database=settings.db_name,
)


engine = create_async_engine(
    DATABASE_URL,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
