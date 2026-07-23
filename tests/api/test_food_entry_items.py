import datetime
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.db.tables.food_entries import Recipe
from tests.conftest import common_food, create_valid_test_user, login_user
from tests.constants import DEFAULT_RECIPE_NAME, EXAMPLE_CUSTOM_FOOD_INPUT


@pytest.mark.anyio
async def test_edit_food_entry_item(
    client: AsyncClient, food_entry_from_recipe, valid_log_in
):
    token = valid_log_in.get("access_token")
    food_items = food_entry_from_recipe.get("food_items")
    food_entry_item = food_items[0]
    food_entry_item_id = food_entry_item.get("id")
    food_entry_item_grams = food_entry_item.get("food_grams")

    response = await client.patch(
        f"/api/food-entry-items/{food_entry_item_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"grams": food_entry_item_grams + 50},
    )
    assert response.status_code == 200
    edited_item = response.json()
    assert food_entry_item_grams != edited_item.get("food_grams")


@pytest.mark.anyio
async def test_edit_food_entry_item_no_auth(
    client: AsyncClient, food_entry_from_recipe
):
    food_items = food_entry_from_recipe.get("food_items")
    food_entry_item = food_items[0]
    food_entry_item_id = food_entry_item.get("id")
    food_entry_item_grams = food_entry_item.get("food_grams")

    response = await client.patch(
        f"/api/food-entry-items/{food_entry_item_id}",
        json={"grams": food_entry_item_grams + 50},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_edit_food_entry_item_bad_id(
    client: AsyncClient, food_entry_from_recipe, valid_log_in
):
    token = valid_log_in.get("access_token")
    food_items = food_entry_from_recipe.get("food_items")
    food_entry_item = food_items[0]
    food_entry_item_id = food_entry_item.get("id")
    food_entry_item_grams = food_entry_item.get("food_grams")
    non_existent_id = str(uuid.uuid4())

    assert food_entry_item_id != non_existent_id

    response = await client.patch(
        f"/api/food-entry-items/{non_existent_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"grams": food_entry_item_grams + 50},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_edit_food_entry_item_bad_schema(
    client: AsyncClient, food_entry_from_recipe, valid_log_in
):
    token = valid_log_in.get("access_token")
    food_items = food_entry_from_recipe.get("food_items")
    food_entry_item = food_items[0]
    food_entry_item_id = food_entry_item.get("id")
    food_entry_item_grams = food_entry_item.get("food_grams")

    response = await client.patch(
        f"/api/food-entry-items/{food_entry_item_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"gramss": food_entry_item_grams + 50},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_edit_food_entry_item_belonging_to_other_user(
    client: AsyncClient, food_entry_from_recipe
):
    food_items = food_entry_from_recipe.get("food_items")
    food_entry_item = food_items[0]
    food_entry_item_id = food_entry_item.get("id")
    food_entry_item_grams = food_entry_item.get("food_grams")

    await create_valid_test_user(client)
    new_test_user = await login_user(client)
    new_test_user_token = new_test_user.json().get("access_token")

    response = await client.patch(
        f"/api/food-entry-items/{food_entry_item_id}",
        headers={"Authorization": f"Bearer {new_test_user_token}"},
        json={"grams": food_entry_item_grams + 50},
    )
    assert response.status_code == 404
