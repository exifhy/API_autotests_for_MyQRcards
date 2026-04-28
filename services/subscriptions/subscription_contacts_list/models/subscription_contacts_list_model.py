from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionContactItemModel(StrictBaseModel):
    accountID: Optional[int] = None
    cardID: Optional[int] = None
    contactID: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    mobilePhone: Optional[str] = None
    position: Optional[str] = None
    created: Optional[str] = None


class SubscriptionContactsListModel(StrictBaseModel):
    items: list[SubscriptionContactItemModel] = []
