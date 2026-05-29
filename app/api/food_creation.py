import uuid

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
from app.validators.food import FoodEntryOut


class CreateFoodEntryPayload(BaseModel):
    # temp location, move to other place, TODO
    food_uuid: uuid.UUID
    grams: int


router = APIRouter()


@router.post("/food_entry")
async def create_food_entry(
    request: Request,
    payload: CreateFoodEntryPayload,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOut:

    result = await db.execute(select(Food).where(Food.id == payload.food_uuid))
    food = result.scalars().first()

    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not fount. Cannot create entry",
        )

    food_entry = FoodEntry(
        food_items=[FoodEntryItem(food_id=payload.food_uuid, food_grams=payload.grams)]
    )
    db.add(food_entry)
    await db.commit()
    await db.refresh(food_entry)
    return food_entry


@router.post("/customer_food")
def create_custom_food(): ...
