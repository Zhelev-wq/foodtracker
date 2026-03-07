import datetime
import uuid

from sqlalchemy import UUID, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class FoodEntry(Base):
    __tablename__ = "food_entry"

    time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, as_uuid=True, default=uuid.uuid4
    )

    food_items: Mapped[list[FoodEntryItem]] = relationship(
        "FoodEntryItem",
        back_populates="food_entry",
        cascade="all, delete-orphan",
        lazy="selectin",
    )  # this will pull all FoodEntryItems where FoodEntryItem.food_id == FoodEntry.id


class FoodEntryItem(Base):
    __tablename__ = "food_entry_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, as_uuid=True, default=uuid.uuid4
    )
    food = relationship("Food", lazy="selectin")
    food_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("food.id"), as_uuid=True
    )
    food_grams: Mapped[float] = mapped_column(Integer)

    food_entry_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("food_entry.id"), as_uuid=True
    )
    food_entry = relationship("FoodEntry", back_populates="food_items")
