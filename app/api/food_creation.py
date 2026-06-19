import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Fats, Food, Minerals, Vitamins
from app.db.tables.food_entries import (FoodEntry, FoodEntryItem, Recipe,
                                        RecipeEntryItem)
from app.validators.food import (CreateFoodEntryPayload, CreateRecipePayload,
                                 CustomFood, FoodEntryOut)

router = APIRouter(tags=["food/create"])


@router.post("/food_entry")
async def create_food_entry(
    payload: list[CreateFoodEntryPayload],
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOut:

    food_ids = [food_entry.food_uuid for food_entry in payload]
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
            detail="Food not fount. Cannot create entry",
        )

    food_entry = FoodEntry(
        food_items=[
            FoodEntryItem(food_id=item.food_uuid, food_grams=item.grams)
            for item in payload
        ],
        user_id=user.id,
    )
    db.add(food_entry)
    await db.commit()
    await db.refresh(food_entry)
    return food_entry


@router.post("/custom_food")
async def create_custom_food(
    payload: CustomFood, user: CurrentUser, db: AsyncSession = Depends(get_db)
):

    custom_food = Food(
        name=payload.name,
        carbs=payload.carbs,
        protein=payload.protein,
        fat=payload.fat,
        kcal=payload.kcal,
        alcohol=payload.alcohol,
        caffeine=payload.caffeine,
        barcode=payload.barcode,
        vitamins=Vitamins(
            **payload.vitamins.model_dump() if payload.vitamins else None
        ),
        fats=Fats(**payload.fats.model_dump() if payload.fats else None),
        minerals=Minerals(
            **payload.minerals.model_dump() if payload.minerals else None
        ),
        user_id=user.id,
    )

    db.add(custom_food)
    await db.commit()
    await db.refresh(custom_food)

    return custom_food


@router.post("/recipe")
async def create_recipe(
    payload: CreateRecipePayload, user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    # TODO: solve duplicate naming

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
            detail="Food not fount. Cannot create entry",
        )

    recipe = Recipe(
        recipe_name=payload.recipe_name,
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


@router.post("/entry_from_recipe/{recipe_id}")
async def create_entry_from_recipe(
    recipe_id: uuid.UUID,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    db_query = (
        select(Recipe).where(Recipe.id == recipe_id).where(Recipe.user_id == user.id)
    )
    result = await db.execute(db_query)
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not")

    food_entry = FoodEntry(
        food_items=[
            FoodEntryItem(food_id=item.food_id, food_grams=item.food_grams)
            for item in recipe.food_items
        ],
        user_id=user.id,
        name=recipe.recipe_name,
    )

    db.add(food_entry)
    await db.commit()
    await db.refresh(food_entry)

    return food_entry
