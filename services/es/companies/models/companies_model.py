from datetime import datetime
from pydantic import BaseModel, RootModel
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


class CompaniesListResult(BaseModel):
    sortOrder: Optional[int] = None
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
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetCompaniesListResultModel(RootModel):
    root: Optional[Dict[str, CompaniesListResult]] = None


class ListAttachmentResultModel(BaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class SuccessGetListAttachmentResultModel(RootModel):
    root: Dict[str, ListAttachmentResultModel]


class SuccessGetAttachmentResultModel(BaseModel):
    attachmentID: Optional[int] = None
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class AttributeTypeResult(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class MeasurementUnitResult(BaseModel):
    abbreviation: Optional[str] = None
    designation: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class DomainResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class CompanyAttributeResultModel(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    values: Optional[List[str]] = None
    isPublic: Optional[bool] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListCompanyAttributeResultModel(BaseModel):
    result: List[CompanyAttributeResultModel]


class BankResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    bic: Optional[str] = None
    correspondingAccount: Optional[str] = None


class CurrencyResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class CompanyBankAccountListResultModel(BaseModel):
    companyID: Optional[int] = None
    bank: Optional[BankResult] = None
    companyBankAccountID: Optional[int] = None
    checkingAccount: Optional[str] = None
    companyName: Optional[str] = None
    currency: Optional[CurrencyResult] = None
    isDefault: Optional[bool] = None


class SuccessGetCompanyBankAccountListResultModel(RootModel):
    root: Dict[str, CompanyBankAccountListResultModel]


class AddBakAccountsToCompanyModel(BaseModel):
    companyID: int
    bankID: int
    companyBankAccountID: int


class SuccessAddBakAccountsToCompanyModel(BaseModel):
    result: List[AddBakAccountsToCompanyModel]


class CompanyContactsResultModel(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    deleted: Optional[datetime] = None
    description: Optional[str] = None
    archived: Optional[datetime] = None
    companyID: Optional[int] = None
    contactID: Optional[int] = None


class SuccessGetListCompanyContactsResultModel(RootModel):
    root: Dict[str, CompanyContactsResultModel]


class SuccessAddContactToCompanyModel(BaseModel):
    companyID: int
    contactID: int


class SuccessAddListContactsToCompanyModel(BaseModel):
    result: List[SuccessAddContactToCompanyModel]


class SuccessGetCompanyDataModel(BaseModel):
    name: str
    erpID: Optional[str] = None
    code: Optional[str] = None
    registrationTypeID: int
    email: Optional[str] = None
    phone: Optional[str] = None
    siteUrl: Optional[str] = None
    fullName: Optional[str] = None
    registeredOffice: Optional[str] = None
    registeredOfficeNote: Optional[str] = None
    tin: Optional[str] = None
    iec: Optional[str] = None
    psrn: Optional[str] = None
    okpo: Optional[str] = None
    certificateNumber: Optional[str] = None
    certificateDate: Optional[str] = None
    isEmployer: Optional[bool] = None
    isContractorHolder: Optional[bool] = None
    isOurCompany: Optional[bool] = None
    isVATTaxpayer: Optional[bool] = None
    vatRate: Optional[int] = None
    locationID: Optional[int] = None

