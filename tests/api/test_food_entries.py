import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.tables.food_entries import FoodEntry
from tests.conftest import common_food, create_valid_test_user, login_user
from tests.constants import EXAMPLE_CUSTOM_FOOD_INPUT


@pytest.mark.anyio
async def test_create_food_entry_multiple_items(
    client: AsyncClient, new_custom_food, valid_log_in, db_session
):
    token = valid_log_in.get("access_token")
    new_custom_food_id = new_custom_food.get("id")

    new_common_food = await common_food(db_session, EXAMPLE_CUSTOM_FOOD_INPUT)
    new_common_food_id = str(new_common_food.id)

    response = await client.post(
        "/api/food-entries",
        json=[
            {"food_uuid": new_custom_food_id, "grams": 100},
            {"food_uuid": new_common_food_id, "grams": 100},
        ],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    food_entry = response.json()
    food_items = food_entry.get("food_items")
    assert len(food_items) == 2
    assert food_items[0].get("food_id") != food_items[1].get("food_id")


@pytest.mark.anyio
async def test_create_food_entry_no_auth(
    client: AsyncClient,
    new_custom_food,
):
    food_id = new_custom_food.get("id")
    response = await client.post(
        "/api/food-entries",
        json=[{"food_uuid": food_id, "grams": 100}],
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_create_food_entry_bad_schema(
    client: AsyncClient,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    response = await client.post(
        "/api/food-entries",
        json=[{"grams": 100}],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_food_entry_wrong_ids(
    client: AsyncClient,
    valid_log_in,
    new_custom_food,
):
    token = valid_log_in.get("access_token")
    food_id = new_custom_food.get("id")
    non_existed_id = str(uuid.uuid4())

    assert food_id != non_existed_id

    response = await client.post(
        "/api/food-entries",
        json=[{"food_uuid": non_existed_id, "grams": 100}],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_food_entry_other_users_custom_food(
    client: AsyncClient, new_custom_food, logged_in_user_details
):
    await create_valid_test_user(client)
    new_test_user = await login_user(client)

    new_test_user_token = new_test_user.json().get("access_token")
    new_test_user_details = await client.post(
        "/api/users/me",
        headers={"Authorization": f"Bearer {new_test_user_token}"},
    )
    new_test_user_id = new_test_user_details.json().get("id")
    test_user_id = logged_in_user_details.get("id")

    assert new_test_user_id != test_user_id

    custom_food_id = new_custom_food.get("id")
    response = await client.post(
        "/api/food-entries",
        json=[{"food_uuid": custom_food_id, "grams": 100}],
        headers={"Authorization": f"Bearer {new_test_user_token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_food_entry_appears_in_log(
    client: AsyncClient,
    valid_log_in,
    logged_in_user_details,
    new_food_entry_single_item,
):
    token = valid_log_in.get("access_token")
    today = datetime.date.today()
    response = await client.get(
        f"/api/food-entries/{today}",
        headers={"Authorization": f"Bearer {token}"},
    )
    results = response.json()
    user_id = logged_in_user_details.get("id")
    assert response.status_code == 200
    assert len(results) == 1
    assert results[0].get("user_id") == user_id


@pytest.mark.anyio
async def test_food_entry_appears_only_for_owner(
    client: AsyncClient, new_food_entry_single_item
):
    await create_valid_test_user(client)
    new_test_user = await login_user(client)

    new_test_user_token = new_test_user.json().get("access_token")
    today = datetime.date.today()

    response = await client.get(
        f"/api/food-entries/{today}",
        headers={"Authorization": f"Bearer {new_test_user_token}"},
    )
    results = response.json()

    assert response.status_code == 200
    assert len(results) == 0


@pytest.mark.anyio
async def test_edit_food_entry_correct_info(
    client: AsyncClient, valid_log_in, new_food_entry_single_item
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_single_item.get("id")
    existing_grams = new_food_entry_single_item.get("food_items")[0].get("food_grams")
    new_grams = 101

    assert existing_grams != new_grams

    food_entry_items = new_food_entry_single_item.get("food_items")
    food_entry_item_id = food_entry_items[0].get("id")

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=[{"id": food_entry_item_id, "food_grams": new_grams}],
        headers={"Authorization": f"Bearer {token}"},
    )
    new_food_entry_state = response.json()
    assert response.status_code == 200
    assert new_food_entry_state != new_food_entry_single_item
    assert existing_grams != new_food_entry_state.get("food_items")[0].get("food_grams")
    assert new_grams == new_food_entry_state.get("food_items")[0].get("food_grams")


@pytest.mark.anyio
async def test_edit_food_entry_no_auth(client: AsyncClient, new_food_entry_single_item):
    food_entry_id = new_food_entry_single_item.get("id")
    existing_grams = new_food_entry_single_item.get("food_items")[0].get("food_grams")
    new_grams = 101

    assert existing_grams != new_grams

    food_entry_items = new_food_entry_single_item.get("food_items")
    food_entry_item_id = food_entry_items[0].get("id")

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=[{"id": food_entry_item_id, "food_grams": new_grams}],
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_edit_food_entry_bad_schema(
    client: AsyncClient, valid_log_in, new_custom_food, new_food_entry_single_item
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_single_item.get("id")
    existing_grams = new_food_entry_single_item.get("food_items")[0].get("food_grams")
    new_grams = 101

    assert existing_grams != new_grams
    food_entry_items = new_food_entry_single_item.get("food_items")
    food_entry_item_id = food_entry_items[0].get("id")

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=[
            {
                "id": food_entry_item_id,
            }
        ],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_edit_food_entry_adjust_all_items_correct_info(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")

    food_entry_id = new_food_entry_multi_item.get("id")
    food_entry_items = new_food_entry_multi_item.get("food_items")
    edit_food_entry_payload = [
        {"id": item.get("id"), "food_grams": item.get("food_grams") + 1}
        for item in food_entry_items
    ]

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    food_entry_edited = response.json()
    food_items_edited = food_entry_edited.get("food_items")
    live_data = {item.get("id"): item.get("food_grams") for item in food_items_edited}
    submitted_data = {
        item.get("id"): item.get("food_grams") for item in edit_food_entry_payload
    }
    assert live_data == submitted_data


@pytest.mark.anyio
async def test_edit_food_entry_add_new_items_and_change_existing(
    client: AsyncClient, new_food_entry_multi_item, valid_log_in, db_session
):

    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")
    food_entry_items = new_food_entry_multi_item.get("food_items")

    third_food = await common_food(db_session, EXAMPLE_CUSTOM_FOOD_INPUT)
    third_food_id = str(third_food.id)
    third_food_grams = 100

    edit_food_entry_payload = [
        {"id": item.get("id"), "food_grams": item.get("food_grams") + 1}
        for item in food_entry_items
    ]
    edit_food_entry_payload.append(
        {"food_uuid": third_food_id, "grams": third_food_grams}
    )

    assert len(edit_food_entry_payload) == 3

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    food_entry_edited_items = response.json().get("food_items")
    assert len(food_entry_edited_items) == 3

    third_food_entry_id = None
    for item in food_entry_edited_items:
        if item.get("food_id") == third_food_id:
            third_food_entry_id = item.get("id")
    assert third_food_entry_id is not None

    submitted_data = {
        item.get("id"): item.get("food_grams")
        for item in edit_food_entry_payload
        if item.get("id") is not None
    }
    submitted_data.update({third_food_entry_id: third_food_grams})

    live_data = {
        item.get("id"): item.get("food_grams") for item in food_entry_edited_items
    }
    assert live_data == submitted_data


@pytest.mark.anyio
async def test_edit_food_entry_remove_item(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")
    food_entry_items = new_food_entry_multi_item.get("food_items")

    edit_food_entry_payload = [
        {
            "id": food_entry_items[0].get("id"),
            "food_grams": food_entry_items[0].get("food_grams"),
        }
    ]
    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    food_entry_edited = response.json()
    food_items_edited = food_entry_edited.get("food_items")
    live_data = {item.get("id"): item.get("food_grams") for item in food_items_edited}
    submitted_data = {
        item.get("id"): item.get("food_grams") for item in edit_food_entry_payload
    }
    assert live_data == submitted_data


@pytest.mark.anyio
async def test_edit_food_entry_remove_all_items(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=[],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


@pytest.mark.anyio
async def test_edit_food_entry_replace_all_items(
    client: AsyncClient, new_food_entry_multi_item, valid_log_in, db_session
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")
    food_entry_items = new_food_entry_multi_item.get("food_items")

    third_food = await common_food(db_session, EXAMPLE_CUSTOM_FOOD_INPUT)
    third_food_id = str(third_food.id)
    third_food_grams = 100

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=[{"food_uuid": third_food_id, "grams": third_food_grams}],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    food_entry_edited_items = response.json().get("food_items")
    assert len(food_entry_edited_items) == 1

    live_data = [item.get("id") for item in food_entry_edited_items]
    previous_data = [item.get("id") for item in food_entry_items]
    for id in previous_data:
        assert id not in live_data


@pytest.mark.anyio
async def test_edit_food_entry_bad_id(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")
    non_existent_id = str(uuid.uuid4())
    assert food_entry_id != non_existent_id

    food_entry_items = new_food_entry_multi_item.get("food_items")
    edit_food_entry_payload = [
        {"id": item.get("id"), "food_grams": item.get("food_grams") + 1}
        for item in food_entry_items
    ]
    response = await client.put(
        f"/api/food-entries/{non_existent_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_edit_food_entry_belonging_to_other_user(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")

    await create_valid_test_user(client)
    login_info = await login_user(client)
    test_user_token = login_info.json().get("access_token")
    assert token != test_user_token

    food_entry_items = new_food_entry_multi_item.get("food_items")
    edit_food_entry_payload = [
        {"id": item.get("id"), "food_grams": item.get("food_grams") + 1}
        for item in food_entry_items
    ]
    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_edit_food_entry_with_non_existent_food(
    client: AsyncClient,
    new_food_entry_multi_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_multi_item.get("id")
    non_existent_food_id = str(uuid.uuid4())

    food_entry_items = new_food_entry_multi_item.get("food_items")
    edit_food_entry_payload = [
        {"id": item.get("id"), "food_grams": item.get("food_grams") + 1}
        for item in food_entry_items
    ]
    edit_food_entry_payload.append({"food_uuid": non_existent_food_id, "grams": 100})
    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_edit_food_entry_with_food_belonging_to_other_user(
    client: AsyncClient, new_custom_food, db_session
):
    await create_valid_test_user(client)
    login_info = await login_user(client)
    test_user_token = login_info.json().get("access_token")
    test_user_details = await client.post(
        "/api/tests/me",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    test_user_id = test_user_details.json().get("id")
    assert new_custom_food.get("user_id") != test_user_id

    normal_food = await common_food(db_session)
    response = await client.post(
        "/api/food-entries",
        json=[{"food_uuid": str(normal_food.id), "grams": 100}],
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 201

    food_entry = response.json()
    food_entry_id = food_entry.get("id")
    food_entry_items = food_entry.get("food_items")
    new_custom_food_id = new_custom_food.get("id")

    edit_food_entry_payload = [
        {
            "id": food_entry_items[0].get("id"),
            "food_grams": food_entry_items[0].get("food_grams"),
        },
        {"food_uuid": new_custom_food_id, "grams": 100},
    ]

    response = await client.put(
        f"/api/food-entries/{food_entry_id}",
        json=edit_food_entry_payload,
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_remove_food_entry(
    client: AsyncClient, new_food_entry_single_item, valid_log_in, db_session
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_single_item.get("id")

    response = await client.delete(
        f"/api/food-entries/{food_entry_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    query = select(FoodEntry).where(FoodEntry.id == food_entry_id)
    result = await db_session.execute(query)
    result = result.scalars().all()
    assert len(result) == 0


@pytest.mark.anyio
async def test_remove_food_entry_no_auth(
    client: AsyncClient,
    new_food_entry_single_item,
):
    food_entry_id = new_food_entry_single_item.get("id")
    response = await client.delete(
        f"/api/food-entries/{food_entry_id}",
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_remove_food_entry_bad_id(
    client: AsyncClient,
    new_food_entry_single_item,
    valid_log_in,
):
    token = valid_log_in.get("access_token")
    food_entry_id = new_food_entry_single_item.get("id")
    non_existent_id = str(uuid.uuid4())
    assert food_entry_id != non_existent_id

    response = await client.delete(
        f"/api/food-entries/{non_existent_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


@pytest.mark.anyio
async def test_remove_food_entry_belonging_to_other_user(
    client: AsyncClient,
    new_food_entry_single_item,
):
    food_entry_id = new_food_entry_single_item.get("id")
    await create_valid_test_user(client)
    login_data = await login_user(client)
    access_token = login_data.json().get("access_token")

    response = await client.delete(
        f"/api/food-entries/{food_entry_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
