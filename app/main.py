from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.foods import router as food_router
from app.api.recipes import router as recipe_router
from app.api.food_entries import router as food_entry_router
from app.api.food_entry_items import router as food_entry_item_router

from app.api.user import router as user_router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)
app.include_router(food_router, prefix="/api/foods")
app.include_router(recipe_router, prefix="/api/recipes")
app.include_router(food_entry_router, prefix="/api/food-entries")
app.include_router(user_router, prefix="/api/users")
app.include_router(food_entry_item_router, prefix="/api/food-entry-items")

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

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
