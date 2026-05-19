import uuid

from sqlalchemy import UUID, Float, ForeignKey, Integer, String, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Food(Base):
    __tablename__ = "food"

    __table_args__ = (
        Index(
            "idx_food_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name":"gin_trgm_ops"}
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String)
    carbs: Mapped[float] = mapped_column(Numeric(10,2))
    protein: Mapped[float] = mapped_column(Numeric(10,2))
    fat: Mapped[float] = mapped_column(Numeric(10,2))
    kcal: Mapped[int] = mapped_column(Integer)
    alcohol: Mapped[int | None] = mapped_column(Integer)
    caffeine: Mapped[int | None] = mapped_column(Integer)
    barcode: Mapped[str | None] = mapped_column(String)
    vitamins = relationship(
        "Vitamins",
        back_populates="food",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
    minerals = relationship(
        "Minerals",
        back_populates="food",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
    fats = relationship(
        "Fats",
        back_populates="food",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )


class Vitamins(Base):
    __tablename__ = "vitamins"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="vitamins")

    # all values based on 100g of food
    vit_a: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b1: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b2: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b3: Mapped[float | None] = mapped_column(Numeric(10,2))
    pantothenic_acid: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b6: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b7: Mapped[float | None] = mapped_column(Numeric(10,2))
    biotin: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b9: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_b12: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_c: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_d: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_e: Mapped[float | None] = mapped_column(Numeric(10,2))
    vit_k: Mapped[float | None] = mapped_column(Numeric(10,2))


class Minerals(Base):
    __tablename__ = "minerals"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="minerals")

    # all values based on 100g of food
    calcium: Mapped[float | None] = mapped_column(Numeric(10,2))
    magnesium: Mapped[float | None] = mapped_column(Numeric(10,2))
    phosphorus: Mapped[float | None] = mapped_column(Numeric(10,2))
    sodium: Mapped[float | None] = mapped_column(Numeric(10,2))
    sulfur: Mapped[float | None] = mapped_column(Numeric(10,2))
    iron: Mapped[float | None] = mapped_column(Numeric(10,2))
    zinc: Mapped[float | None] = mapped_column(Numeric(10,2))
    copper: Mapped[float | None] = mapped_column(Numeric(10,2))
    manganese: Mapped[float | None] = mapped_column(Numeric(10,2))
    molybdenum: Mapped[float | None] = mapped_column(Numeric(10,2))
    selenium: Mapped[float | None] = mapped_column(Numeric(10,2))
    iodine: Mapped[float | None] = mapped_column(Numeric(10,2))
    fluoride: Mapped[float | None] = mapped_column(Numeric(10,2))
    chromium: Mapped[float | None] = mapped_column(Numeric(10,2))
    potassium: Mapped[float | None] = mapped_column(Numeric(10,2))
    taurine: Mapped[float | None] = mapped_column(Numeric(10,2))


class Fats(Base):
    __tablename__ = "fats"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("food.id"), primary_key=True
    )
    food = relationship("Food", back_populates="fats")

    saturated_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
    monounsaturated_fat: Mapped[float | None] = mapped_column(
        Float, name="monounstaurated_fat"
    )
    polyunsaturated_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
    omega_3_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
    omega_6_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
    omega_9_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
    trans_fat: Mapped[float | None] = mapped_column(Numeric(10,2))
