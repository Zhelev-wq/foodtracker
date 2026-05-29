import datetime
import uuid

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.router import router
from app.db.database import get_db
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry
from app.validators.food import FoodEntryOut, FoodOut

router = APIRouter()


@router.get("/search/name/{food_name}")
async def search_food_by_name(
    food_name: str,
    iteration: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[
    FoodOut
]:  # fuzzy search, will return 20 results of things with similarity to food_name
    food_query = (
        select(Food)
        .where(Food.name.op("%")(food_name))
        .order_by(func.similarity(Food.name, food_name).label("sim").desc())
        .offset((iteration - 1) * page_size)
        .limit(page_size)
    )
    results = await db.scalars(food_query)
    food_results = results.all()
    return food_results


@router.get("/search/specific/")
async def search_food_by_uuid(
    food_uuid: uuid.UUID | None = None,
    barcode: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> FoodOut:
    if food_uuid and barcode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provide only one: UUID or barcode",
        )

    if not any([food_uuid, barcode]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Provide either UUID or barcode",
        )

    food = None
    if food_uuid:
        food = await db.get(Food, food_uuid)
    if barcode and int(barcode):
        result = await db.scalars(select(Food).where(Food.barcode == barcode))
        food = result.first()

    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Food not found"
        )
    return food


@router.get("/search/date/{date}")
async def search_food_entries_by_date(
    date: datetime.datetime, db: AsyncSession = Depends(get_db)
) -> list[FoodEntryOut]:

    db_query = select(FoodEntry).where(func.date(FoodEntry.time) == date.date())
    results = await db.execute(db_query)
    food_entries = results.scalars().all()
    return food_entries
