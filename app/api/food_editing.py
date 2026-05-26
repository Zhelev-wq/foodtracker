from app.api.router import router
from fastapi import Depends
from fastapi.responses import JSONResponse

from app.db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
import uuid

from pydantic import BaseModel


class FoodEntryItemEdit(BaseModel):
    grams: int

@router.patch("/edit/food_entry_item/{item_id}")
def edit_food_entry_item(
    item_id: uuid.UUID, payload: FoodEntryItemEdit, db: Session = Depends(get_db)
):
    food_entry_item = db.execute(select(FoodEntryItem).where(FoodEntryItem.id == item_id)).scalars().first()
    if not food_entry_item:
        return JSONResponse(content={"status":"entry not found"}, status_code=404)
    
    food_entry_item.food_grams = payload.grams
    
    db.commit()

    return JSONResponse(content={"status":"success"}, status_code=200)