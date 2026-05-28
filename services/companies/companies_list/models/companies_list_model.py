from typing import Optional

from src.models.base import StrictBaseModel


class CompanyLocationModel(StrictBaseModel):
    id: Optional[int] = None
    country: Optional[str] = None
    postalCode: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CompanyLogoModel(StrictBaseModel):
    id: Optional[int] = None
    url: Optional[str] = None


class CompanyListItemModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    siteUrl: Optional[str] = None
    foundedYear: Optional[int] = None
    activity: Optional[str] = None
    isCorporate: Optional[bool] = None
    isReadOnly: Optional[bool] = None
    location: Optional[CompanyLocationModel] = None
    logo: Optional[CompanyLogoModel] = None


class CompaniesListModel(StrictBaseModel):
    items: list[CompanyListItemModel]

