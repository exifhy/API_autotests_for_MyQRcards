from typing import Optional

from src.models.base import StrictBaseModel


class CultureItemModel(StrictBaseModel):
    id: Optional[int] = None
    language: Optional[str] = None
    code: Optional[str] = None


class CulturesListModel(StrictBaseModel):
    items: list[CultureItemModel]

