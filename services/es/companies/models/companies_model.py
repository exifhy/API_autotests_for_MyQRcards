from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict


class SuccessAddCompaniesModel(BaseModel):
    companies: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TimeZoneResult(BaseModel):
    utcOffsetMinutes: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CountryResult(BaseModel):
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationResult(BaseModel):
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    id: Optional[int] = None


class IdNameDeletedResult(BaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CountersResult(BaseModel):
    assets: Optional[int] = None
    users: Optional[int] = None


class SuccessCompaniesGetResult(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    siteUrl: Optional[str] = None
    fullName: Optional[str] = None
    registeredOffice: Optional[str] = None
    registeredOfficeNote: Optional[str] = None
    psrn: Optional[str] = None
    okpo: Optional[str] = None
    certificateNumber: Optional[str] = None
    certificateDate: Optional[datetime] = None
    vatRate: Optional[int] = None
    location: Optional[LocationResult] = None
    erpID: Optional[str] = None
    code: Optional[str] = None
    registrationTypeID: Optional[int] = None
    registrationTypeShortNameRu: Optional[str] = None
    registrationTypeNameRu: Optional[str] = None
    tin: Optional[str] = None
    iec: Optional[str] = None
    isEmployer: Optional[bool] = None
    isContractorHolder: Optional[bool] = None
    isOurCompany: Optional[bool] = None
    isVATTaxpayer: Optional[bool] = None
    customerOrgUnit: Optional[IdNameDeletedResult] = None
    staffOrgUnit: Optional[IdNameDeletedResult] = None
    counters: Optional[CountersResult] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None
