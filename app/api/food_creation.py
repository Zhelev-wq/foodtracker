from app.api.router import router
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, func, insert
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
from app.db.tables.food import Food
import uuid

from pydantic import BaseModel

class CreateFoodEntryBody(BaseModel):
    #TODO: temporary store, move later
    food_uuid: uuid.UUID
    grams: float

@router.post("/create_food_entry")
def create_food_entry(
    body: CreateFoodEntryBody, db: Session = Depends(get_db)
):
    food_item = db.execute(select(Food).where(Food.id == body.food_uuid)).scalars().first()

    if not food_item:
        return JSONResponse(content={"error": "Food doesn't exist"})

    food_entry = FoodEntry(
        food_items=[FoodEntryItem(food_id=body.food_uuid, food_grams=body.grams)]
    )
    db.add(food_entry)
    db.commit()

    return JSONResponse(content={"error": "error processing entry"})


@router.post("/create_custom_food")
def create_custom_food(): ...
