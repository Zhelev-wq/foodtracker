from pydantic import BaseModel
from typing import Optional


class Vitamins(BaseModel):
    vit_a: Optional[float] = None
    vit_b1: Optional[float] = None
    vit_b2: Optional[float] = None
    vit_b3: Optional[float] = None
    pantothenic_acid: Optional[float] = None #also known as B5
    vit_b6: Optional[float] = None
    vit_b7: Optional[float] = None
    biotin: Optional[float] = None #also known as B8
    vit_b9: Optional[float] = None
    vit_b12: Optional[float] = None
    vit_c: Optional[float] = None
    vit_d: Optional[float] = None
    vit_e: Optional[float] = None
    vit_k: Optional[float] = None
    

class Minerals(BaseModel):
    calcium: Optional[float] = None
    magnesium: Optional[float] = None
    phosphorus: Optional[float] = None
    sodium: Optional[float] = None
    sulfur: Optional[float] = None
    iron: Optional[float] = None
    zinc: Optional[float] = None
    copper: Optional[float] = None
    manganese: Optional[float] = None
    molybdenum: Optional[float] = None
    selenium: Optional[float] = None
    iodine: Optional[float] = None
    fluoride: Optional[float] = None
    chromium: Optional[float] = None
    potassium: Optional[float] = None
    taurine: Optional[float] = None

class Fats(BaseModel):
    saturated_fat: Optional[float] = None
    monounstaurated_fat: Optional[float] = None
    polyunsaturated_fat: Optional[float] = None
    omage_3_fat: Optional[float] = None
    omage_6_fat: Optional[float] = None
    omage_9_fat: Optional[float] = None
    trans_fat: Optional[float] = None   

class Food(BaseModel):
    name: str
    carbs: float
    protein: float
    fat: float
    kcal: float
    alcohol: Optional[float] = None
    caffeine: Optional[float] = None
    barcode: str
    vitamins: Optional[Vitamins]
    minerals: Optional[Minerals]
    fats: Optional[Fats]
    
