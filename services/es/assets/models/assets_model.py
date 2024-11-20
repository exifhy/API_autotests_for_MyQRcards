from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel
from datetime import datetime


class AssetTaskActualityResult(BaseModel):
    self: int
    nested: int


class IdNameDeletedResult(BaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdResult(BaseModel):
    id: Optional[int] = None


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


class AssetResultWithLocation(BaseModel):
    location: Optional[IdResult] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class AssetExtResult(BaseModel):
    hasChildren: bool
    tasksActualities: Optional[Dict[str, AssetTaskActualityResult]] = None
    hostAsset: Optional[IdNameDeletedResult] = None
    host: Optional[AssetResultWithLocation] = None
    location: Optional[LocationResult] = None
    isHostLocation: bool
    published: Optional[datetime] = None
    company: Optional[IdNameDeletedResult] = None
    warrantyTill: Optional[datetime] = None
    path: Optional[List[IdNameDeletedResult]] = None
    sortOrder: int
    erpID: Optional[str] = None
    serialNumber: Optional[str] = None
    useAllWorkTypes: bool
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    name: str
    id: int


class AssetExtResults(BaseModel):
    """Main model AssetList"""
    results: Dict[str, AssetExtResult]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class IdNameResultModel(BaseModel):
    name: str
    id: int


class AssetTypeResult(BaseModel):
    isHostable: bool
    name: str
    id: int


class IdNameResult(BaseModel):
    name: str
    id: int


class ParentAssetResult(BaseModel):
    assetType: AssetTypeResult
    deleted: Optional[datetime] = None
    name: str
    id: int


class AssetResponsiblePersonResult(BaseModel):
    userID: int
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    email: Optional[str] = None
    isEmailVerified: bool
    isMobilePhoneVerified: bool


class AssetPosition(BaseModel):
    schemaID: int
    x: int
    y: int


class AssetResultWithLocationDetailedInfo(BaseModel):
    location: IdNameResult
    deleted: Optional[datetime] = None
    name: str
    id: int


class AssetDetailedInfoResult(BaseModel):
    """Main asset detailed model"""
    isMobileAsset: bool
    assetType: AssetTypeResult
    assetClass: IdNameResult
    scheduleRule: Optional[IdNameResult] = None
    parent: Optional[ParentAssetResult] = None
    notes: Optional[str] = None
    publishedBy: Optional[int] = None
    responsiblePerson: Optional[AssetResponsiblePersonResult] = None
    avatarUrl: Optional[str] = None
    positionOnSchema: Optional[AssetPosition] = None
    hostAsset: Optional[IdNameDeletedResult] = None
    host: Optional[AssetResultWithLocation] = None
    location: Optional[LocationResult] = None
    isHostLocation: Optional[bool] = None
    published: Optional[datetime] = None
    company: IdNameResult
    warrantyTill: Optional[datetime] = None
    path: List[IdNameResult]
    sortOrder: int
    erpID: Optional[str] = None
    serialNumber: Optional[str] = None
    useAllWorkTypes: bool
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    name: str
    id: int


class UserResult(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[str] = None


class PeriodResult(BaseModel):
    from_: Optional[str] = Field(None, alias="from")
    till: Optional[str] = None


class GetAssetAssignmentResultModel(BaseModel):
    user: Optional[UserResult] = None
    validityPeriod: Optional[PeriodResult] = None
    notes: Optional[str] = None


class SuccessGetAssetAssignmentResultModel(BaseModel):
    result: List[GetAssetAssignmentResultModel]


class ListAttachmentResult(BaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class SuccessGetListAttachmentResultModel(RootModel):
    root: Dict[str, ListAttachmentResult]


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


class AssetAttributeResult(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    isPublic: Optional[bool] = None
    sortOrder: Optional[int] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListAssetAttributeResultModel(BaseModel):
    result: List[AssetAttributeResult]


class SuccessPutUploadFileModel(BaseModel):
    attachmentID: int
    publicUrl: str
    size: int


class GetAssetChecklistsModel(BaseModel):
    description: str
    name: str
    id: int


class SuccessGetAssetChecklistsModel(RootModel):
    root: Dict[str, List[GetAssetChecklistsModel]]


class GetAssetContactsResultModel(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    archived: Optional[str] = None
    assetID: Optional[int] = None
    contactID: Optional[int] = None
    id: Optional[int] = None


class SuccessGetAssetContactsResultModel(RootModel):
    root: Dict[str, GetAssetContactsResultModel]


class SuccessGetAssetContactByIdResult(BaseModel):
    email: Optional[str] = None
    phone01: Optional[str] = None
    phone02: Optional[str] = None
    phone03: Optional[str] = None
    description: Optional[str] = None
    fullName: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    deleted: Optional[str] = None
    archived: Optional[str] = None
    assetID: Optional[int] = None
    contactID: Optional[int] = None
    id: Optional[int] = None


class SuccessAddContactAssetResultModel(BaseModel):
    assetID: int
    contactID: int
    id: int


class SuccessListContactAssetResultModel(BaseModel):
    result: List[SuccessAddContactAssetResultModel]
