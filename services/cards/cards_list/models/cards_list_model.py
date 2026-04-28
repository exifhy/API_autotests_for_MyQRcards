from typing import Optional

from src.models.base import StrictBaseModel


class CardSubscriptionModel(StrictBaseModel):
    validTill: Optional[str] = None
    isTrial: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CardCompanyModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardPersonModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None


class CardListItemModel(StrictBaseModel):
    subscription: Optional[CardSubscriptionModel] = None
    company: Optional[CardCompanyModel] = None
    person: Optional[CardPersonModel] = None
    isAttributesSupported: Optional[bool] = None
    isPublic: Optional[bool] = None
    culture: Optional[str] = None
    isPrimary: Optional[bool] = None
    isHidden: Optional[bool] = None
    url: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CardsListModel(StrictBaseModel):
    items: list[CardListItemModel]
