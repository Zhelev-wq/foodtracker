from pydantic import BaseModel, computed_field
from functools import cached_property
from typing import Optional, List
import datetime
import uuid

class Vitamins(BaseModel):
    vit_a: Optional[float] = 0
    vit_b1: Optional[float] = 0
    vit_b2: Optional[float] = 0
    vit_b3: Optional[float] = 0
    pantothenic_acid: Optional[float] = 0 #also known as B5
    vit_b6: Optional[float] = 0
    vit_b7: Optional[float] = 0
    biotin: Optional[float] = 0 #also known as B8
    vit_b9: Optional[float] = 0
    vit_b12: Optional[float] = 0
    vit_c: Optional[float] = 0
    vit_d: Optional[float] = 0
    vit_e: Optional[float] = 0
    vit_k: Optional[float] = 0
    

class Minerals(BaseModel):
    calcium: Optional[float] = 0
    magnesium: Optional[float] = 0
    phosphorus: Optional[float] = 0
    sodium: Optional[float] = 0
    sulfur: Optional[float] = 0
    iron: Optional[float] = 0
    zinc: Optional[float] = 0
    copper: Optional[float] = 0
    manganese: Optional[float] = 0
    molybdenum: Optional[float] = 0
    selenium: Optional[float] = 0
    iodine: Optional[float] = 0
    fluoride: Optional[float] = 0
    chromium: Optional[float] = 0
    potassium: Optional[float] = 0
    taurine: Optional[float] = 0

class Fats(BaseModel):
    saturated_fat: Optional[float] = 0
    monounstaurated_fat: Optional[float] = 0
    polyunsaturated_fat: Optional[float] = 0
    omage_3_fat: Optional[float] = 0
    omage_6_fat: Optional[float] = 0
    omage_9_fat: Optional[float] = 0
    trans_fat: Optional[float] = 0   

class FoodOut(BaseModel):

    model_config = {"from_attributes": True}

    name: str
    carbs: float
    protein: float
    fat: float
    kcal: float
    alcohol: Optional[float] = 0
    caffeine: Optional[float] = 0
    barcode: str
    vitamins: Optional[Vitamins]
    minerals: Optional[Minerals]
    fats: Optional[Fats]

class FoodEntryItemOut(BaseModel):

    model_config = {"from_attributes": True}
    id: uuid.UUID
    food_id: uuid.UUID
    food_grams: int
    food: FoodOut
    
class FoodEntryOut(BaseModel):
    id: uuid.UUID
    time: datetime.datetime
    food_items: list[FoodEntryItemOut]
    model_config = {"from_attributes": True}

    @cached_property
    def _total(self):
        total = {
            "kcal": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0,
            "alcohol": 0,
            "caffeine": 0,
            "food_grams": 0,
            "name": None
        }

        for item in self.food_items:
            total["kcal"] += item.food.kcal * item.food_grams / 100
            total["protein"] += item.food.protein * item.food_grams / 100
            total["fat"] += item.food.fat * item.food_grams / 100
            total["carbs"] += item.food.carbs * item.food_grams / 100
            total["alcohol"] += (item.food.alcohol or 0) * item.food_grams / 100
            total["caffeine"] += (item.food.caffeine or 0) * item.food_grams / 100
            total["food_grams"] += item.food_grams
            
        total["name"] = self.food_items[0].food.name
        return total

    @computed_field
    @property
    def name(self) -> str:
        return self._total.get("name")

    @computed_field
    @property
    def protein(self) -> float:
        return self._total.get("protein")
    
    @computed_field
    @property
    def carbs(self) -> float:
        return self._total.get("carbs")
    
    @computed_field
    @property
    def fat(self) -> float:
        return self._total.get("fat")        
    
    @computed_field
    @property
    def kcal(self) -> float:
        return self._total.get("kcal")

    @computed_field
    @property
    def alcohol(self) -> float:
        return self._total.get("alcohol")
    
    @computed_field
    @property
    def caffeine(self) -> float:
        return self._total.get("caffeine")
    
    @computed_field
    @property
    def food_grams(self) -> float:
        return self._total.get("food_grams")