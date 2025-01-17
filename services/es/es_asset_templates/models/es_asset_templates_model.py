from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddAssetTemplatesModel(BaseModel):
    result: List[int]


class GetListAttachmentsFromAssetTemplate(BaseModel):
    fileName: str
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[datetime] = None


class SuccessGetListAttachmentsFromAssetTemplate(RootModel):
    root: Dict[str, GetListAttachmentsFromAssetTemplate]


class IdNameDeletedResult(BaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


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


class AssetTemplateAttributeResultModel(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    isPublic: Optional[bool] = None
    sortOrder: Optional[int] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessAssetTemplateAttributeResultModel(BaseModel):
    result: List[AssetTemplateAttributeResultModel]


class SuccessUploadAvatarToAssetTemplateModel(BaseModel):
    attachmentID: Optional[int] = None
    publicUrl: Optional[str] = None
    size: Optional[int] = None


class IdNameModel(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class GetListAssetTemplatesModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assetName: Optional[str] = None
    hostAsset: Optional[IdNameModel] = None
    company: Optional[IdNameModel] = None
    assetType: Optional[IdNameModel] = None
    assetClass: Optional[IdNameModel] = None


class SuccessGetListAssetTemplatesModel(RootModel):
    root: Dict[str, GetListAssetTemplatesModel]


class AssetTypeResult(BaseModel):
    isHostable: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class UserResult(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


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


class AssetResult(BaseModel):
    host: Optional[IdNameDeletedResult] = None
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetAssetTemplateResult(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hostAsset: Optional[IdNameModel] = None
    assetName: Optional[str] = None
    company: Optional[IdNameModel] = None
    assetType: Optional[AssetTypeResult] = None
    assetClass: Optional[IdNameModel] = None
    responsiblePerson: Optional[UserResult] = None
    erpID: Optional[str] = None
    scheduleRuleID: Optional[int] = None
    checkListID: Optional[int] = None
    warrantyTill: Optional[datetime] = None
    notes: Optional[str] = None
    isMobileAsset: Optional[bool] = None
    isInheritParentDistricts: Optional[bool] = None
    isSkipForEscalation: Optional[bool] = None
    isStopEscalation: Optional[bool] = None
    location: Optional[LocationResult] = None
    parentAsset: Optional[AssetResult] = None
    avatarUrl: Optional[str] = None


class DistrictsFromAssetTemplateModel(BaseModel):
    name: str


class SuccessGetListDistrictsFromAssetTemplateModel(RootModel):
    root: Dict[str, DistrictsFromAssetTemplateModel]


class SuccessGetListSkillsFromAssetTemplateModel(BaseModel):
    result: List[int]


class DescriptionWorkTypesModel(BaseModel):
    description: Optional[str] = None
    name: str
    id: int


class ListWorkTypesFromAssetTemplateModel(BaseModel):
    workType: DescriptionWorkTypesModel
    isDefault: bool


class SuccessGetListWorkTypesFromAssetTemplateModel(BaseModel):
    result: List[ListWorkTypesFromAssetTemplateModel]
