import uuid

from .base_food import FoodBase


class FoodOutput(FoodBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID | None = None
    barcode: str
