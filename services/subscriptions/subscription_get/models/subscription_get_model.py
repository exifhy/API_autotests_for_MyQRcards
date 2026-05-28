from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionGetModel(StrictBaseModel):
    id: Optional[int] = None
    accountID: Optional[int] = None
    name: Optional[str] = None
