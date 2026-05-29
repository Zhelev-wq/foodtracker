import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.router import router
from app.db.database import get_db
from app.db.tables.food_entries import FoodEntryItem
from app.validators.food import FoodEntryItemOut


class FoodEntryItemEdit(BaseModel):
    grams: int


router = APIRouter()


@router.patch("/food_entry_item/{item_id}")
async def edit_food_entry_item(
    item_id: uuid.UUID, payload: FoodEntryItemEdit, db: AsyncSession = Depends(get_db)
) -> FoodEntryItemOut:
    result = await db.execute(select(FoodEntryItem).where(FoodEntryItem.id == item_id))
    food_entry_item = result.scalars().first()
    if not food_entry_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food entry item not found"
        )

    food_entry_item.food_grams = payload.grams

    await db.commit()
    await db.refresh(food_entry_item)

    return food_entry_item
