from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/frontend/pages")

@app.get("/")
def home(request: Request):
    ctx = {}
    return templates.TemplateResponse(request, "base.html", context=ctx)