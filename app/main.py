from fastapi import FastAPI, Request, Depends, APIRouter
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
import app.api.food_removal
import app.api.food_editing
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/frontend/pages")

@app.get("/")
def home(request: Request):
    ctx = {}
    return templates.TemplateResponse(request, "base.html", context=ctx)