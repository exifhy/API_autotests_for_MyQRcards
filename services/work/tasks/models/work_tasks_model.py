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


class AttachmentBaseResult(BaseModel):
    id: Optional[int] = None
    fileName: Optional[str] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class TaskConversationDeliveryResult(BaseModel):
    toAnyone: Optional[bool] = None
    toAll: Optional[bool] = None
    toCurrentUser: Optional[datetime] = None


class TaskConversationReadResult(BaseModel):
    byAnyone: Optional[bool] = None
    byAll: Optional[bool] = None
    byCurrentUser: Optional[datetime] = None
    isReadExpected: Optional[bool] = None


class TaskMessageModel(BaseModel):
    id: Optional[int] = None
    created: Optional[datetime] = None
    message: Optional[str] = None
    isExternal: Optional[bool] = None
    author: Optional[UserResult] = None
    attachment: Optional[List[AttachmentBaseResult]] = None
    delivery: Optional[TaskConversationDeliveryResult] = None
    read: Optional[TaskConversationReadResult] = None


class SuccessGetListTaskMessageModel(BaseModel):
    results: List[TaskMessageModel]


class PeriodResult(BaseModel):
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[str] = None


class AssignmentHistoryResultModel(BaseModel):
    sortOrder: Optional[int] = None
    assigned: Optional[str] = None
    assignedTo: Optional[UserResult] = None
    assignedBy: Optional[UserResult] = None
    scheduled: Optional[PeriodResult] = None


class SuccessGetListAssignmentHistoryResultModel(BaseModel):
    result: List[AssignmentHistoryResultModel]


