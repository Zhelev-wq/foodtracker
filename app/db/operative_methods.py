from sqlalchemy import select, func
from app.db.tables.food_entries import FoodEntry
import datetime
from sqlalchemy.orm import Session

def food_entries_by_date(db: Session, date: datetime.datetime):
    db_query = select(FoodEntry).where(func.date(FoodEntry.time) == date.date())
    food_entries = db.scalars(db_query).all()
    return food_entries