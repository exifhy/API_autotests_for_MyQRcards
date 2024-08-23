from typing import Optional, Dict, List
from pydantic import BaseModel
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
    scheduleRule: IdNameResult
    parent: Optional[ParentAssetResult] = None
    notes: Optional[str] = None
    publishedBy: Optional[int] = None
    responsiblePerson: Optional[AssetResponsiblePersonResult] = None
    avatarUrl: Optional[str] = None
    positionOnSchema: Optional[AssetPosition] = None
    hostAsset: Optional[IdNameDeletedResult] = None
    host: Optional[AssetResultWithLocation] = None
    location: Optional[LocationResult] = None
    isHostLocation: bool
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
