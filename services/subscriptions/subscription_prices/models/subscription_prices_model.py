from typing import Optional

from src.models.base import StrictBaseModel


class SubscriptionTypeModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class SubscriptionPricesItemModel(StrictBaseModel):
    subscriptionType: Optional[SubscriptionTypeModel] = None
    currencyCode: Optional[str] = None
    price: Optional[float] = None
    discountedPrice: Optional[float] = None
    discountPercent: Optional[float] = None


class SubscriptionPricesModel(StrictBaseModel):
    items: list[SubscriptionPricesItemModel]
