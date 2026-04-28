from typing import Optional

from src.models.base import StrictBaseModel


class LocationCreateModel(StrictBaseModel):
    id: Optional[int] = None

