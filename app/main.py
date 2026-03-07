from fastapi import FastAPI, Request, Depends, staticfiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.db.database import Base, engine, get_db
from sqlalchemy import select, text, func
from sqlalchemy.orm import Session
from app.db.tables.food import Food
from app.api.router import router 
import app.api.food_retrieval 
import app.api.food_creation
import datetime
from app.db.operative_methods import food_entries_by_date

app = FastAPI()
app.include_router(router)
static_files = staticfiles.StaticFiles(directory="app/frontend/static")
app.mount("/static", static_files, name="static")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/frontend/pages")

@app.get("/")
def home(request: Request, 
         date: datetime.datetime = datetime.datetime.now(), 
         db: Session = Depends(get_db)
         ):
    ctx = {}
    food_entries = food_entries_by_date(db, date)
    ctx["food_entries"] = food_entries

    return templates.TemplateResponse(request, "home.html", context=ctx)
