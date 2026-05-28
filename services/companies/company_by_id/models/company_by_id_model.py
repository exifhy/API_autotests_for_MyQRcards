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


class CompanySocialNetworkModel(StrictBaseModel):
    contactUrl: Optional[str] = None
    nameEn: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompanyByIdModel(StrictBaseModel):
    customers: Optional[str] = None
    location: Optional[CompanyLocationModel] = None
    socialNetworks: list[CompanySocialNetworkModel] = []
    isReadOnly: Optional[bool] = None
    logo: Optional[CompanyLogoModel] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    siteUrl: Optional[str] = None
    foundedYear: Optional[int] = None
    activity: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None

