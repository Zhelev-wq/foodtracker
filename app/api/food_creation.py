import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
from app.validators.food import FoodEntryOut


class CreateFoodEntryPayload(BaseModel):
    # temp location, move to other place, TODO
    food_uuid: uuid.UUID
    grams: int


router = APIRouter(tags=["food/create"])


@router.post("/food_entry")
async def create_food_entry(
    payload: list[CreateFoodEntryPayload],
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOut:

    food_ids = [food_entry.food_uuid for food_entry in payload]
    result = await db.execute(
        select(Food).where(
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


@router.post("/customer_food")
def create_custom_food(): ...
