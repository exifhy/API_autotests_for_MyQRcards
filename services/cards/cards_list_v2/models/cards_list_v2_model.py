from typing import Optional

from src.models.base import StrictBaseModel


class CardV2SubscriptionTypeModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardV2SubscriptionModel(StrictBaseModel):
    subscriptionType: Optional[CardV2SubscriptionTypeModel] = None
    validTill: Optional[str] = None
    isTrial: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None
    isValid: Optional[bool] = None


class CardV2CompanyModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class CardV2PersonModel(StrictBaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    email: Optional[str] = None
    siteUrl: Optional[str] = None
    mobilePhone: Optional[str] = None


class CardV2EmploymentModel(StrictBaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    activity: Optional[str] = None
    company: Optional[dict] = None


class CardV2ListItemModel(StrictBaseModel):
    subscription: Optional[CardV2SubscriptionModel] = None
    company: Optional[CardV2CompanyModel] = None
    person: Optional[CardV2PersonModel] = None
    employment: Optional[CardV2EmploymentModel] = None
    color: Optional[str] = None
    qrColor: Optional[str] = None
    gallery: list[dict] = []
    personSocialNetworks: list[dict] = []
    isAttributesSupported: Optional[bool] = None
    isPublic: Optional[bool] = None
    culture: Optional[str] = None
    isPrimary: Optional[bool] = None
    isHidden: Optional[bool] = None
    url: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CardsListV2Model(StrictBaseModel):
    items: list[CardV2ListItemModel]
