from typing import Optional

from src.models.base import StrictBaseModel


class CardCreateModel(StrictBaseModel):
    id: Optional[int] = None
