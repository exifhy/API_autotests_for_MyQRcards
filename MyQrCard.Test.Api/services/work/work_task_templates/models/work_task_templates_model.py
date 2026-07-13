from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict, Field
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ScheduleAppointmentBaseResult(StrictBaseModel):
    nextID: Optional[int] = None
    next: Optional[str] = None


class IdNameResult1(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class ListSchedulesResult(StrictBaseModel):
    isActive: Optional[bool] = None
    appointment: Optional[ScheduleAppointmentBaseResult] = None
    id: Optional[int] = None
    frequencyType: Optional[IdNameResult1] = None


class IdNameDeletedResult1(StrictBaseModel):
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdResult1(StrictBaseModel):
    id: Optional[int] = None


class HostAssetResult(StrictBaseModel):
    location: Optional[IdResult1] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class AssetResult(StrictBaseModel):
    deleted: Optional[str] = None
    parentID: Optional[int] = None
    location: Optional[IdResult1] = None
    host: Optional[HostAssetResult] = None
    company: Optional[IdNameDeletedResult1] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TimeZoneResult(StrictBaseModel):
    utcOffsetMinutes: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None


class CountryResult(StrictBaseModel):
    id: Optional[int] = None
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None


class LocationResult(StrictBaseModel):
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    deleted: Optional[str] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


class ContractResult(StrictBaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    date: Optional[str] = None
    dateTill: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None


class TaskTemplatesListResult(StrictBaseModel):
    schedule: Optional[ListSchedulesResult] = None
    sortOrder: Optional[int] = None
    assetCount: Optional[int] = None
    id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[str] = None
    isVisible: Optional[bool] = None
    published: Optional[str] = None
    notes: Optional[str] = None
    taskType: Optional[IdNameDeletedResult1] = None
    asset: Optional[AssetResult] = None
    location: Optional[LocationResult] = None
    workType: Optional[IdNameDeletedResult1] = None
    criticality: Optional[IdNameDeletedResult1] = None
    contract: Optional[ContractResult] = None
    serviceLevelAgreement: Optional[IdNameDeletedResult1] = None
    allowCreateTask: Optional[bool] = None


class SuccessGetTaskTemplatesModel(RootModel):
    """Main class GET"""
    root: Dict[str, TaskTemplatesListResult]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddTaskTemplatesModel(StrictBaseModel):
    templates: List[str]


class TaskTemplateAssignmentMergeModel(StrictBaseModel):
    tenantID: int
    taskTemplateID: str
    userID: int
    error: Optional[str] = None


class SuccessTaskTemplateAssignmentMergeModel(StrictBaseModel):
    task: List[TaskTemplateAssignmentMergeModel]


class SuccessActivateTaskTemplatesSchedulesModel(StrictBaseModel):
    isActive: Optional[bool] = None
    nextAppointment: Optional[datetime] = None


class IdNameResult(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetListExcludedAssetsTaskTemplateModel(RootModel):
    root: Dict[str, IdNameResult]


class IdNameDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameDescriptionResult(StrictBaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class PeriodResult(StrictBaseModel):
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[datetime] = None


class CurrencyResult(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class ScheduledAppointmentResult(StrictBaseModel):
    notes: Optional[str] = None
    isContinuedOnTheNextDay: Optional[bool] = None
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[datetime] = None


class UserResult(StrictBaseModel):
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


class TimesheetResult(StrictBaseModel):
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


class AssetFilterResult(StrictBaseModel):
    workTypes: Optional[List[int]] = None
    taskTypes: Optional[List[int]] = None
    assetClasses: Optional[List[int]] = None
    assetTypes: Optional[List[int]] = None
    assets: Optional[List[int]] = None
    responsiblePersons: Optional[List[int]] = None
    districts: Optional[List[int]] = None
    companies: Optional[List[int]] = None
    warrantyPeriod: Optional[PeriodResult] = None


class TaskTemplatesGetResultModel(StrictBaseModel):
    parentTaskID: Optional[int] = None
    erpID: Optional[str] = None
    contactPerson: Optional[str] = None
    contactPhone: Optional[str] = None
    contactEmail: Optional[str] = None
    requestMethod: Optional[IdNameResult] = None
    payerCompany: Optional[IdNameDeletedResult] = None
    requestedBy: Optional[UserResult] = None
    assignedTo: Optional[UserResult] = None
    timesheet: Optional[TimesheetResult] = None
    estimatedTimeConsumptionMinutes: Optional[int] = None
    estimatedCost: Optional[float] = None
    estimatedCostCurrency: Optional[CurrencyResult] = None
    invitation: Optional[IdNameDescriptionResult] = None
    taskCreationUrl: Optional[str] = None
    assetFilter: Optional[AssetFilterResult] = None
    id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    isVisible: Optional[bool] = None
    published: Optional[datetime] = None
    notes: Optional[str] = None
    taskType: Optional[IdNameDeletedResult] = None
    asset: Optional[IdNameDeletedResult] = None
    location: Optional[LocationResult] = None
    workType: Optional[IdNameDeletedResult] = None
    criticality: Optional[IdNameDeletedResult] = None
    contract: Optional[ContractResult] = None
    serviceLevelAgreement: Optional[IdNameDeletedResult] = None
    allowCreateTask: Optional[bool] = None


class PublishTaskTemplateModel(StrictBaseModel):
    id: str


class IdResult(StrictBaseModel):
    id: Optional[int] = None


class MeasurementUnitResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class PublicAttributeResult(StrictBaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    measurementUnit: Optional[MeasurementUnitResult] = None


class PublicAttachmentResult(StrictBaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    contentType: Optional[str] = None


class PublicAssetResult(StrictBaseModel):
    assetClass: Optional[IdNameResult] = None
    avatarUrl: Optional[str] = None
    notes: Optional[str] = None
    warrantyTill: Optional[datetime] = None
    attributes: Optional[List[PublicAttributeResult]] = None
    attachments: Optional[List[PublicAttachmentResult]] = None
    host: Optional[IdNameDeletedResult] = None
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationShortResult(StrictBaseModel):
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


class GetPublicResultModel(StrictBaseModel):
    tenant: Optional[IdResult] = None
    description: Optional[str] = None
    publicAsset: Optional[PublicAssetResult] = None
    taskCreationUrl: Optional[str] = None
    invitation: Optional[IdResult] = None
    location: Optional[LocationShortResult] = None
    allowCreateTask: Optional[bool] = None
    code: Optional[str] = None
    id: str


class TaskTemplateAssignmentDetailsProjectionModel(StrictBaseModel):
    tenantID: int
    taskTemplateID: str
    userID: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None


class SuccessGetListTaskTemplateAssignmentDetailsProjectionModel(StrictBaseModel):
    results: List[TaskTemplateAssignmentDetailsProjectionModel]


class ScheduleStateResult(StrictBaseModel):
    isActive: Optional[bool] = None
    timeStamp: Optional[datetime] = None


class ScheduleAppointmentResult(StrictBaseModel):
    total: Optional[int] = None
    remaining: Optional[int] = None
    previousID: Optional[int] = None
    previous: Optional[datetime] = None
    nextID: Optional[int] = None
    next: Optional[datetime] = None


class ExceptionResult(StrictBaseModel):
    statusCode: Optional[int] = None
    traceIdentifier: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    arguments: Optional[Dict[str, str]] = None


class TaskResult(StrictBaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    notes: Optional[str] = None
    unreadMessagesCount: Optional[int] = None


class GetSchedulesResultModel(StrictBaseModel):
    state: Optional[ScheduleStateResult] = None
    appointment: Optional[ScheduleAppointmentResult] = None
    exceptions: Optional[List[ExceptionResult]] = None
    task: Optional[TaskResult] = None
    id: Optional[int] = None
    frequencyType: Optional[IdNameResult] = None


class SuccessGetListGetSchedulesResultModel(StrictBaseModel):
    results: List[GetSchedulesResultModel]
