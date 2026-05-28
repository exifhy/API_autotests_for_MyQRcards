from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionModeratorItemModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    email: Optional[str] = None


class SubscriptionModeratorsListModel(StrictBaseModel):
    items: list[SubscriptionModeratorItemModel] = []
