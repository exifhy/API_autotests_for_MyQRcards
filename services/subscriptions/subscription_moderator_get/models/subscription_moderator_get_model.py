from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionModeratorGetModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    email: Optional[str] = None
