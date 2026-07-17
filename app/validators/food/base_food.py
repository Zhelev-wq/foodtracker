from typing import Optional

from pydantic import BaseModel


class Vitamins(BaseModel):
    vit_a: Optional[float] = 0
    vit_b1: Optional[float] = 0
    vit_b2: Optional[float] = 0
    vit_b3: Optional[float] = 0
    pantothenic_acid: Optional[float] = 0  # also known as B5
    vit_b6: Optional[float] = 0
    vit_b7: Optional[float] = 0
    biotin: Optional[float] = 0  # also known as B8
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
    monounsaturated_fat: Optional[float] = 0
    polyunsaturated_fat: Optional[float] = 0
    omega_3_fat: Optional[float] = 0
    omega_6_fat: Optional[float] = 0
    omega_9_fat: Optional[float] = 0
    trans_fat: Optional[float] = 0


class FoodBase(BaseModel):
    name: str
    carbs: float
    protein: float
    fat: float
    kcal: float
    barcode: Optional[str]

    alcohol: Optional[float] = 0
    caffeine: Optional[float] = 0
    vitamins: Optional[Vitamins]
    minerals: Optional[Minerals]
    fats: Optional[Fats]
