import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from testcontainers.postgres import PostgresContainer

from app.db.database import Base, get_db
from app.db.tables.food import Food
from app.main import app
from tests.constants import (DEFAULT_NAME, DEFAULT_WORKING_EMAIL,
                             DEFAULT_WORKING_PASSWORD,
                             EXAMPLE_CUSTOM_FOOD_INPUT)

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


async def create_valid_test_user(
    client: AsyncClient,
    email: str = "test_email@nonexistent.com",
    password: str = "test_password",
    name: str = "test_name",
):
    response = await client.post(
        "/api/users", json={"email": email, "password": password, "name": name}
    )
    assert response.status_code == 201
    return response


async def login_user(
    client: AsyncClient,
    email: str = "test_email@nonexistent.com",
    password: str = "test_password",
):

    response = await client.post(
        "/api/users/token", data={"username": email, "password": password}
    )

    assert response.status_code == 200
    return response


@pytest.fixture
async def valid_user(client: AsyncClient):
    response = await create_valid_test_user(
        client=client,
        email=DEFAULT_WORKING_EMAIL,
        password=DEFAULT_WORKING_PASSWORD,
        name=DEFAULT_NAME,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def valid_log_in(client: AsyncClient, valid_user):
    response = await login_user(
        client=client, email=DEFAULT_WORKING_EMAIL, password=DEFAULT_WORKING_PASSWORD
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def logged_in_user_details(client: AsyncClient, valid_user, valid_log_in):

    token = valid_log_in.get("access_token")
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
async def new_custom_food(
    client: AsyncClient, valid_user, valid_log_in, logged_in_user_details, db_session
):
    token = valid_log_in.get("access_token")
    response = await client.post(
        "/api/foods/custom-foods",
        json=EXAMPLE_CUSTOM_FOOD_INPUT,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201

    user_id = logged_in_user_details.get("id")
    food_id = response.json().get("id")

    result = await db_session.execute(select(Food).where(Food.id == food_id))
    result = result.scalars().all()

    assert len(result) > 0
    assert len(result) < 2
    assert str(result[0].user_id) == user_id

    return response.json()
