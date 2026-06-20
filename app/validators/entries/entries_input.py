import uuid
from typing import List

from pydantic import BaseModel


class EntryItemInput(BaseModel):
    food_uuid: uuid.UUID
    grams: int


class RecipeInput(BaseModel):
    recipe_name: str
    food_items: List[EntryItemInput]


class FoodEntryItemEdit(BaseModel):
    grams: int


class RecipeEdit(BaseModel):
    food_items: List[ExistingRecipeItemInput | EntryItemInput]
    recipe_name: str


class ExistingEntryItemInput(BaseModel):
    # used opposite EntryItemInput to distinguish exisitng items vs incoming items
    id: uuid.UUID
    food_grams: int


class ExistingRecipeItemInput(ExistingEntryItemInput):
    pass
