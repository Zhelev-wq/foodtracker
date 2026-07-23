import datetime
import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
from app.validators.entries.entries_input import EntryItemInput, ExistingEntryItemInput
from app.validators.entries.entries_output import FoodEntryOutput

router = APIRouter(tags=["food_entries"])


@router.get("/{date}")
async def search_food_entries_by_date(
    date: datetime.date, user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> list[FoodEntryOutput]:

    db_query = (
        select(FoodEntry)
        .where(FoodEntry.user_id == user.id)
        .where(func.date(FoodEntry.time) == date)
    )
    results = await db.execute(db_query)
    food_entries = results.scalars().all()
    return food_entries


@router.post("", status_code=status.HTTP_201_CREATED)
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


@router.put("/{food_entry_id}")
async def edit_food_entry_food_items(
    food_entry_id: uuid.UUID,
    food_items: list[
        ExistingEntryItemInput | EntryItemInput
    ],  # recheck later if FoodEntryItemOutput is the right model for this job
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodEntryOutput:
    if not food_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Food items not provided"
        )

    db_query = (
        select(FoodEntry)
        .where(FoodEntry.id == food_entry_id)
        .where(FoodEntry.user_id == user.id)
    )
    result = await db.execute(db_query)
    food_entry = result.scalars().first()

    if not food_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food entry with ID: {food_entry_id} not found",
        )

    incoming_existing = [
        item for item in food_items if isinstance(item, ExistingEntryItemInput)
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
    for existing_item in food_entry.food_items:
        incoming = incoming_by_id.get(existing_item.id, None)
        if incoming is not None:
            existing_item.food_grams = incoming.food_grams
            kept_items.append(existing_item)

    new_items = []
    for item in incoming_new:
        new_items.append(FoodEntryItem(food_id=item.food_uuid, food_grams=item.grams))

    food_entry.food_items = kept_items + new_items
    await db.commit()

    result = await db.execute(
        select(FoodEntry)
        .where(FoodEntry.id == food_entry.id)
        .options(selectinload(FoodEntry.food_items).selectinload(FoodEntryItem.food))
    )
    food_entry = result.scalars().first()
    return food_entry


@router.delete("/{food_entry_uuid}", status_code=status.HTTP_204_NO_CONTENT)
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
