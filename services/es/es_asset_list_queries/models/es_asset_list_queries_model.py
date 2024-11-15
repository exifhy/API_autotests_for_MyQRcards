from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict, Literal
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddAssetListQueryModel(BaseModel):
    result: List[int]


class Coordinate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PeriodResult(BaseModel):
    from_date: Optional[datetime] = None
    till: Optional[datetime] = None


class AssetFlagFilter(BaseModel):
    isMobile: Optional[bool] = None
    isAssigned: Optional[bool] = None
    hasSchema: Optional[bool] = None


class AssetTextFilter(BaseModel):
    name: Optional[str] = None


class FlagFilter(BaseModel):
    isPublished: Optional[bool] = None
    isDeleted: Optional[bool] = None
    isPublic: Optional[bool] = None
    isRead: Optional[bool] = None
    isExternal: Optional[bool] = None
    isHidden: Optional[bool] = None
    isSystem: Optional[bool] = None


class LocationFilter(BaseModel):
    radius: Optional[float] = None
    pointCenter: Optional[Coordinate] = None
    pointNorthEast: Optional[Coordinate] = None
    pointSouthWest: Optional[Coordinate] = None


class ExportFlagFilter(BaseModel):
    noData: Optional[bool] = None


class AssetFilterData(BaseModel):
    assetFlags: Optional[AssetFlagFilter] = None
    assetText: Optional[AssetTextFilter] = None
    warrantyPeriod: Optional[PeriodResult] = None
    responsiblePersons: Optional[List[int]] = None
    attributes: Optional[List[int]] = None
    orgUnits: Optional[List[int]] = None
    districts: Optional[List[int]] = None
    companies: Optional[List[int]] = None
    criticalities: Optional[List[int]] = None
    contracts: Optional[List[int]] = None
    workTypes: Optional[List[int]] = None
    skills: Optional[List[int]] = None
    assets: Optional[List[int]] = None
    startWithAssets: Optional[List[int]] = None
    tasks: Optional[List[int]] = None
    tags: Optional[List[str]] = None
    taskTypes: Optional[List[int]] = None
    flags: Optional[FlagFilter] = None
    validityPeriod: Optional[PeriodResult] = None
    creationPeriod: Optional[PeriodResult] = None
    parents: Optional[List[int]] = None
    users: Optional[List[int]] = None
    validityOnDates: Optional[List[datetime]] = None
    checkLists: Optional[List[int]] = None
    geoViewPort: Optional[LocationFilter] = None
    exportFlags: Optional[ExportFlagFilter] = None
    assetTypes: Optional[List[int]] = None
    assetClasses: Optional[List[int]] = None
    companyRegistrationTypes: Optional[List[int]] = None
    erpIDs: Optional[List[str]] = None
    contacts: Optional[List[int]] = None
    systemTags: Optional[List[int]] = None
    scheduleRules: Optional[List[int]] = None
    dateRangePeriod: Optional[PeriodResult] = None
    attributeValues: Optional[dict] = None
    eventTransportTypes: Optional[List[int]] = None
    materials: Optional[List[int]] = None
    warehouses: Optional[List[int]] = None


class RangeData(BaseModel):
    offset: Optional[int] = None
    fetch: Optional[int] = None


class SortData(BaseModel):
    orderBy: Optional[int] = None
    direction: Optional[Literal["Ascending", "Descending"]] = None


class AssetListQueryResult(BaseModel):
    name: Optional[str] = None
    filter: Optional[AssetFilterData] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    sort: Optional[SortData] = None
    queryString: Optional[str] = None


class SuccessGetAssetListQueryResultModel(RootModel):
    root: Dict[str, AssetListQueryResult]
