import uuid

from sqlalchemy import UUID, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Food(Base):
    __tablename__ = "food"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String)
    carbs: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)
    kcal: Mapped[int] = mapped_column(Integer)
    alcohol: Mapped[int | None] = mapped_column(Integer)
    caffeine: Mapped[int | None] = mapped_column(Integer)
    barcode: Mapped[str | None] = mapped_column(String)
    vitamins = relationship(
        "Vitamins", back_populates="food", cascade="all, delete-orphan", uselist=False
    )
    minerals = relationship(
        "Minerals", back_populates="food", cascade="all, delete-orphan", uselist=False
    )
    fats = relationship(
        "Fats", back_populates="food", cascade="all, delete-orphan", uselist=False
    )


class Vitamins(Base):
    __tablename__ = "vitamins"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="vitamins")

    # all values based on 100g of food
    vit_a: Mapped[float | None] = mapped_column(Float)
    vit_b1: Mapped[float | None] = mapped_column(Float)
    vit_b2: Mapped[float | None] = mapped_column(Float)
    vit_b3: Mapped[float | None] = mapped_column(Float)
    pantothenic_acid: Mapped[float | None] = mapped_column(Float)
    vit_b6: Mapped[float | None] = mapped_column(Float)
    vit_b7: Mapped[float | None] = mapped_column(Float)
    biotin: Mapped[float | None] = mapped_column(Float)
    vit_b9: Mapped[float | None] = mapped_column(Float)
    vit_b12: Mapped[float | None] = mapped_column(Float)
    vit_c: Mapped[float | None] = mapped_column(Float)
    vit_d: Mapped[float | None] = mapped_column(Float)
    vit_e: Mapped[float | None] = mapped_column(Float)
    vit_k: Mapped[float | None] = mapped_column(Float)


class Minerals(Base):
    __tablename__ = "minerals"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="minerals")

    # all values based on 100g of food
    calcium: Mapped[float | None] = mapped_column(Float)
    magnesium: Mapped[float | None] = mapped_column(Float)
    phosphorus: Mapped[float | None] = mapped_column(Float)
    sodium: Mapped[float | None] = mapped_column(Float)
    sulfur: Mapped[float | None] = mapped_column(Float)
    iron: Mapped[float | None] = mapped_column(Float)
    zinc: Mapped[float | None] = mapped_column(Float)
    copper: Mapped[float | None] = mapped_column(Float)
    manganese: Mapped[float | None] = mapped_column(Float)
    molybdenum: Mapped[float | None] = mapped_column(Float)
    selenium: Mapped[float | None] = mapped_column(Float)
    iodine: Mapped[float | None] = mapped_column(Float)
    fluoride: Mapped[float | None] = mapped_column(Float)
    chromium: Mapped[float | None] = mapped_column(Float)
    potassium: Mapped[float | None] = mapped_column(Float)
    taurine: Mapped[float | None] = mapped_column(Float)


class Fats(Base):
    __tablename__ = "fats"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="fats")

    saturated_fat: Mapped[float | None] = mapped_column(Float)
    monounsaturated_fat: Mapped[float | None] = mapped_column(Float)
    polyunsaturated_fat: Mapped[float | None] = mapped_column(Float)
    omega_3_fat: Mapped[float | None] = mapped_column(Float)
    omega_6_fat: Mapped[float | None] = mapped_column(Float)
    omega_9_fat: Mapped[float | None] = mapped_column(Float)
    trans_fat: Mapped[float | None] = mapped_column(Float)
