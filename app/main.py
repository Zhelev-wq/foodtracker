from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="app/frontend/pages")

@app.get("/")
def home(request: Request):
    ctx = {}
    return templates.TemplateResponse(request, "base.html", context=ctx)