class AttachmentResultModel(BaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class AttachmentResultByIdModel(BaseModel):
    attachmentID: int
    fileName: str
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class SuccessGetListAttachmentResultModel(RootModel):
    root: Dict[str, AttachmentResultModel]


class SuccessGetAttributeAttachmentResultModel(RootModel):
    root: Dict[str, List[AttachmentResultByIdModel]]


class SuccessGetAttachmentLinkNoRedirectModel(BaseModel):
    fileName: str
    url: str
    size: int
    created: datetime


class AttributeResultModel(BaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListAttributeResultModel(BaseModel):
    result: List[AttributeResultModel]


class ChangeTypeResult(BaseModel):
    tab: IdNameResult
    sections: List[IdNameResult]


class SuccessGetListTaskChangeTypeResultModel(BaseModel):
    result: List[ChangeTypeResult]


class Initiator(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatarUrl: Optional[str] = None


class HistoryResult(BaseModel):
    sortOrder: Optional[int] = None
    uid: Optional[str] = None
    occured: Optional[str] = None
    operation: Optional[str] = None
    tab: Optional[str] = None
    section: Optional[str] = None
    applicationID: Optional[int] = None
    user: Optional[Initiator] = None
    locationState: Optional[int] = None
    location: Optional[str] = None
    previousSnapshot: Optional[dict] = None
    currentSnapshot: Optional[dict] = None
    diff: Optional[dict] = None


class SuccessGetListTaskChangesResultModel(BaseModel):
    result: Optional[List[HistoryResult]] = None


class IdNameChecklistResult(BaseModel):
    description: Optional[str] = None
    name: str
    id: int


class TaskCheckListResult(BaseModel):
    checkList: IdNameChecklistResult
    completedWorkID: Optional[int] = None
    totalItemsCount: Optional[int] = None
    completedItemsCount: Optional[int] = None


class SuccessGetListTaskCheckListResultModel(RootModel):
    root: Dict[str, TaskCheckListResult]


class AddChecklistsToTaskModel(BaseModel):
    taskID: int
    id: int


class SuccessAddChecklistsToTaskModel(BaseModel):
    result: List[AddChecklistsToTaskModel]


class SuccessUploadAttachmentsToServerTaskChecklistDataFromFormModel(BaseModel):
    taskID: int
    taskCheckListID: int
    taskCheckListResultID: int
    attachments: List[int]
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class AttributeTypeResultChecklist(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class TaskCheckListResultV2ResultModel(BaseModel):
    isChecked: Optional[bool] = None
    value: Optional[List[str]] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sortOrder: Optional[int] = None
    attribute: Optional[IdNameChecklistResult] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None


class SuccessGetTaskCheckListResultV2ResultModel(RootModel):
    root: Dict[str, TaskCheckListResultV2ResultModel]


class SuccessGetAttachmentByIdFromTaskChecklist(BaseModel):
    tenantID: int
    taskID: int
    taskCheckListID: int
    taskCheckListResultID: int
    attachmentID: int
    contentType: str
    isProtected: bool
    fileName: str
    internalFileName: Optional[str] = None
    storageLogin: Optional[str] = None
    securityKey: str
    storageContainer: str
    size: int
    created: datetime


class SuccessUploadAttachmentsToServerTaskCompletedWorkDataFromFormModel(BaseModel):
    taskID: int
    completedWorkID: int
    attributeID: int
    attachments: List[int]


class UpdateTaskChecklistResultsModel(BaseModel):
    taskID: int
    taskCheckListID: int
    checkListItemID: int


class SuccessUpdateTaskChecklistResultsModel(BaseModel):
    result: List[UpdateTaskChecklistResultsModel]


class CompletedWorkAttributeResult(BaseModel):
    taskID: int
    completedWorkID: int
    attribute: Optional[IdNameDeletedResult] = None
    selectionMode: Optional[IdNameResult] = None
    values: Optional[List[str]] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListCompletedWorkAttributeResultModel(BaseModel):
    result: List[CompletedWorkAttributeResult]


class ListAttributesTaskCompletedWorksModel(BaseModel):
    taskID: int
    completedWorkID: int
    attributeID: int


class SuccessGetListAttributesTaskCompletedWorksModel(BaseModel):
    results: List[ListAttributesTaskCompletedWorksModel]


class WorkTypeResult(BaseModel):
    id: int
    name: Optional[str] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None


class HostAssetResult(BaseModel):
    location: Optional[IdResult] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class MaintainedAssetResult(BaseModel):
    deleted: Optional[str] = None
    parentID: Optional[int] = None
    location: Optional[IdResult] = None
    host: Optional[HostAssetResult] = None
    company: Optional[IdNameDeletedResult] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompletedWorkResult(BaseModel):
    id: int
    workType: Optional[WorkTypeResult] = None
    maintainedAsset: Optional[AssetResult] = None
    started: Optional[str] = None
    finished: Optional[str] = None
    notes: Optional[str] = None
    quantity: Optional[float] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    created: Optional[str] = None


class SuccessGetListCompletedWorkResult(BaseModel):
    result: List[CompletedWorkResult]


class AttachmentsTaskCompletedWorksModel(BaseModel):
    attachmentID: int
    completedWorkID: int
    fileName: str
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[datetime] = None


class SuccessGetListAttachmentsTaskCompletedWorksModel(BaseModel):
    result: List[AttachmentsTaskCompletedWorksModel]


class MaterialsTaskComplectedWorkModel(BaseModel):
    taskID: int
    completedWorkID: int
    materialID: int
    warehouseID: int
    inventoryID: int


class SuccessAddMaterialsTaskComplectedWork(BaseModel):
    results: List[MaterialsTaskComplectedWorkModel]


class TechniciansTaskComplectedWorkModel(BaseModel):
    taskID: int
    completedWorkID: int
    userID: int


class SuccessAddTechniciansTaskComplectedWorkModel(BaseModel):
    results: List[TechniciansTaskComplectedWorkModel]


class IdNameErpIDResult(BaseModel):
    erpID: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TakenByUserResult(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class MaterialResult(BaseModel):
    inventoryID: Optional[int] = None
    materialID: Optional[int] = None
    materialName: Optional[str] = None
    materialErpID: Optional[str] = None
    materialDeleted: Optional[datetime] = None
    warehouse: Optional[IdNameErpIDResult] = None
    measurementUnit: Optional[IdNameResult] = None
    quantity: Optional[float] = None
    consumed: Optional[datetime] = None
    takenByUser: Optional[TakenByUserResult] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None
    sortOrder: Optional[int] = None


class SuccessGetListCompletedWorkMaterialResultModel(BaseModel):
    taskID: Optional[int] = None
    completedWorkID: Optional[int] = None
    materials: Optional[List[MaterialResult]] = None


class SuccessGetListRootCompletedWorkMaterialResultModel(RootModel):
    root: Dict[str, SuccessGetListCompletedWorkMaterialResultModel]


class SuccessUploadAttachToReportTaskCompletedWorkModel(BaseModel):
    taskID: int
    attachmentID: int
    md5Hash: str
    fileName: str
    isProtected: bool


class SignatureReportAttachmentModel(BaseModel):
    tenantID: Optional[int] = None
    attachmentID: Optional[int] = None
    taskID: Optional[int] = None
    fileName: Optional[str] = None
    internalFileName: Optional[str] = None
    contentType: Optional[str] = None
    storageLogin: Optional[str] = None
    securityKey: Optional[str] = None
    size: Optional[int] = None
    created: Optional[datetime] = None
    storageContainer: Optional[str] = None
    isProtected: Optional[bool] = None


class TechnicianResult(BaseModel):
    userID: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    rate: Optional[float] = None
    rateCurrencyID: Optional[int] = None


class CompletedWorkTechnicianResult(BaseModel):
    taskID: int
    completedWorkID: int
    technicians: List[TechnicianResult]


class SuccessGetListCompletedWorkTechnicianResult(RootModel):
    root: Dict[str, CompletedWorkTechnicianResult]


class TaskContactsListResultModel(BaseModel):
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    deleted: Optional[datetime] = None
    description: Optional[str] = None
    archived: Optional[datetime] = None
    taskID: Optional[int] = None
    contactID: Optional[int] = None


class SuccessGetTaskContactsListResultModel(RootModel):
    root: Dict[str, TaskContactsListResultModel]


class SuccessUploadAttachmentsToServerTaskConversationDataFromFormModel(BaseModel):
    taskID: Optional[int] = None
    taskconversationID: int
    attachments: List[int]
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class ConversationDeliveryResult(BaseModel):
    recipient: Optional[UserResult] = None
    delivered: Optional[datetime] = None
    read: Optional[datetime] = None


class SuccessGetListConversationDeliveryResult(BaseModel):
    results: List[ConversationDeliveryResult]
