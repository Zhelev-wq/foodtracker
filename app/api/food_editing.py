import uuid

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Fats, Food, Minerals, Vitamins
from app.db.tables.food_entries import (FoodEntry, FoodEntryItem, Recipe,
                                        RecipeEntryItem)
from app.validators.food import (CreateFoodEntryPayload, CustomFood,
                                 FoodEntryItemEdit, FoodEntryItemOut, FoodOut,
                                 RecipeItemOut)
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["food/update"])


@router.patch("/food_entry_item/{item_id}")
async def edit_food_entry_item(
    item_id: uuid.UUID,
    payload: FoodEntryItemEdit,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryItemOut:
    result = await db.execute(
        select(FoodEntryItem)
        .where(FoodEntryItem.id == item_id)
        .where(FoodEntryItem.user_id == user.id)
    )
    food_entry_item = result.scalars().first()
    if not food_entry_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food entry item not found"
        )

    food_entry_item.food_grams = payload.grams

    await db.commit()
    await db.refresh(food_entry_item)

    return food_entry_item


@router.put("/custom_food/{food_id}")
async def edit_custom_food(
    food_id: uuid.UUID,
    payload: CustomFood,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodOut:

    db_query = select(Food).where(Food.id == food_id).where(Food.user_id == user.id)

    result = await db.execute(db_query)
    existing_food = result.scalars().first()
    if not existing_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Custom food doesnt exist"
        )

    def apply(existing, data):
        for k, v in data.items():
            setattr(existing, k, v)

    apply(
        existing_food,
        payload.model_dump(exclude={"id", "user_id", "vitamins", "minerals", "fats"}),
    )

    if payload.vitamins:
        if existing_food.vitamins:
            apply(existing_food.vitamins, payload.vitamins.model_dump())
        else:
            existing_food.vitamins = Vitamins(**payload.vitamins.model_dump())

    if payload.fats:
        if existing_food.fats:
            apply(existing_food.fats, payload.fats.model_dump())
        else:
            existing_food.fats = Fats(**payload.fats.model_dump())

    if payload.minerals:
        if existing_food.minerals:
            apply(existing_food.minerals, payload.minerals.model_dump())
        else:
            existing_food.minerals = Minerals(**payload.minerals.model_dump())

    await db.commit()
    await db.refresh(existing_food)
    return existing_food


@router.put("/food_entry/{food_entry_id}")
async def edit_food_entry_food_items(
    food_entry_id: uuid.UUID,
    food_items: list[FoodEntryItemOut | CreateFoodEntryPayload],
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    if not food_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Food items not provided"
        )

    db_query = (
        select(FoodEntry)
        .where(FoodEntry.id == food_entry_id)
        .where(FoodEntry.user_id == user.id)
    )
    result = await db.execute(db_query)
    food_entry = result.scalars().first()

    if not food_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food entry with ID: {food_entry_id} not found",
        )

    incoming_existing = [
        item for item in food_items if isinstance(item, FoodEntryItemOut)
    ]  # maybe original, maybe edited
    incoming_new = [
        item for item in food_items if isinstance(item, CreateFoodEntryPayload)
    ]  # completely new
    incoming_by_id = {(item.id): item for item in incoming_existing}

    kept_items = []
    for existing_item in food_entry.food_items:
        incoming = incoming_by_id.get(existing_item.id, None)
        if incoming is not None:
            existing_item.food_grams = incoming.food_grams
            kept_items.append(existing_item)

    new_items = []
    for item in incoming_new:
        new_items.append(FoodEntryItem(food_id=item.food_uuid, food_grams=item.grams))

    food_entry.food_items = kept_items + new_items
    await db.commit()
    await db.refresh(food_entry)
    return food_entry


class EditRecipePayload(BaseModel):
    food_items: list[
        RecipeItemOut, CreateFoodEntryPayload
    ]  # TODO: validators clarification
    recipe_name: str


@router.put("/recipe/{recipe_id}")
async def edit_recipe(
    recipe_id: uuid.UUID,
    payload: EditRecipePayload,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    food_items = payload.food_items
    if not food_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Food items not provided"
        )

    db_query = (
        select(Recipe).where(Recipe.id == recipe_id).where(Recipe.user_id == user.id)
    )
    result = await db.execute(db_query)
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with ID: {recipe_id} not found.",
        )

    incoming_existing = [
        item for item in food_items if isinstance(item, RecipeItemOut)
    ]  # maybe original, maybe edited
    incoming_new = [
        item for item in food_items if isinstance(item, CreateFoodEntryPayload)
    ]  # completely new
    incoming_by_id = {(item.id): item for item in incoming_existing}

    kept_items = []
    for existing_item in recipe.food_items:
        incoming = incoming_by_id.get(existing_item.id, None)
        if incoming is not None:
            existing_item.food_grams = incoming.food_grams
            kept_items.append(existing_item)

    new_items = []
    for item in incoming_new:
        new_items.append(RecipeEntryItem(food_id=item.food_uuid, food_grams=item.grams))

    recipe_name = payload.recipe_name
    if recipe.recipe_name != recipe_name:
        recipe.recipe_name = recipe_name

    recipe.food_items = kept_items + new_items
    await db.commit()
    await db.refresh(recipe)
    return recipe
