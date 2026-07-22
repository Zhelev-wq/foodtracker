import datetime
import uuid

from sqlalchemy import (UUID, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from app.db.database import Base

"""
TODO: 
    rename classes and attributes to something that makes sense
    current setup is confusing af
        food_entry is attr and table name
    
"""


class EntryBase(Base):
    __abstract__ = True
    owned_item_class_name = ""
    time: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )

    @declared_attr
    def food_items(cls):
        return relationship(
            cls.owned_item_class_name,
            back_populates="food_entry",
            cascade="all, delete-orphan",
            lazy="selectin",
            order_by=cls.owned_item_class_name + ".id"
        )  # this will pull all FoodEntryItems where FoodEntryItem.food_id == FoodEntry.id


class FoodEntry(EntryBase):
    __tablename__ = "food_entry"
    owned_item_class_name = "FoodEntryItem"
    name: Mapped[str] = mapped_column(String, nullable=True)


class Recipe(EntryBase):
    __tablename__ = "recipe"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_recipe_user_name"),)
    owned_item_class_name = "RecipeEntryItem"
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class ItemBase(Base):
    __abstract__ = True

    owner_table = ""
    owner_table_class_name = ""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    food_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("food.id"),
    )
    food_grams: Mapped[int] = mapped_column(Integer)

    @declared_attr
    def user_id(cls):
        return association_proxy("food_entry", "user_id")

    @declared_attr
    def food(cls):
        return relationship("Food", lazy="selectin")

    @declared_attr
    def food_entry_id(cls):
        return mapped_column(UUID(as_uuid=True), ForeignKey(f"{cls.owner_table}.id"))

    @declared_attr
    def food_entry(cls):
        return relationship(
            cls.owner_table_class_name, back_populates="food_items", lazy="selectin"
        )


class FoodEntryItem(ItemBase):
    __tablename__ = "food_entry_item"

    owner_table = "food_entry"
    owner_table_class_name = "FoodEntry"


class RecipeEntryItem(ItemBase):
    __tablename__ = "recipe_item"

    owner_table = "recipe"
    owner_table_class_name = "Recipe"
