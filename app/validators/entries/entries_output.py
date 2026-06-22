import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, model_validator

from app.validators.food.food_output import FoodOutput


class FoodEntryItemOutput(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    food_id: uuid.UUID
    food_grams: int
    food: FoodOutput
    user_id: uuid.UUID
    food_entry_id: uuid.UUID


class FoodEntryOutput(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID
    time: datetime.datetime
    name: Optional[str] = None
    food_items: List[FoodEntryItemOutput]

    kcal: float = 0
    protein: float = 0
    fat: float = 0
    carbs: float = 0
    alcohol: float = 0
    caffeine: float = 0
    food_grams: float = 0

    @model_validator(mode="after")
    def compute_totals(self):

        for item in self.food_items:
            self.kcal += item.food.kcal * item.food_grams / 100
            self.protein += item.food.protein * item.food_grams / 100
            self.fat += item.food.fat * item.food_grams / 100
            self.carbs += item.food.carbs * item.food_grams / 100
            self.alcohol += (item.food.alcohol or 0) * item.food_grams / 100
            self.caffeine += (item.food.caffeine or 0) * item.food_grams / 100
            self.food_grams += item.food_grams

        if not self.name and self.food_items:
            self.name = self.food_items[0].food.name
        return self


class RecipeItemOutput(FoodEntryItemOutput):
    pass


class RecipeOutput(FoodEntryOutput):
    name: str
    food_items: List[RecipeItemOutput]
