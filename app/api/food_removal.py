import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food_entries import FoodEntry, Recipe

router = APIRouter(tags=["food/delete"])


@router.delete("/food_entry/{food_entry_uuid}")
async def remove_food_entry(
    food_entry_uuid: uuid.UUID, user: CurrentUser, db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(FoodEntry)
        .where(FoodEntry.id == food_entry_uuid)
        .where(FoodEntry.user_id == user.id)
    )
    food_entry = result.scalars().first()
    if not food_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food entry not found"
        )

    await db.delete(food_entry)
    await db.commit()


@router.delete("/recipe/{recipe_id}")
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
