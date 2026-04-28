from typing import Optional

from src.models.base import StrictBaseModel


class CardDeleteByIdModel(StrictBaseModel):
    status_code: Optional[int] = None
