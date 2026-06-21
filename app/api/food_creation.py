import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Fats, Food, Minerals, Vitamins
from app.db.tables.food_entries import (FoodEntry, FoodEntryItem, Recipe,
                                        RecipeEntryItem)
from app.validators.entries.entries_input import EntryItemInput, RecipeInput
from app.validators.entries.entries_output import FoodEntryOutput, RecipeOutput
from app.validators.food.food_input import CustomFoodInput
from app.validators.food.food_output import FoodOutput

router = APIRouter(tags=["food/create"])


@router.post("/food_entry")
async def create_food_entry(
    payload: list[EntryItemInput],
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOutput:
    # normal use case is single-item entry, but options included for multi-item
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
            detail="Food not found. Cannot create entry",
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
    payload: CustomFoodInput, user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> FoodOutput:

    custom_food = Food(
        name=payload.name,
        carbs=payload.carbs,
        protein=payload.protein,
        fat=payload.fat,
        kcal=payload.kcal,
        alcohol=payload.alcohol,
        caffeine=payload.caffeine,
        barcode=payload.barcode,
        user_id=user.id,
    )

    if payload.vitamins:
        custom_food.vitamins=Vitamins(
            **payload.vitamins.model_dump()
        )
    else:
        custom_food.vitamins=None
    
    if payload.fats:        
        custom_food.fats=Fats(**payload.fats.model_dump())
    else:
        custom_food.fats=None
        
    if payload.minerals:
        custom_food.minerals=Minerals(
            **payload.minerals.model_dump()
        )
    else:
        custom_food.minerals = None

    db.add(custom_food)
    await db.commit()
    await db.refresh(custom_food)

    return custom_food


@router.post("/recipe")
async def create_recipe(
    payload: RecipeInput, user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> RecipeOutput:
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
            detail="Food not found. Cannot create entry",
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
) -> FoodEntryOutput:
    db_query = (
        select(Recipe).where(Recipe.id == recipe_id).where(Recipe.user_id == user.id)
    )
    result = await db.execute(db_query)
    recipe = result.scalars().first()

    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

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
