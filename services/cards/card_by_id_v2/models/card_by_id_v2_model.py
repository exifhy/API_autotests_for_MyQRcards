from typing import Optional

from src.models.base import StrictBaseModel


class CardByIdV2PersonModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    mobilePhone: Optional[str] = None
    homePhone: Optional[str] = None
    email: Optional[str] = None
    siteUrl: Optional[str] = None
    education: Optional[str] = None
    selfInfo: Optional[str] = None
    birthDate: Optional[str] = None
    fileName: Optional[str] = None
    location: Optional[dict] = None
    socialNetworks: list[dict] = []


class CardByIdV2CardThemeModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardByIdV2SubscriptionModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None
    subscriptionType: Optional[dict] = None
    isValid: Optional[bool] = None


class CardByIdV2EmploymentModel(StrictBaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    activity: Optional[str] = None
    company: Optional[dict] = None


class CardByIdV2Model(StrictBaseModel):
    accountID: Optional[int] = None
    accountUrl: Optional[str] = None
    customizedUrl: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    person: Optional[CardByIdV2PersonModel] = None
    cardTheme: Optional[CardByIdV2CardThemeModel] = None
    subscription: Optional[CardByIdV2SubscriptionModel] = None
    cardLinkType: Optional[dict] = None
    employment: Optional[CardByIdV2EmploymentModel] = None
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
