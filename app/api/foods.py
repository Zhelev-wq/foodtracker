import uuid

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import CurrentUser
from app.db.database import get_db
from app.db.tables.food import Fats, Food, Minerals, Vitamins
from app.validators.food.food_input import CustomFoodInput
from app.validators.food.food_output import FoodOutput

router = APIRouter(tags=["foods"])


@router.get("/custom-foods")
async def get_user_custom_food(
    user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> list[FoodOutput]:
    db_query = select(Food).where(Food.user_id == user.id)

    results = await db.execute(db_query)
    custom_foods = results.scalars().all()

    return custom_foods


@router.get("/{food_name}")
async def search_food_by_name(
    user: CurrentUser,
    food_name: str,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[
    FoodOutput
]:  # fuzzy search, will return 20 results of things with similarity to food_name
    food_query = (
        select(Food)
        .where(Food.name.op("%")(food_name))
        .where(
            or_(
                Food.user_id == user.id, Food.user_id.is_(None)
            )  # custom food belonging to user, or common food
        )
        .order_by(func.similarity(Food.name, food_name).label("sim").desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    results = await db.scalars(food_query)
    food_results = results.all()
    return food_results


@router.post("/custom-foods", status_code=status.HTTP_201_CREATED)
async def create_custom_food(
    payload: CustomFoodInput, user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> FoodOutput:

    custom_food = Food(
        name=payload.name,
        carbs=payload.carbs,
        protein=payload.protein,
        fat=payload.fat,
        kcal=payload.kcal,
        alcohol=payload.alcohol,
        caffeine=payload.caffeine,
        barcode=payload.barcode,
        user_id=user.id,
    )

    if payload.vitamins:
        custom_food.vitamins = Vitamins(**payload.vitamins.model_dump())
    else:
        custom_food.vitamins = None

    if payload.fats:
        custom_food.fats = Fats(**payload.fats.model_dump())
    else:
        custom_food.fats = None

    if payload.minerals:
        custom_food.minerals = Minerals(**payload.minerals.model_dump())
    else:
        custom_food.minerals = None

    db.add(custom_food)
    await db.commit()
    await db.refresh(custom_food)

    return custom_food


@router.put("/custom-foods/{food_id}")
async def edit_custom_food(
    food_id: uuid.UUID,
    payload: CustomFoodInput,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> FoodOutput:

    db_query = select(Food).where(Food.id == food_id).where(Food.user_id == user.id)

    result = await db.execute(db_query)
    existing_food = result.scalars().first()
    if not existing_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Custom food doesn't exist"
        )

    def apply(existing, data):
        for k, v in data.items():
            setattr(existing, k, v)

    apply(
        existing_food,
        payload.model_dump(exclude={"id", "user_id", "vitamins", "minerals", "fats"}),
    )

    if payload.vitamins:
        if existing_food.vitamins:
            apply(existing_food.vitamins, payload.vitamins.model_dump())
        else:
            existing_food.vitamins = Vitamins(**payload.vitamins.model_dump())

    if payload.fats:
        if existing_food.fats:
            apply(existing_food.fats, payload.fats.model_dump())
        else:
            existing_food.fats = Fats(**payload.fats.model_dump())

    if payload.minerals:
        if existing_food.minerals:
            apply(existing_food.minerals, payload.minerals.model_dump())
        else:
            existing_food.minerals = Minerals(**payload.minerals.model_dump())

    await db.commit()
    await db.refresh(existing_food)
    return existing_food
