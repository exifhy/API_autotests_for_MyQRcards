from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    

class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddAssetTemplatesModel(StrictBaseModel):
    result: List[int]


class GetListAttachmentsFromAssetTemplate(StrictBaseModel):
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


class IdNameDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


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


class AssetTemplateAttributeResultModel(StrictBaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    isPublic: Optional[bool] = None
    sortOrder: Optional[int] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessAssetTemplateAttributeResultModel(StrictBaseModel):
    result: List[AssetTemplateAttributeResultModel]


class SuccessUploadAvatarToAssetTemplateModel(StrictBaseModel):
    attachmentID: Optional[int] = None
    publicUrl: Optional[str] = None
    size: Optional[int] = None


class IdNameModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class GetListAssetTemplatesModel(StrictBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assetName: Optional[str] = None
    hostAsset: Optional[IdNameModel] = None
    company: Optional[IdNameModel] = None
    assetType: Optional[IdNameModel] = None
    assetClass: Optional[IdNameModel] = None


class SuccessGetListAssetTemplatesModel(RootModel):
    root: Dict[str, GetListAssetTemplatesModel]


class AssetTypeResult(StrictBaseModel):
    isHostable: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None


class UserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


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


class AssetResult(StrictBaseModel):
    host: Optional[IdNameDeletedResult] = None
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetAssetTemplateResult(StrictBaseModel):
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


class DistrictsFromAssetTemplateModel(StrictBaseModel):
    name: str


class SuccessGetListDistrictsFromAssetTemplateModel(RootModel):
    root: Dict[str, DistrictsFromAssetTemplateModel]


class SuccessGetListSkillsFromAssetTemplateModel(StrictBaseModel):
    result: List[int]


class DescriptionWorkTypesModel(StrictBaseModel):
    description: Optional[str] = None
    name: str
    id: int


class ListWorkTypesFromAssetTemplateModel(StrictBaseModel):
    workType: DescriptionWorkTypesModel
    isDefault: Optional[bool] = None


class SuccessGetListWorkTypesFromAssetTemplateModel(StrictBaseModel):
    result: List[ListWorkTypesFromAssetTemplateModel]


class SuccessGetAssetTemplatesAttachmentsByIdNoRedirectModel(StrictBaseModel):
    fileName: str
    url: str
    size: int
    created: datetime
