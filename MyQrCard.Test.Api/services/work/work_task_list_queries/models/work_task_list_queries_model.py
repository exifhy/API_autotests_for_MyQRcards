from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, Field


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class PeriodResult(BaseModel):
    from_: Optional[str] = Field(None, alias="from")
    till: Optional[str] = None


class TaskFlagFilter(BaseModel):
    hasAssigneeCheckedIn: Optional[bool] = None
    isClosed: Optional[bool] = None
    isFavourite: Optional[bool] = None
    isCompleted: Optional[bool] = None
    isAssigned: Optional[bool] = None
    isOutdated: Optional[bool] = None
    isRated: Optional[bool] = None
    isScheduled: Optional[bool] = None


class FlagFilter(BaseModel):
    isPublished: Optional[bool] = None
    isDeleted: Optional[bool] = None
    isPublic: Optional[bool] = None
    isRead: Optional[bool] = None
    isExternal: Optional[bool] = None
    isHidden: Optional[bool] = None
    isSystem: Optional[bool] = None


class Coordinate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationFilter(BaseModel):
    radius: Optional[float] = None
    pointCenter: Optional[Coordinate] = None
    pointNorthEast: Optional[Coordinate] = None
    pointSouthWest: Optional[Coordinate] = None


class ExportFlagFilter(BaseModel):
    noData: Optional[bool] = None


class TaskFilterData(BaseModel):
    requestedBy: Optional[List[int]] = None
    assignedTo: Optional[List[int]] = None
    approvalWith: Optional[List[int]] = None
    escalatedTo: Optional[List[int]] = None
    assetResponsiblePersons: Optional[List[int]] = None
    taskStatuses: Optional[List[int]] = None
    taskStages: Optional[List[int]] = None
    taskFlags: Optional[TaskFlagFilter] = None
    assignationPeriod: Optional[PeriodResult] = None
    completionPeriod: Optional[PeriodResult] = None
    closingPeriod: Optional[PeriodResult] = None
    deadlinePeriod: Optional[PeriodResult] = None
    taskNumbers: Optional[List[str]] = None
    ratingCriterias: Optional[List[int]] = None
    taskTemplates: Optional[List[str]] = None
    requestMethods: Optional[List[int]] = None
    branches: Optional[List[int]] = None
    assetSchemas: Optional[List[int]] = None
    lastModifiedPeriod: Optional[PeriodResult] = None
    completedWorks: Optional[List[int]] = None
    payeeCompanies: Optional[List[int]] = None
    tabs: Optional[List[str]] = None
    sections: Optional[List[str]] = None
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
    validityOnDates: Optional[List[str]] = None
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
    attributeValues: Optional[List[dict]] = None
    eventTransportTypes: Optional[List[int]] = None
    materials: Optional[List[int]] = None
    warehouses: Optional[List[int]] = None


class RangeData(BaseModel):
    offset: Optional[int] = None
    fetch: Optional[int] = None


class SortData(BaseModel):
    orderBy: Optional[int] = None
    direction: Optional[int] = None


class TaskListQueryResultModel(BaseModel):
    name: str
    filter: Optional[TaskFilterData] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    deleted: Optional[str] = None
    sort: Optional[SortData] = None
    queryString: Optional[str] = None


class SuccessGetTaskListQueryResultModel(RootModel):
    root: Dict[str, TaskListQueryResultModel]


class SuccessAddTaskListQueryResultModel(BaseModel):
    result: List[int]
