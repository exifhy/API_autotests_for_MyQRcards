from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel, ConfigDict
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AssetTaskActualityResult(StrictBaseModel):
    self: int
    nested: int


class IdNameDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdResult(StrictBaseModel):
    id: Optional[int] = None


class TimeZoneResult(StrictBaseModel):
    utcOffsetMinutes: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CountryResult(StrictBaseModel):
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationResult(StrictBaseModel):
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    id: Optional[int] = None


class AssetResultWithLocation(StrictBaseModel):
    location: Optional[IdResult] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class AssetExtResult(StrictBaseModel):
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


class AssetExtResults(StrictBaseModel):
    """Main model AssetList"""
    results: Dict[str, AssetExtResult]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdNameResultModel(StrictBaseModel):
    name: str
    id: int

class IdNameResultWithConcurrencyStampModel(StrictBaseModel):
    name: str
    id: int
    concurrencyStamp: str


class AssetTypeResult(StrictBaseModel):
    isHostable: bool
    name: str
    id: int


class IdNameResult(StrictBaseModel):
    name: str
    id: int


class ParentAssetResult(StrictBaseModel):
    assetType: AssetTypeResult
    deleted: Optional[datetime] = None
    name: str
    id: int


class AssetResponsiblePersonResult(StrictBaseModel):
    userID: int
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    email: Optional[str] = None
    isEmailVerified: bool
    isMobilePhoneVerified: bool


class AssetPosition(StrictBaseModel):
    schemaID: int
    x: int
    y: int


class AssetResultWithLocationDetailedInfo(StrictBaseModel):
    location: IdNameResult
    deleted: Optional[datetime] = None
    name: str
    id: int


class AssetDetailedInfoResult(StrictBaseModel):
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
    isInheritParentDistricts: bool


class UserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[str] = None


class PeriodResult(StrictBaseModel):
    from_: Optional[str] = Field(None, alias="from")
    till: Optional[str] = None


class GetAssetAssignmentResultModel(StrictBaseModel):
    user: Optional[UserResult] = None
    validityPeriod: Optional[PeriodResult] = None
    notes: Optional[str] = None


class SuccessGetAssetAssignmentResultModel(StrictBaseModel):
    result: List[GetAssetAssignmentResultModel]


class ListAttachmentResult(StrictBaseModel):
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


class AttributeTypeResult(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class MeasurementUnitResult(StrictBaseModel):
    abbreviation: Optional[str] = None
    designation: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class DomainResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class AssetAttributeResult(StrictBaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    isPublic: Optional[bool] = None
    sortOrder: Optional[int] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListAssetAttributeResultModel(StrictBaseModel):
    result: List[AssetAttributeResult]


class SuccessPutUploadFileModel(StrictBaseModel):
    attachmentID: int
    publicUrl: str
    size: int


class GetAssetChecklistsModel(StrictBaseModel):
    description: str
    name: str
    id: int


class SuccessGetAssetChecklistsModel(RootModel):
    root: Dict[str, List[GetAssetChecklistsModel]]


class GetAssetContactsResultModel(StrictBaseModel):
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


class SuccessGetAssetContactByIdResult(StrictBaseModel):
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


class SuccessAddContactAssetResultModel(StrictBaseModel):
    assetID: int
    contactID: int
    id: int


class SuccessListContactAssetResultModel(StrictBaseModel):
    result: List[SuccessAddContactAssetResultModel]


class AssetDistrictResultModel(StrictBaseModel):
    parentID: Optional[int] = None
    name: str


class SuccessAssetDistrictResultModel(RootModel):
    root: Dict[str, AssetDistrictResultModel]


class SuccessAssetSkillResultModel(RootModel):
    root: Dict[str, IdNameResult]


class SuccessGetTagsAssetsModel(StrictBaseModel):
    result: List[str]


class GetAssetWorkTypesResult(StrictBaseModel):
    workClassID: Optional[int] = None
    name: str
    description: Optional[str] = None
    parentID: Optional[int] = None
    hasChildren: Optional[bool] = None


class SuccessGetAssetWorkTypesResult(RootModel):
    root: Dict[str, GetAssetWorkTypesResult]
