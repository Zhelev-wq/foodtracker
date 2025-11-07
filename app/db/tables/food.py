from sqlalchemy import UUID, Column, Float, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid


class Food(Base):
    __tablename__ = "food"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    kcal = Column(Integer, nullable=False)
    alcohol = Column(Integer, nullable=True)
    caffeine = Column(Integer, nullable=True)
    barcode = Column(String, nullable=True)
    vitamins = relationship(
        "Vitamins", back_populates="food", cascade="all, delete-orphan"
    )
    minerals = relationship(
        "Minerals", back_populates="food", cascade="all, delete-orphan"
    )
    fats = relationship(
        "Fats", back_populates="food", cascade="all, delete-orphan"
    )
    

class Vitamins(Base):
    __tablename__ = "vitamins"
    id = Column(UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True, default=uuid.uuid4)
    food = relationship("Food", back_populates="vitamins")

    # all values based on 100g of food
    vit_a = Column(Float, nullable=True)
    vit_b1 = Column(Float, nullable=True)
    vit_b2 = Column(Float, nullable=True)
    vit_b3 = Column(Float, nullable=True)
    pantothenic_acid = Column(Float, nullable=True)
    vit_b6 = Column(Float, nullable=True)
    vit_b7 = Column(Float, nullable=True)
    biotin = Column(Float, nullable=True)
    vit_b9 = Column(Float, nullable=True)
    vit_b12 = Column(Float, nullable=True)
    vit_c = Column(Float, nullable=True)
    vit_d = Column(Float, nullable=True)
    vit_e = Column(Float, nullable=True)
    vit_k = Column(Float, nullable=True)


class Minerals(Base):
    __tablename__ = "minerals"
    id = Column(UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True, default=uuid.uuid4)
    food = relationship("Food", back_populates="minerals")

    # all values based on 100g of food
    calcium = Column(Float, nullable=True)
    magnesium = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    sodium = Column(Float, nullable=True)
    sulfur = Column(Float, nullable=True)
    iron = Column(Float, nullable=True)
    zinc = Column(Float, nullable=True)
    copper = Column(Float, nullable=True)
    manganese = Column(Float, nullable=True)
    molybdenum = Column(Float, nullable=True)
    selenium = Column(Float, nullable=True)
    iodine = Column(Float, nullable=True)
    fluoride = Column(Float, nullable=True)
    chromium = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    taurine = Column(Float, nullable=True)

class Fats(Base):
    __tablename__ = "fats"
    id = Column(UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True, default=uuid.uuid4)
    food = relationship("Food", back_populates="fats")

    saturated_fat = Column(Float, nullable=True)
    monounstaurated_fat = Column(Float, nullable=True)
    polyunsaturated_fat = Column(Float, nullable=True)
    omega_3_fat = Column(Float, nullable=True)
    omega_6_fat = Column(Float, nullable=True)
    omega_9_fat = Column(Float, nullable=True)
    trans_fat = Column(Float, nullable=True)
