from typing import Optional

from src.models.base import StrictBaseModel


class PromotionListItemModel(StrictBaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None


class PromotionsListModel(StrictBaseModel):
    items: list[PromotionListItemModel]

