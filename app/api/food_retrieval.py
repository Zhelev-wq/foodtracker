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


@router.get("/search/name/{food_name}")
def search_food_by_name(
    request: Request,
    food_name: str,
    iteration: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):  # fuzzy search, will return 20 results of things with similarity to food_name
    food_query = (
        select(Food)
        .where(func.similarity(Food.name, food_name) > 0.3)
        .order_by(func.similarity(Food.name, food_name).desc())
        .offset((iteration - 1) * page_size)
        .limit(page_size)
    )
    food_results = db.scalars(food_query).all()
    return JSONResponse(content=jsonable_encoder(food_results))


@router.get("/search/specific/")
def search_food_by_uuid(
    request: Request,
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
    request: Request, date: datetime.datetime, db: Session = Depends(get_db)
):

    db_query = select(FoodEntry).where(func.date(FoodEntry.time) == date.date())
    food_entries = db.scalars(db_query).all()

    if food_entries:
        return JSONResponse(content=jsonable_encoder(food_entries))
    else:
        return JSONResponse(content={"entries": "None"})


@router.get("/search/food_entries/all")
def all_food_entries(request: Request, db: Session = Depends(get_db)):
    entries = db.scalars(select(FoodEntry)).all()
    return JSONResponse(content=jsonable_encoder(entries))
