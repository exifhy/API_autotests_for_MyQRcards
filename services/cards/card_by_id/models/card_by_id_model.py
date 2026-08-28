from typing import Optional

from src.models.base import StrictBaseModel


class CardByIdPersonModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    selfInfo: Optional[str] = None
    email: Optional[str] = None
    fileName: Optional[str] = None


class CardByIdCardThemeModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardByIdSubscriptionModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    subscriptionType: Optional[dict] = None
    isValid: Optional[bool] = None


class CardByIdEmploymentModel(StrictBaseModel):
    position: Optional[str] = None
    activity: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[dict] = None


class CardByIdModel(StrictBaseModel):
    accountID: Optional[int] = None
    accountUrl: Optional[str] = None
    customizedUrl: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    person: Optional[CardByIdPersonModel] = None
    cardTheme: Optional[CardByIdCardThemeModel] = None
    subscription: Optional[CardByIdSubscriptionModel] = None
    cardLinkType: Optional[dict] = None
    employment: Optional[CardByIdEmploymentModel] = None
    gallery: list[dict] = []
    customCardLink: Optional[dict] = None
    defaultCardLinkUrlID: Optional[int] = None
    featureCodes: list[str] = []
    isPublic: Optional[bool] = None
    culture: Optional[str] = None
    isPrimary: Optional[bool] = None
    isHidden: Optional[bool] = None
    url: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None
    subscriptionStatus: Optional[str] = None
    isIndexable: Optional[bool] = None
