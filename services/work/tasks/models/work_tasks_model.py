from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddTasksModel(BaseModel):
    id: int
    number: str


class ResultDeleteModel(BaseModel):
    tenantID: Optional[int] = None
    taskID: Optional[int] = None
    error: Optional[str] = None


class SuccessDeleteTaskModel(BaseModel):
    list: Optional[List[ResultDeleteModel]] = None


class IdResult(BaseModel):
    id: Optional[int] = None


class TimeZoneResult(BaseModel):
    utcOffsetMinutes: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None


class CountryResult(BaseModel):
    id: Optional[int] = None
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None


class IdNameResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class TaskWorkTypeListResult(BaseModel):
    normalWorkingHours: Optional[int] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameDeletedResult(BaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskActualCriticalityResult(BaseModel):
    color: Optional[str] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskStatusResult(BaseModel):
    color: Optional[str] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class ScheduledAppointmentResult(BaseModel):
    notes: Optional[str] = None
    isContinuedOnTheNextDay: Optional[bool] = None
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[datetime] = None


class UserResult(BaseModel):
    tenantMemberID: Optional[int] = None
    coordinate: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    otherPhone: Optional[str] = None
    workPhone: Optional[str] = None
    isTechnician: Optional[bool] = None
    isCustomer: Optional[bool] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    coordinateActuality: Optional[datetime] = None
    distance: Optional[int] = None
    rate: Optional[float] = None
    rateCurrencyID: Optional[int] = None
    appointments: Optional[List[ScheduledAppointmentResult]] = None
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class AssetResult(BaseModel):
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    location: Optional[IdResult] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationResult(BaseModel):
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    deleted: Optional[datetime] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


class TimesheetResult(BaseModel):
    created: Optional[datetime] = None
    requested: Optional[datetime] = None
    statusChanged: Optional[datetime] = None
    deadline: Optional[datetime] = None
    completed: Optional[datetime] = None
    closed: Optional[datetime] = None
    accepted: Optional[datetime] = None
    assigned: Optional[datetime] = None
    escalated: Optional[datetime] = None
    lastUpdated: Optional[datetime] = None
    outdated: Optional[datetime] = None
    signed: Optional[datetime] = None
    requestedStart: Optional[datetime] = None
    requestedFinish: Optional[datetime] = None
    faultTimestamp: Optional[datetime] = None
    nextTaskStageMovement: Optional[datetime] = None


class IdNameColorResult(BaseModel):
    color: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskListResult(BaseModel):
    isAvailable: Optional[bool] = None
    isRated: Optional[bool] = None
    sortOrder: Optional[int] = None
    averageRating: Optional[float] = None
    lastModified: Optional[datetime] = None
    workType: Optional[TaskWorkTypeListResult] = None
    number: Optional[str] = None
    notes: Optional[str] = None
    contactPerson: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None
    serviceLevelAgreement: Optional[IdNameDeletedResult] = None
    actualCriticality: Optional[TaskActualCriticalityResult] = None
    taskStatus: Optional[TaskStatusResult] = None
    taskActuality: Optional[IdNameResult] = None
    taskType: Optional[IdNameDeletedResult] = None
    requestedBy: Optional[UserResult] = None
    assignedTo: Optional[UserResult] = None
    listAssignedTo: Optional[List[UserResult]] = None
    approvalWith: Optional[UserResult] = None
    escalatedTo: Optional[UserResult] = None
    company: Optional[IdNameDeletedResult] = None
    asset: Optional[AssetResult] = None
    location: Optional[LocationResult] = None
    timesheet: Optional[TimesheetResult] = None
    isFavourite: Optional[bool] = None
    deleted: Optional[datetime] = None
    taskStage: Optional[IdNameColorResult] = None
    listCategory: Optional[IdNameResult] = None
    parent: Optional[IdNameResult] = None
    childCount: Optional[int] = None
    erpID: Optional[str] = None


class SuccessTaskListResultModel(RootModel):
    root: Optional[Dict[str, TaskListResult]] = None


class CurrencyResult(BaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class ContractResult(BaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    date: Optional[str] = None
    dateTill: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None


class CompanyResult(BaseModel):
    code: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CounterResult(BaseModel):
    checkListsCount: Optional[int] = None
    completedWorksCount: Optional[int] = None


class TaskWorkTypeGetResult(BaseModel):
    normalWorkingHours: Optional[int] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class FlagsResult(BaseModel):
    isAllowMergeRating: Optional[bool] = None


class AttributeResult(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None


class AttributeTypeResult(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class MeasurementUnitResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class DomainResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class SuccessDetailedInfoModel(BaseModel):
    erpID: Optional[str] = None
    branch: Optional[IdNameResult] = None
    requestMethod: Optional[IdNameResult] = None
    requestedCriticality: Optional[IdNameDeletedResult] = None
    company: Optional[CompanyResult] = None
    payerCompany: Optional[IdNameDeletedResult] = None
    payeeCompany: Optional[IdNameDeletedResult] = None
    contract: Optional[ContractResult] = None
    actualCost: Optional[float] = None
    actualCostCurrency: Optional[CurrencyResult] = None
    estimatedCost: Optional[float] = None
    estimatedCostCurrency: Optional[CurrencyResult] = None
    actualTimeConsumptionMinutes: Optional[int] = None
    estimatedTimeConsumptionMinutes: Optional[int] = None
    acceptedPerson: Optional[str] = None
    counters: Optional[CounterResult] = None
    averageRating: Optional[float] = None
    workType: Optional[TaskWorkTypeGetResult] = None
    flags: Optional[FlagsResult] = None
    attribute: Optional[List[AttributeResult]] = None
    deadlineRuleID: Optional[int] = None
    lastModified: Optional[str] = None
    assetSchema: Optional[IdNameResult] = None
    notesHtml: Optional[str] = None
    number: Optional[str] = None
    notes: Optional[str] = None
    contactPerson: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None
    serviceLevelAgreement: Optional[IdNameDeletedResult] = None
    actualCriticality: Optional[IdNameDeletedResult] = None
    taskStatus: Optional[IdNameDeletedResult] = None
    taskActuality: Optional[IdNameResult] = None
    taskType: Optional[IdNameDeletedResult] = None
    requestedBy: Optional[UserResult] = None
    assignedTo: Optional[UserResult] = None
    listAssignedTo: Optional[List[UserResult]] = None
    approvalWith: Optional[UserResult] = None
    escalatedTo: Optional[UserResult] = None
    asset: Optional[LocationResult] = None
    timesheet: Optional[TimesheetResult] = None
    isFavourite: Optional[bool] = None
    deleted: Optional[str] = None
    taskStage: Optional[IdNameResult] = None
    listCategory: Optional[IdNameResult] = None
    parent: Optional[IdNameResult] = None
    childCount: Optional[int] = None


class TaskStageRequirementResult(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    arguments: Optional[str] = None


class ListStagesResult(BaseModel):
    name: Optional[str] = None
    verbName: Optional[str] = None
    taskViewTemplateID: Optional[int] = None
    stageDescription: Optional[str] = None
    permissionUiCode: Optional[str] = None
    taskStatus: Optional[IdNameResult] = None
    branch: Optional[IdNameResult] = None
    linkDescription: Optional[str] = None
    linkName: Optional[str] = None
    isPositiveResult: Optional[bool] = None
    isFinishStage: Optional[bool] = None
    sortOrder: Optional[int] = None
    requirements: Optional[Dict[str, TaskStageRequirementResult]] = None


class SuccessGetListStagesModel(RootModel):
    root: Dict[str, ListStagesResult]


class ConversationTaskModel(BaseModel):
    taskID: int
    id: int


class SuccessListConversationTaskModel(BaseModel):
    result: List[ConversationTaskModel]

