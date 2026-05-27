from app.api.router import router
from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from app.db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.tables.food_entries import FoodEntry, FoodEntryItem
import uuid

@router.delete("/delete/food_entry/{food_entry_uuid}")
def remove_food_entry(
    food_entry_uuid: uuid.UUID, 
    db: Session = Depends(get_db)
):

    food_entry = db.execute(select(FoodEntry).where(FoodEntry.id == food_entry_uuid)).scalars().first()

    if not food_entry:
        return JSONResponse(content={"status": "Error: Food entry doesn't exist"}, status_code=404)
    
    db.delete(food_entry)
    db.commit()

    return JSONResponse(content={"status": "Success. Food entry deleted"}, status_code=200)