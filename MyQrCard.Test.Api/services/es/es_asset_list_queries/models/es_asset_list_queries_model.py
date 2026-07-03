from pydantic import BaseModel, RootModel, ConfigDict
from typing import List, Optional, Dict, Literal
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


class SuccessAddAssetListQueryModel(StrictBaseModel):
    result: List[int]


class NameIdModel(StrictBaseModel):
    name: str
    id: str


class Coordinate(StrictBaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PeriodResult(StrictBaseModel):
    from_date: Optional[datetime] = None
    till: Optional[datetime] = None


class AssetFlagFilter(StrictBaseModel):
    isMobile: Optional[bool] = None
    isAssigned: Optional[bool] = None
    hasSchema: Optional[bool] = None


class AssetTextFilter(StrictBaseModel):
    name: Optional[str] = None


class FlagFilter(StrictBaseModel):
    isPublished: Optional[bool] = None
    isDeleted: Optional[bool] = None
    isPublic: Optional[bool] = None
    isRead: Optional[bool] = None
    isExternal: Optional[bool] = None
    isHidden: Optional[bool] = None
    isSystem: Optional[bool] = None


class LocationFilter(StrictBaseModel):
    radius: Optional[float] = None
    pointCenter: Optional[Coordinate] = None
    pointNorthEast: Optional[Coordinate] = None
    pointSouthWest: Optional[Coordinate] = None


class ExportFlagFilter(StrictBaseModel):
    noData: Optional[bool] = None


class AssetFilterData(StrictBaseModel):
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


class AssetFilterListDataModel(StrictBaseModel):
    assetFlags: Optional[AssetFlagFilter] = None
    assetText: Optional[AssetTextFilter] = None
    warrantyPeriod: Optional[PeriodResult] = None
    responsiblePersons: Optional[List[int]] = None
    attributes: Optional[List[int]] = None
    orgUnits: Optional[List[int]] = None
    districts: Optional[List[NameIdModel]] = None
    companies: Optional[List[NameIdModel]] = None
    criticalities: Optional[List[int]] = None
    contracts: Optional[List[int]] = None
    workTypes: Optional[List[NameIdModel]] = None
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
    assetTypes: Optional[List[NameIdModel]] = None
    assetClasses: Optional[List[NameIdModel]] = None
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


class RangeData(StrictBaseModel):
    offset: Optional[int] = None
    fetch: Optional[int] = None


class SortData(StrictBaseModel):
    orderBy: Optional[int] = None
    direction: Optional[Literal["Ascending", "Descending"]] = None


class AssetListQueryResult(StrictBaseModel):
    name: Optional[str] = None
    filter: Optional[AssetFilterData] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    sort: Optional[SortData] = None
    queryString: Optional[str] = None


class AssetListQueryFixedResult(StrictBaseModel):
    name: Optional[str] = None
    filterList: Optional[AssetFilterListDataModel] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    sort: Optional[SortData] = None
    queryString: Optional[str] = None
    deleted: Optional[datetime] = None


class SuccessGetAssetListQueryResultModel(RootModel):
    root: Dict[str, AssetListQueryResult]
