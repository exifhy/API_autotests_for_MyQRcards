from typing import Optional

from src.models.base import StrictBaseModel


class CardCustomLinkItemModel(StrictBaseModel):
    customCardLinkUrl: Optional[str] = None
    isAttributesSupported: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CardsCustomLinkModel(StrictBaseModel):
    items: list[CardCustomLinkItemModel]
