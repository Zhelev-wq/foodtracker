from dotenv import dotenv_values
from sqlalchemy import Column, MetaData, Table
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

config = dotenv_values("./app/.env")
db = config.get("db")
username = config.get("username")
password = config.get("password")
host_address = config.get("host_address")
port = config.get("port")


engine = create_async_engine(
    f"{db}+asyncpg://{username}:{password}@{host_address}:{port}/food", echo=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
