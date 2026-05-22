from app.api.router import router
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.tables.food import Food
from app.db.tables.food_entries import FoodEntry
import datetime
import uuid
from app.validators.food import FoodEntryOut, FoodOut


@router.get("/search/name/{food_name}")
def search_food_by_name(
    food_name: str,
    iteration: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
) -> list[FoodOut]:  # fuzzy search, will return 20 results of things with similarity to food_name
    food_query = (
        select(Food)
        .where(Food.name.op("%")(food_name))
        .order_by(func.similarity(Food.name, food_name).label("sim").desc())
        .offset((iteration - 1) * page_size)
        .limit(page_size)
    )
    food_results = db.scalars(food_query).all()
    return food_results


@router.get("/search/specific/")
def search_food_by_uuid(
    food_uuid: uuid.UUID | None = None,
    barcode: str | None = None,
    db: Session = Depends(get_db),
):
    if food_uuid and barcode:
        return JSONResponse(content={"error": "Provide only single parameter"})

    if not any([food_uuid, barcode]):
        return JSONResponse(content={"error": "Provide arguments shithead"})
    food = None
    if food_uuid:
        food = db.get(Food, food_uuid)
    if barcode and int(barcode):
        food = db.scalars(select(Food).where(Food.barcode == barcode)).first()

    if not food:
        return JSONResponse(content={"error": "Food doesn't exist"})

    return JSONResponse(content=jsonable_encoder(food))


@router.get("/search/date/{date}")
def search_food_entries_by_date(
    date: datetime.datetime, db: Session = Depends(get_db)
) -> list[FoodEntryOut]:

    db_query = select(FoodEntry).where(func.date(FoodEntry.time) == date.date())
    food_entries = db.scalars(db_query).all()
    return food_entries



@router.get("/search/food_entries/all")
def all_food_entries(db: Session = Depends(get_db)) -> list[FoodEntryOut]:
    entries = db.scalars(select(FoodEntry)).all()
    return entries
