import uuid
from typing import List

from pydantic import BaseModel, Field


class EntryItemInput(BaseModel):
    food_uuid: uuid.UUID
    grams: int


class RecipeInput(BaseModel):
    name: str = Field(min_length=4)
    food_items: List[EntryItemInput]


class FoodEntryItemEdit(BaseModel):
    grams: int


class ExistingEntryItemInput(BaseModel):
    # used opposite EntryItemInput to distinguish exisitng items vs incoming items
    id: uuid.UUID
    food_grams: int


class ExistingRecipeItemInput(ExistingEntryItemInput):
    pass


class RecipeEdit(BaseModel):
    food_items: List[ExistingRecipeItemInput | EntryItemInput]
    name: str = Field(min_length=4)
