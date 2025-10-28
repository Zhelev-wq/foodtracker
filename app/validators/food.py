from pydantic import BaseModel
from typing import Optional


class Vitamins(BaseModel):
    vit_a: Optional[float]
    vit_b1: Optional[float]
    vit_b2: Optional[float]
    vit_b3: Optional[float]
    vit_b5: Optional[float]
    vit_b6: Optional[float]
    vit_b7: Optional[float]
    vit_b9: Optional[float]
    vit_b12: Optional[float]
    vit_c: Optional[float]
    vit_d: Optional[float]
    vit_e: Optional[float]
    vit_k: Optional[float]


class Minerals(BaseModel):
    calcium: Optional[float]
    magnesium: Optional[float]
    phosphorus: Optional[float]
    sodium: Optional[float]
    sulfur: Optional[float]
    iron: Optional[float]
    zinc: Optional[float]
    copper: Optional[float]
    manganese: Optional[float]
    molybdenum: Optional[float]
    selenium: Optional[float]
    Iodine: Optional[float]
    fluoride: Optional[float]


class Food(BaseModel):
    name: str
    carbs: float
    protein: float
    fat: float
    vitamins: Optional[Vitamins]
    minerals: Optional[Minerals]
