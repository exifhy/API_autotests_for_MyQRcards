from typing import Optional

from src.models.base import StrictBaseModel


class CardShortPersonModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None


class CardShortCompanyModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardShortGalleryItemModel(StrictBaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    sortOrder: Optional[int] = None


class CardByIdShortModel(StrictBaseModel):
    accountID: Optional[int] = None
    id: Optional[int] = None
    selfInfo: Optional[str] = None
    position: Optional[str] = None
    person: Optional[CardShortPersonModel] = None
    gallery: list[CardShortGalleryItemModel] = []
    company: Optional[CardShortCompanyModel] = None
    cardLinkUrl: Optional[str] = None
    customizedUrl: Optional[str] = None
    isSubscriptionValid: Optional[bool] = None
    isIndexable: Optional[bool] = None
