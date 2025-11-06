from app.db.database import Base
from sqlalchemy import Column, ForeignKey, UUID, Integer, DateTime
from sqlalchemy.orm import relationship


class FoodEntry(Base):
    __tablename__ = "food_entry"

    time = Column(DateTime)
    id = Column(UUID, primary_key=True)

    food_items = relationship(
        "FoodEntryItem", back_populates="food_entry", cascade="all, delete-orphan"
    )  # this will pull all FoodEntryItems where FoodEntryItem.food_id == FoodEntry.id


class FoodEntryItem(Base):
    __tablename__ = "food_entry_item"

    food = relationship("Food")
    food_id = Column(UUID, ForeignKey("food.id"))
    food_grams = Column(Integer, nullable=False)

    food_entry_id = Column(UUID, ForeignKey("food_entry.id"))
    food_entry = relationship("FoodEntry")
