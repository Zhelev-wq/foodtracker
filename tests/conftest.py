import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from testcontainers.postgres import PostgresContainer

from app.db.database import Base, get_db
from app.main import app

pytest_plugins = ["anyio"]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def setup_container():
    postgres = PostgresContainer(
        image="postgres:18.4",
        username="test",
        password="test",
        dbname="test_food",
        driver="asyncpg",
    )
    postgres.start()

    yield postgres

    postgres.stop()


@pytest.fixture(scope="session")
async def test_engine(setup_container):
    engine = create_async_engine(setup_container.get_connection_url())
    return engine


@pytest.fixture(scope="session")
async def test_db(setup_container, test_engine):
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION pg_trgm"))
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session(test_engine, test_db, setup_container):
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()


@pytest.fixture
async def client(db_session):

    async def swap_db():
        yield db_session

    app.dependency_overrides[get_db] = swap_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200, "Status code should be 200"


@pytest.mark.anyio
async def test_db_query(db_session):
    await db_session.execute(text("SELECT 1"))
