from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.food_creation import router as food_creation_router
from app.api.food_editing import router as food_editing_router
from app.api.food_removal import router as food_remove_router
from app.api.food_retrieval import router as food_retrieval_router
from app.api.user import router as user_router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, separate_input_output_schemas=False)
app.include_router(
    food_creation_router,
    prefix="/api/food_create",
)
app.include_router(food_editing_router, prefix="/api/food_edit")
app.include_router(food_remove_router, prefix="/api/food_delete")
app.include_router(food_retrieval_router, prefix="/api/food_get")
app.include_router(user_router, prefix="/api/users")

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
