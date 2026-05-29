import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.tables.food_entries import FoodEntry, FoodEntryItem

router = APIRouter()


@router.delete("/food_entry/{food_entry_uuid}")
async def remove_food_entry(
    food_entry_uuid: uuid.UUID, db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(FoodEntry).where(FoodEntry.id == food_entry_uuid))
    food_entry = result.scalars().first()
    if not food_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food entry item not found"
        )

    await db.delete(food_entry)
    await db.commit()

    return food_entry
