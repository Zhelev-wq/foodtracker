import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry, FoodEntryItem, Recipe, RecipeEntryItem
from app.validators.entries.entries_input import (
    EntryItemInput,
    ExistingRecipeItemInput,
    RecipeEdit,
    RecipeInput,
)
from app.validators.entries.entries_output import FoodEntryOutput, RecipeOutput

router = APIRouter(tags=["recipes"])


@router.get("")
async def get_user_recipes(
    user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> list[RecipeOutput]:
    db_query = select(Recipe).where(Recipe.user_id == user.id)

    results = await db.execute(db_query)
    recipes = results.scalars().all()

    return recipes


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_recipe(
    payload: RecipeInput, user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> RecipeOutput:

    food_ids = [food_entry.food_uuid for food_entry in payload.food_items]
    result = await db.execute(
        select(Food)
        .where(Food.id.in_(food_ids))
        .where(
            or_(
                Food.user_id == user.id, Food.user_id.is_(None)
            )  # custom food belonging to user, or common food
        )
    )
    food = result.scalars().all()

    if len(food) != len(food_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found. Cannot create entry",
        )

    recipe = Recipe(
        name=payload.name,
        food_items=[
            RecipeEntryItem(food_id=item.food_uuid, food_grams=item.grams)
            for item in payload.food_items
        ],
        user_id=user.id,
    )
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.put("/{recipe_id}")
async def edit_recipe(
    recipe_id: uuid.UUID,
    payload: RecipeEdit,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> RecipeOutput:
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
        item for item in food_items if isinstance(item, ExistingRecipeItemInput)
    ]  # maybe original, maybe edited
    incoming_new = [
        item for item in food_items if isinstance(item, EntryItemInput)
    ]  # completely new
    db_query = (
        select(Food)
        .where(Food.id.in_([item.food_uuid for item in incoming_new]))
        .where(or_(Food.user_id == user.id, Food.user_id.is_(None)))
    )
    result = await db.execute(db_query)
    result = result.scalars().all()
    if len(result) != len(incoming_new):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="New food entry items not found or don't belong to user",
        )

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

    name = payload.name
    if recipe.name != name:
        recipe.name = name

    recipe.food_items = kept_items + new_items
    await db.commit()
    result = await db.execute(
        select(Recipe)
        .where(Recipe.id == recipe.id)
        .options(selectinload(Recipe.food_items).selectinload(RecipeEntryItem.food))
    )
    recipe = result.scalars().first()
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_recipe(
    recipe_id: uuid.UUID, user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Recipe).where(Recipe.id == recipe_id).where(Recipe.user_id == user.id)
    )

    recipe = result.scalars().first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    await db.delete(recipe)
    await db.commit()


@router.post("/{recipe_id}/food-entries", status_code=status.HTTP_201_CREATED)
async def create_entry_from_recipe(
    recipe_id: uuid.UUID,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOutput:
    db_query = (
        select(Recipe).where(Recipe.id == recipe_id).where(Recipe.user_id == user.id)
    )
    result = await db.execute(db_query)
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )

    food_entry = FoodEntry(
        food_items=[
            FoodEntryItem(food_id=item.food_id, food_grams=item.food_grams)
            for item in recipe.food_items
        ],
        user_id=user.id,
        name=recipe.name,
    )

    db.add(food_entry)
    await db.commit()
    await db.refresh(food_entry)

    return food_entry
