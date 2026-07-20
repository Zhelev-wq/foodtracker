import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import delete

from app.db.tables.user import User
from tests.conftest import create_valid_test_user, login_user


@pytest.mark.anyio
async def test_create_duplicate_user(client: AsyncClient):
    response = await create_valid_test_user(
        client=client, email="working_email1@email.com", password="working_password"
    )
    assert response.status_code == 201
    response = await client.post(
        "/api/users",
        json={"email": "working_email1@email.com", "password": "working_password"},
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_create_multiple_users(client: AsyncClient):
    await create_valid_test_user(
        client=client, email="working_email@email.com", password="working_password"
    )
    await create_valid_test_user(
        client=client, email="working_email_1@email.com", password="working_password2"
    )


@pytest.mark.anyio
async def test_user_creation_validation_failure(client: AsyncClient):

    response = await client.post(
        "/api/users", json={"email": "working_email@email.com", "password": ""}
    )
    assert response.status_code == 422

    response = await client.post(
        "/api/users", json={"email": "bad_email_str", "password": "working_password"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_wrong_login_info(client: AsyncClient):
    await create_valid_test_user(
        client=client, email="working_email1@email.com", password="working_password"
    )
    response = await login_user(
        client=client, email="working_email1@email.com", password="working_password"
    )
    assert response.status_code == 200

    response = await client.post(
        "/api/users/token",
        data={"username": "working_email1@email.com", "password": "wrong_password"},
    )
    assert response.status_code == 401

    response = await client.post(
        "/api/users/token",
        data={"username": "non_working@email.com", "password": "working_password"},
    )
    assert response.status_code == 401

    response = await client.post(
        "/api/users/token",
        data={"username": "non_working@email.com", "password": "wrong_password"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_logged_in_user_correct_data(client: AsyncClient):
    email = "working_email1@email.com"
    name = "users_first_name"
    await create_valid_test_user(
        client=client, email=email, password="working_password", name=name
    )
    response = await login_user(client=client, email=email, password="working_password")
    token = response.json().get("access_token")

    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == email
    assert uuid.UUID(response.json().get("id"))
    assert response.json().get("name") == name


@pytest.mark.anyio
async def test_user_login_corrupted_data(client: AsyncClient, db_session: AsyncSession):
    email = "working_email1@email.com"
    name = "users_first_name"
    await create_valid_test_user(
        client=client, email=email, password="working_password", name=name
    )
    response = await login_user(client=client, email=email, password="working_password")
    correct_token = response.json().get("access_token")
    wrong_token = correct_token[1:]

    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {wrong_token}"},
    )
    assert response.status_code == 401

    await db_session.execute(delete(User).where(User.email == email))
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {correct_token}"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_update_user_correct_data(client: AsyncClient, db_session: AsyncSession):

    email = "working_email1@email.com"
    name = "users_first_name"
    await create_valid_test_user(
        client=client, email=email, password="working_password", name=name
    )
    response = await login_user(client=client, email=email, password="working_password")
    token = response.json().get("access_token")
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    user_details = response.json()
    user_id = user_details.get("id")
    initial_email = user_details.get("email")
    initial_user_name = user_details.get("name")

    new_name = "new_name"

    response = await client.patch(
        f"/api/users/{user_id}",
        json={"name": new_name, "email": initial_email},
        headers={"Authorization": f"Bearer {token}"},
    )
    current_name = response.json().get("name")
    current_email = response.json().get("email")

    assert response.status_code == 200
    assert current_name != initial_user_name
    assert current_name == new_name
    assert current_email == initial_email

    new_email = "new_email@email.com"
    response = await client.patch(
        f"/api/users/{user_id}",
        json={"name": new_name, "email": new_email},
        headers={"Authorization": f"Bearer {token}"},
    )
    current_name = response.json().get("name")
    current_email = response.json().get("email")

    assert response.status_code == 200
    assert current_name == new_name
    assert current_email != initial_email
    assert new_email == current_email


@pytest.mark.anyio
async def test_update_user_wrong_user_id(client: AsyncClient):
    email_one = "working_email1@email.com"
    name_one = "users_first_name"
    password_one = "working_password_one"
    await create_valid_test_user(
        client=client, email=email_one, password=password_one, name=name_one
    )
    response = await login_user(client=client, email=email_one, password=password_one)
    token_one = response.json().get("access_token")
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token_one}"},
    )
    user_id_one = response.json().get("id")

    non_existent_id = uuid.uuid4()
    response = await client.patch(
        f"/api/users/{non_existent_id}",
        json={"email": "correct_email@email.com", "name": "correct_name"},
        headers={"Authorization": f"Bearer {token_one}"},
    )
    response_data = response.json()
    assert response.status_code == 403
    assert "name" not in response_data.keys()
    assert "email" not in response_data.keys()

    #### using user_1 id with user_2's token

    email_two = "working_email2@email.com"
    name_two = "users_second_name"
    password_two = "working_password_two"
    await create_valid_test_user(
        client=client, email=email_two, password=password_two, name=name_two
    )
    response = await login_user(client=client, email=email_two, password=password_two)
    token_two = response.json().get("access_token")
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token_two}"},
    )
    user_id_two = response.json().get("id")

    assert user_id_one != user_id_two

    response = await client.patch(
        f"/api/users/{user_id_one}",
        json={"email": "correct_email@email.com", "name": "correct_name"},
        headers={"Authorization": f"Bearer {token_two}"},
    )

    response_data = response.json()
    assert response.status_code == 403
    assert "name" not in response_data.keys()
    assert "email" not in response_data.keys()

    ### changing user_1's email to user_2's
    assert email_one != email_two
    response = await client.patch(
        f"/api/users/{user_id_one}",
        json={
            "email": email_two,
            "name": "correct_name",
        },
        headers={"Authorization": f"Bearer {token_one}"},
    )

    assert response.status_code == 400

#TODO: resort test functions, introduce fixtures, 
# update_user db missing info tests