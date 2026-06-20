import uuid

from .base_food import FoodBase


class CustomFoodInput(FoodBase):
    # TODO: create validators for kcal and macro values
    pass


class CustomFoodEdit(FoodBase):
    user_id: uuid.UUID
    id: uuid.UUID
