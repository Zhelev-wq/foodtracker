from sqlalchemy import UUID, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Food(Base):
    __tablename__ = "food"
    id = Column(UUID, primary_key=True)
    name = Column(String)
    carbs = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    vitamins = relationship(
        "Vitamins", back_populates="food", cascade="all, delete-oprhan"
    )
    minerals = relationship(
        "Minerals", back_populates="food", cascade="all, delete-oprhan"
    )


class Vitamins(Base):
    __tablename__ = "vitamins"
    id = Column(UUID, ForeignKey("food.id"), primary_key=True)

    # all values based on 100g of food
    vit_a = Column(Float, nullable=True)
    vit_b1 = Column(Float, nullable=True)
    vit_b2 = Column(Float, nullable=True)
    vit_b3 = Column(Float, nullable=True)
    vit_b5 = Column(Float, nullable=True)
    vit_b6 = Column(Float, nullable=True)
    vit_b7 = Column(Float, nullable=True)
    vit_b9 = Column(Float, nullable=True)
    vit_b12 = Column(Float, nullable=True)
    vit_c = Column(Float, nullable=True)
    vit_d = Column(Float, nullable=True)
    vit_e = Column(Float, nullable=True)
    vit_k = Column(Float, nullable=True)


class Minerals(Base):
    __tablename__ = "minerals"
    id = Column(UUID, ForeignKey("food.id"), primary_key=True)

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
    Iodine = Column(Float, nullable=True)
    fluoride = Column(Float, nullable=True)
