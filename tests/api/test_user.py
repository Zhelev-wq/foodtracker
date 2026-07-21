import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import delete

from app.db.tables.user import User
from tests.conftest import (create_valid_test_user, logged_in_user_details,
                            login_user, valid_log_in, valid_user)
from tests.constants import (DEFAULT_NAME, DEFAULT_WORKING_EMAIL,
                             DEFAULT_WORKING_PASSWORD)


@pytest.mark.anyio
async def test_create_duplicate_user(client: AsyncClient, valid_user):
    response = await client.post(
        "/api/users",
        json={"email": DEFAULT_WORKING_EMAIL, "password": DEFAULT_WORKING_PASSWORD},
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_create_multiple_users(client: AsyncClient):
    await create_valid_test_user(
        client=client, email=DEFAULT_WORKING_EMAIL, password=DEFAULT_WORKING_PASSWORD
    )
    await create_valid_test_user(
        client=client, email="working_email_2@email.com", password="working_password2"
    )


@pytest.mark.anyio
async def test_user_creation_empty_password(client: AsyncClient):
    response = await client.post(
        "/api/users", json={"email": DEFAULT_WORKING_EMAIL, "password": ""}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_user_creation_short_password(client: AsyncClient):
    response = await client.post(
        "/api/users", json={"email": DEFAULT_WORKING_EMAIL, "password": "1234"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_user_creation_bad_email_string(client: AsyncClient):
    response = await client.post(
        "/api/users",
        json={"email": "bad_email_str", "password": DEFAULT_WORKING_PASSWORD},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_wrong_password(client: AsyncClient, valid_user):
    response = await client.post(
        "/api/users/token",
        data={"username": DEFAULT_WORKING_EMAIL, "password": "wrong_password"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_wrong_email(client: AsyncClient, valid_user):
    response = await client.post(
        "/api/users/token",
        data={
            "username": "non_working@email.com",
            "password": DEFAULT_WORKING_PASSWORD,
        },
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_wrong_email_and_password(client: AsyncClient, valid_user):
    response = await client.post(
        "/api/users/token",
        data={"username": "non_working@email.com", "password": "wrong_password"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_user_login_no_email(
    client: AsyncClient, db_session: AsyncSession, valid_log_in
):
    response = await client.post(
        "/api/users/token",
        data={"password": DEFAULT_WORKING_PASSWORD},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_user_login_no_password(
    client: AsyncClient, db_session: AsyncSession, valid_log_in
):
    response = await client.post(
        "/api/users/token",
        data={"username": DEFAULT_WORKING_EMAIL},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_logged_in_user_correct_data(client: AsyncClient, valid_log_in):

    token = valid_log_in.get("access_token")

    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json().get("email") == DEFAULT_WORKING_EMAIL
    assert uuid.UUID(response.json().get("id"))
    assert response.json().get("name") == DEFAULT_NAME


@pytest.mark.anyio
async def test_user_login_corrupted_data(client: AsyncClient, valid_log_in):

    correct_token = valid_log_in.get("access_token")
    wrong_token = correct_token[1:]

    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {wrong_token}"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_user_login_email_doesnt_exist(
    client: AsyncClient, db_session: AsyncSession, valid_log_in
):
    token = valid_log_in.get("access_token")
    await db_session.execute(delete(User).where(User.email == DEFAULT_WORKING_EMAIL))
    response = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_update_user_correct_name(
    client: AsyncClient,
    valid_log_in,
    logged_in_user_details,
):

    new_name = "new_name"
    token = valid_log_in.get("access_token")
    user_id = logged_in_user_details.get("id")
    initial_email = logged_in_user_details.get("email")
    initial_user_name = logged_in_user_details.get("name")
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


@pytest.mark.anyio
async def test_update_user_correct_email(
    client: AsyncClient,
    valid_log_in,
    logged_in_user_details,
):
    new_email = "new_email@email.com"
    token = valid_log_in.get("access_token")
    user_id = logged_in_user_details.get("id")
    initial_email = logged_in_user_details.get("email")
    initial_user_name = logged_in_user_details.get("name")

    response = await client.patch(
        f"/api/users/{user_id}",
        json={"name": initial_user_name, "email": new_email},
        headers={"Authorization": f"Bearer {token}"},
    )
    current_email = response.json().get("email")

    assert response.status_code == 200
    assert current_email != initial_email
    assert new_email == current_email


@pytest.mark.anyio
async def test_update_user_mismatched_id(
    client: AsyncClient, valid_log_in, logged_in_user_details
):

    token = valid_log_in.get("access_token")
    user_id = logged_in_user_details.get("id")
    non_existent_id = uuid.uuid4().__str__()
    assert user_id != non_existent_id

    response = await client.patch(
        f"/api/users/{non_existent_id}",
        json={"email": "correct_email@email.com", "name": "correct_name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    response_data = response.json()
    assert response.status_code == 403
    assert "name" not in response_data.keys()
    assert "email" not in response_data.keys()


@pytest.mark.anyio
async def test_update_user_wrong_user_id(client: AsyncClient, logged_in_user_details):
    user_id_one = logged_in_user_details.get("id")

    await create_valid_test_user(
        client=client,
        email="working_email2@email.com",
        password="working_password_two",
        name="users_second_name",
    )
    response = await login_user(
        client=client, email="working_email2@email.com", password="working_password_two"
    )
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


@pytest.mark.anyio
async def test_update_user_using_existing_user_email(
    client: AsyncClient, valid_log_in, logged_in_user_details
):
    ### changing user_1's email to user_2's
    token = valid_log_in.get("access_token")
    user_id_one = logged_in_user_details.get("id")
    email_one = logged_in_user_details.get("email")
    email_two = "working_email2@email.com"
    await create_valid_test_user(
        client=client,
        email=email_two,
        password="working_password_two",
        name="users_second_name",
    )
    assert email_one != email_two
    response = await client.patch(
        f"/api/users/{user_id_one}",
        json={
            "email": email_two,
            "name": "correct_name",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400


@pytest.mark.anyio
async def test_update_user_no_auth_header(client: AsyncClient, logged_in_user_details):
    new_email = "new_email@email.com"
    user_id = logged_in_user_details.get("id")
    initial_user_name = logged_in_user_details.get("name")

    response = await client.patch(
        f"/api/users/{user_id}",
        json={"name": initial_user_name, "email": new_email},
    )

    assert response.status_code == 401
