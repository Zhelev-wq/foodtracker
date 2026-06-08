import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Fats, Food, Minerals, Vitamins
from app.db.tables.food_entries import FoodEntryItem
from app.validators.food import CustomFood, FoodEntryItemOut, FoodOut


class FoodEntryItemEdit(BaseModel):
    grams: int


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
