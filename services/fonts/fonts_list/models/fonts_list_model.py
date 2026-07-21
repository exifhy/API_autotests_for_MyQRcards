from typing import Optional

from src.models.base import StrictBaseModel


class FontItemModel(StrictBaseModel):
    id: Optional[int] = None
    displayName: Optional[str] = None
    fontFamily: Optional[str] = None
    url: Optional[str] = None


class FontsListModel(StrictBaseModel):
    items: list[FontItemModel]
