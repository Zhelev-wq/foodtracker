import copy
import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import (create_valid_test_user, logged_in_user_details,
                            login_user, new_custom_food, valid_log_in,
                            valid_user)
from tests.constants import EXAMPLE_CUSTOM_FOOD_INPUT


@pytest.mark.anyio
async def test_custom_food_appears_in_search_results(
    client: AsyncClient, new_custom_food, valid_log_in
):
    token = valid_log_in.get("access_token")
    response = await client.get(
        f"/api/foods/{EXAMPLE_CUSTOM_FOOD_INPUT.get('name')}",
        headers={"Authorization": f"Bearer {token}"},
    )
    results = response.json()
    assert response.status_code == 200
    assert results[0].get("name") == EXAMPLE_CUSTOM_FOOD_INPUT.get("name")


@pytest.mark.anyio
async def test_custom_food_appears_in_users_custom_foods_list(
    client: AsyncClient,
    new_custom_food,
    valid_log_in,
    logged_in_user_details,
):
    token = valid_log_in.get("access_token")
    user_id = logged_in_user_details.get("id")
    response = await client.get(
        "/api/foods/custom-foods",
        headers={"Authorization": f"Bearer {token}"},
    )
    results = response.json()
    assert response.status_code == 200
    assert results[0].get("name") == EXAMPLE_CUSTOM_FOOD_INPUT.get("name")
    assert results[0].get("user_id") == user_id


@pytest.mark.anyio
async def test_custom_food_doesnt_appear_in_another_users_list(
    client: AsyncClient,
    new_custom_food,
):
    # create custom food, attempt to retrieve custom food with user 2 and fail
    await create_valid_test_user(client)
    new_user = await login_user(client)
    new_user_token = new_user.json().get("access_token")

    response = await client.get(
        "/api/foods/custom-foods",
        headers={"Authorization": f"Bearer {new_user_token}"},
    )
    results = response.json()
    assert response.status_code == 200
    assert len(results) == 0

    new_user_details = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {new_user_token}"},
    )
    new_user_details = new_user_details.json()
    new_user_id = new_user_details.get("id")

    assert new_custom_food.get("user_id") != new_user_id


@pytest.mark.anyio
async def test_custom_food_doesnt_appear_in_another_users_search_results(
    client: AsyncClient, new_custom_food
):
    await create_valid_test_user(client)
    new_user = await login_user(client)
    new_user_token = new_user.json().get("access_token")

    response = await client.get(
        f"/api/foods/{EXAMPLE_CUSTOM_FOOD_INPUT.get('name')}",
        headers={"Authorization": f"Bearer {new_user_token}"},
    )
    results = response.json()
    assert response.status_code == 200
    assert len(results) == 0


@pytest.mark.anyio
async def test_edit_custom_food(
    client: AsyncClient,
    new_custom_food,
    valid_log_in,
    logged_in_user_details,
):
    # edit food, pull food from db, verify changes

    token = valid_log_in.get("access_token")
    new_custom_food_id = new_custom_food.get("id")
    user_id = logged_in_user_details.get("id")

    new_custom_food_payload = copy.deepcopy(EXAMPLE_CUSTOM_FOOD_INPUT)
    new_custom_food_payload.update({"name": "edited_name"})

    response = await client.put(
        f"/api/foods/custom-foods/{new_custom_food_id}",
        json=new_custom_food_payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json().get("name") == "edited_name"
    assert response.json().get("id") == new_custom_food_id
    assert response.json().get("user_id") == user_id


@pytest.mark.anyio
async def test_edit_custom_food_no_auth_header(
    client: AsyncClient,
    new_custom_food,
):
    new_custom_food_id = new_custom_food.get("id")

    new_custom_food_payload = copy.deepcopy(EXAMPLE_CUSTOM_FOOD_INPUT)
    new_custom_food_payload.update({"name": "edited_name"})

    response = await client.put(
        f"/api/foods/custom-foods/{new_custom_food_id}",
        json=new_custom_food_payload,
    )

    assert response.status_code == 401


@pytest.mark.anyio
async def test_edit_custom_food_bad_schema(
    client: AsyncClient,
    new_custom_food,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    new_custom_food_id = new_custom_food.get("id")

    new_custom_food_payload = copy.deepcopy(EXAMPLE_CUSTOM_FOOD_INPUT)
    del new_custom_food_payload["name"]

    response = await client.put(
        f"/api/foods/custom-foods/{new_custom_food_id}",
        json=new_custom_food_payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_edit_custom_food_bad_food_id(
    client: AsyncClient,
    new_custom_food,
    valid_log_in,
):

    token = valid_log_in.get("access_token")
    new_custom_food_id = new_custom_food.get("id")
    non_existed_food_id = uuid.uuid4()
    assert new_custom_food_id != non_existed_food_id

    new_custom_food_payload = copy.deepcopy(EXAMPLE_CUSTOM_FOOD_INPUT)
    new_custom_food_payload.update({"name": "edited_name"})

    response = await client.put(
        f"/api/foods/custom-foods/{non_existed_food_id}",
        json=new_custom_food_payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_edit_custom_food_belonging_to_other_user(
    client: AsyncClient,
    new_custom_food,
    logged_in_user_details,
):
    await create_valid_test_user(client)
    new_user = await login_user(client)
    new_user_token = new_user.json().get("access_token")
    new_user_details = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {new_user_token}"},
    )
    new_user_id = new_user_details.json().get("id")
    default_test_user_id = logged_in_user_details.get("id")

    assert new_user_id != default_test_user_id
    assert new_custom_food.get("user_id") == default_test_user_id

    custom_food_id = new_custom_food.get("id")
    new_custom_food_payload = copy.deepcopy(EXAMPLE_CUSTOM_FOOD_INPUT)
    new_custom_food_payload.update({"name": "edited_name"})

    response = await client.put(
        f"/api/foods/custom-foods/{custom_food_id}",
        json=new_custom_food_payload,
        headers={"Authorization": f"Bearer {new_user_token}"},
    )

    assert response.status_code == 404
