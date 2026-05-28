from typing import Optional

from src.models.base import StrictBaseModel


class CardLastUpdateItemModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    lastModified: Optional[str] = None


class CardsLastUpdateModel(StrictBaseModel):
    items: list[CardLastUpdateItemModel]
