from typing import Optional, Dict, List
from pydantic import BaseModel, Field, RootModel, ConfigDict
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


class SuccessAddTasksModel(StrictBaseModel):
    id: int
    number: str


class SuccessAddTasksWithConcurrencyStampModel(StrictBaseModel):
    id: int
    number: str
    concurrencyStamp: str


class ResultDeleteModel(StrictBaseModel):
    tenantID: int
    taskID: int
    error: Optional[str] = None


class SuccessDeleteTaskModel(StrictBaseModel):
    list: List[ResultDeleteModel]


class IdResult(StrictBaseModel):
    id: Optional[int] = None


class TimeZoneResult(StrictBaseModel):
    utcOffsetMinutes: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None


class CountryResult(StrictBaseModel):
    id: Optional[int] = None
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None


class IdNameResult(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class TaskWorkTypeListResult(StrictBaseModel):
    normalWorkingHours: Optional[int] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskActualCriticalityResult(StrictBaseModel):
    color: Optional[str] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskStatusResult(StrictBaseModel):
    color: Optional[str] = None
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


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


class AssetResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    location: Optional[IdResult] = None
    name: Optional[str] = None
    id: Optional[int] = None


class LocationResult(StrictBaseModel):
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    deleted: Optional[datetime] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


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


class HostAssetResult(StrictBaseModel):
    location: Optional[IdResult] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskAssetResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None
    location: Optional[IdResult] = None
    host: Optional[HostAssetResult] = None
    company: Optional[IdNameDeletedResult] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameColorResult(StrictBaseModel):
    color: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskListResult(StrictBaseModel):
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
    asset: Optional[TaskAssetResult] = None
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
    root: Dict[str, TaskListResult]


class CurrencyResult(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class ContractResult(StrictBaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    date: Optional[str] = None
    dateTill: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None


class CompanyResult(StrictBaseModel):
    code: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CounterResult(StrictBaseModel):
    checkListsCount: Optional[int] = None
    completedWorksCount: Optional[int] = None


class TaskWorkTypeGetResult(StrictBaseModel):
    normalWorkingHours: Optional[int] = None
    normalWorkingMinutes: Optional[int] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class FlagsResult(StrictBaseModel):
    isAllowMergeRating: Optional[bool] = None


class AttributeResult(StrictBaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None


class AttributeTypeResult(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class MeasurementUnitResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    designation: Optional[str] = None


class DomainResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class SuccessDetailedInfoModel(StrictBaseModel):
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
    actualCriticality: Optional[TaskActualCriticalityResult] = None
    taskStatus: Optional[IdNameDeletedResult] = None
    taskActuality: Optional[IdNameResult] = None
    taskType: Optional[IdNameDeletedResult] = None
    requestedBy: Optional[UserResult] = None
    assignedTo: Optional[UserResult] = None
    listAssignedTo: Optional[List[UserResult]] = None
    approvalWith: Optional[UserResult] = None
    escalatedTo: Optional[UserResult] = None
    asset: Optional[TaskAssetResult] = None
    location: Optional[LocationResult] = None
    timesheet: Optional[TimesheetResult] = None
    isFavourite: Optional[bool] = None
    deleted: Optional[str] = None
    taskStage: Optional[IdNameResult] = None
    listCategory: Optional[IdNameResult] = None
    parent: Optional[IdNameResult] = None
    childCount: Optional[int] = None


class TaskStageRequirementResult(StrictBaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    arguments: Optional[str] = None


class ListStagesResult(StrictBaseModel):
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


class ConversationTaskModel(StrictBaseModel):
    taskID: int
    id: int


class SuccessListConversationTaskModel(StrictBaseModel):
    result: List[ConversationTaskModel]


class AttachmentBaseResult(StrictBaseModel):
    id: Optional[int] = None
    fileName: Optional[str] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class TaskConversationDeliveryResult(StrictBaseModel):
    toAnyone: Optional[bool] = None
    toAll: Optional[bool] = None
    toCurrentUser: Optional[datetime] = None


class TaskConversationReadResult(StrictBaseModel):
    byAnyone: Optional[bool] = None
    byAll: Optional[bool] = None
    byCurrentUser: Optional[datetime] = None
    isReadExpected: Optional[bool] = None


class TaskMessageModel(StrictBaseModel):
    id: Optional[int] = None
    created: Optional[datetime] = None
    message: Optional[str] = None
    isExternal: Optional[bool] = None
    author: Optional[UserResult] = None
    attachment: Optional[List[AttachmentBaseResult]] = None
    delivery: Optional[TaskConversationDeliveryResult] = None
    read: Optional[TaskConversationReadResult] = None


class SuccessGetListTaskMessageModel(StrictBaseModel):
    results: List[TaskMessageModel]


class PeriodResult(StrictBaseModel):
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[str] = None


class AssignmentHistoryResultModel(StrictBaseModel):
    sortOrder: Optional[int] = None
    assigned: Optional[str] = None
    assignedTo: Optional[UserResult] = None
    assignedBy: Optional[UserResult] = None
    scheduled: Optional[PeriodResult] = None


class SuccessGetListAssignmentHistoryResultModel(StrictBaseModel):
    result: List[AssignmentHistoryResultModel]


class AttachmentResultModel(StrictBaseModel):
    fileName: Optional[str] = None
    description: Optional[str] = None
    isUploaded: Optional[bool] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    isProtected: Optional[bool] = None
    size: Optional[int] = None
    created: Optional[str] = None


class AttachmentResultByIdModel(StrictBaseModel):
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


class SuccessGetAttachmentLinkNoRedirectModel(StrictBaseModel):
    fileName: str
    url: str
    size: int
    created: datetime


class AttributeResultModel(StrictBaseModel):
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListAttributeResultModel(StrictBaseModel):
    result: List[AttributeResultModel]


class ChangeTypeResult(StrictBaseModel):
    tab: IdNameResult
    sections: List[IdNameResult]


class SuccessGetListTaskChangeTypeResultModel(StrictBaseModel):
    result: List[ChangeTypeResult]


class Initiator(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    avatarUrl: Optional[str] = None


class HistoryResult(StrictBaseModel):
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


class SuccessGetListTaskChangesResultModel(StrictBaseModel):
    result: Optional[List[HistoryResult]] = None


class IdNameChecklistResult(StrictBaseModel):
    description: Optional[str] = None
    name: str
    id: int


class TaskCheckListResult(StrictBaseModel):
    checkList: IdNameChecklistResult
    completedWorkID: Optional[int] = None
    totalItemsCount: Optional[int] = None
    completedItemsCount: Optional[int] = None


class SuccessGetListTaskCheckListResultModel(RootModel):
    root: Dict[str, TaskCheckListResult]


class AddChecklistsToTaskModel(StrictBaseModel):
    taskID: int
    id: int


class SuccessAddChecklistsToTaskModel(StrictBaseModel):
    result: List[AddChecklistsToTaskModel]


class SuccessUploadAttachmentsToServerTaskChecklistDataFromFormModel(StrictBaseModel):
    taskID: int
    taskCheckListID: int
    taskCheckListResultID: int
    attachments: List[int]
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class AttributeTypeResultChecklist(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class TaskCheckListResultV2ResultModel(StrictBaseModel):
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


class SuccessGetAttachmentByIdFromTaskChecklist(StrictBaseModel):
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


class SuccessUploadAttachmentsToServerTaskCompletedWorkDataFromFormModel(StrictBaseModel):
    taskID: int
    completedWorkID: int
    attributeID: int
    attachments: List[int]


class UpdateTaskChecklistResultsModel(StrictBaseModel):
    taskID: int
    taskCheckListID: int
    checkListItemID: int


class SuccessUpdateTaskChecklistResultsModel(StrictBaseModel):
    result: List[UpdateTaskChecklistResultsModel]


class CompletedWorkAttributeResult(StrictBaseModel):
    taskID: int
    completedWorkID: int
    attribute: Optional[IdNameDeletedResult] = None
    selectionMode: Optional[IdNameResult] = None
    values: Optional[List[str]] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class SuccessGetListCompletedWorkAttributeResultModel(StrictBaseModel):
    result: List[CompletedWorkAttributeResult]


class ListAttributesTaskCompletedWorksModel(StrictBaseModel):
    taskID: int
    completedWorkID: int
    attributeID: int


class SuccessGetListAttributesTaskCompletedWorksModel(StrictBaseModel):
    results: List[ListAttributesTaskCompletedWorksModel]


class WorkTypeResult(StrictBaseModel):
    id: int
    name: Optional[str] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None


class MaintainedAssetResult(StrictBaseModel):
    deleted: Optional[str] = None
    parentID: Optional[int] = None
    location: Optional[IdResult] = None
    host: Optional[HostAssetResult] = None
    company: Optional[IdNameDeletedResult] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompletedWorkResult(StrictBaseModel):
    id: int
    workType: Optional[WorkTypeResult] = None
    maintainedAsset: Optional[AssetResult] = None
    started: Optional[str] = None
    finished: Optional[str] = None
    notes: Optional[str] = None
    quantity: Optional[float] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    created: Optional[str] = None


class SuccessGetListCompletedWorkResult(StrictBaseModel):
    result: List[CompletedWorkResult]


class AttachmentsTaskCompletedWorksModel(StrictBaseModel):
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


class SuccessGetListAttachmentsTaskCompletedWorksModel(StrictBaseModel):
    result: List[AttachmentsTaskCompletedWorksModel]


class MaterialsTaskComplectedWorkModel(StrictBaseModel):
    taskID: int
    completedWorkID: int
    materialID: int
    warehouseID: int
    inventoryID: int


class SuccessAddMaterialsTaskComplectedWork(StrictBaseModel):
    results: List[MaterialsTaskComplectedWorkModel]


class TechniciansTaskComplectedWorkModel(StrictBaseModel):
    taskID: int
    completedWorkID: int
    userID: int


class SuccessAddTechniciansTaskComplectedWorkModel(StrictBaseModel):
    results: List[TechniciansTaskComplectedWorkModel]


class IdNameErpIDResult(StrictBaseModel):
    erpID: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TakenByUserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class MarkingCodeInfoItemResult(StrictBaseModel):
    code: Optional[str] = None
    scannedAtUtc: Optional[datetime] = None
    receivedAtUtc: datetime
    createdBy: int


class MarkingCodesInfoResult(StrictBaseModel):
    scannedCount: int
    items: Optional[List[MarkingCodeInfoItemResult]] = None


class MaterialResult(StrictBaseModel):
    inventoryID: Optional[int] = None
    materialID: Optional[int] = None
    materialName: Optional[str] = None
    materialErpID: Optional[str] = None
    materialDeleted: Optional[datetime] = None
    materialIsMarkable: bool
    warehouse: Optional[IdNameErpIDResult] = None
    measurementUnit: Optional[IdNameResult] = None
    quantity: Optional[float] = None
    consumed: Optional[datetime] = None
    takenByUser: Optional[TakenByUserResult] = None
    cost: Optional[float] = None
    costCurrencyID: Optional[int] = None
    sortOrder: Optional[int] = None
    markingCodesInfo: Optional[MarkingCodesInfoResult] = None


class SuccessGetListCompletedWorkMaterialResultModel(StrictBaseModel):
    taskID: Optional[int] = None
    completedWorkID: Optional[int] = None
    materials: Optional[List[MaterialResult]] = None


class SuccessGetListRootCompletedWorkMaterialResultModel(RootModel):
    root: Dict[str, SuccessGetListCompletedWorkMaterialResultModel]


class SuccessUploadAttachToReportTaskCompletedWorkModel(StrictBaseModel):
    taskID: int
    attachmentID: int
    md5Hash: str
    fileName: str
    isProtected: bool


class SignatureReportAttachmentModel(StrictBaseModel):
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


class TechnicianResult(StrictBaseModel):
    userID: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    rate: Optional[float] = None
    rateCurrencyID: Optional[int] = None


class CompletedWorkTechnicianResult(StrictBaseModel):
    taskID: int
    completedWorkID: int
    technicians: List[TechnicianResult]


class SuccessGetListCompletedWorkTechnicianResult(RootModel):
    root: Dict[str, CompletedWorkTechnicianResult]


class TaskContactsListResultModel(StrictBaseModel):
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


class SuccessUploadAttachmentsToServerTaskConversationDataFromFormModel(StrictBaseModel):
    taskID: Optional[int] = None
    taskconversationID: int
    attachments: List[int]
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class ConversationDeliveryResult(StrictBaseModel):
    recipient: Optional[UserResult] = None
    delivered: Optional[datetime] = None
    read: Optional[datetime] = None


class SuccessGetListConversationDeliveryResult(StrictBaseModel):
    results: List[ConversationDeliveryResult]


class SuccessGetUsedCompanyCodeInTaskNumberModel(StrictBaseModel):
    result: bool


class LocationShortResult(StrictBaseModel):
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


class ListShortResult(StrictBaseModel):
    number: Optional[str] = None
    notes: Optional[str] = None
    deadline: Optional[datetime] = None
    sortOrder: Optional[int] = None
    criticality: Optional[TaskActualCriticalityResult] = None
    location: Optional[LocationShortResult] = None
    asset: Optional[TaskAssetResult] = None
    timesheet: Optional[TimesheetResult] = None
    escalatedToUserID: Optional[int] = None
    approvalWithUserID: Optional[int] = None
    assignedToUserID: Optional[int] = None
    assignedToUserIDs: Optional[List[int]] = None
    requestedByUserID: Optional[int] = None
    workTypeID: Optional[int] = None
    lastModified: Optional[datetime] = None
    erpID: Optional[str] = None
    id: int


class SuccessListShortResultModel(RootModel):
    root: Dict[str, ListShortResult]


class ListCountResult(StrictBaseModel):
    countWithAssign: Optional[int] = None
    countWithoutAssign: Optional[int] = None
    runtimeMinutes: Optional[int] = None


class SuccessGetListCountResultModel(RootModel):
    root: Dict[str, ListCountResult]


class ClusterResult(StrictBaseModel):
    hash: Optional[str] = None
    center: Optional[str] = None


class TaskGroupByResult(StrictBaseModel):
    tasksCount: Optional[int] = None
    assignedTaskCount: Optional[int] = None
    unasssignedTaskCount: Optional[int] = None
    expiredTaskCount: Optional[int] = None
    groupKey: Optional[ClusterResult] = None


class SuccessGetTaskGroupByResultModel(StrictBaseModel):
    results: List[TaskGroupByResult]


class IdNameErpIDDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    erpID: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskUserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class ListResult(StrictBaseModel):
    material: Optional[IdNameErpIDDeletedResult] = None
    warehouse: Optional[IdNameErpIDResult] = None
    measurementUnit: Optional[IdNameResult] = None
    quantity: Optional[float] = None
    taken: Optional[datetime] = None
    takenByUser: Optional[TaskUserResult] = None
    sortOrder: Optional[int] = None
    id: Optional[int] = None


class SuccessTaskMaterialsModel(RootModel):
    root: Dict[str, ListResult]


class TaskStageComponentResult(StrictBaseModel):
    permission: Optional[str] = None
    capability: Optional[str] = None


class TaskStageAttributeResult(StrictBaseModel):
    permission: Optional[str] = None
    capability: Optional[str] = None
    attribute: Optional[IdNameDeletedResult] = None
    value: Optional[str] = None
    attributeType: Optional[AttributeTypeResult] = None
    measurementUnit: Optional[MeasurementUnitResult] = None
    listOfValues: Optional[Dict[str, str]] = None
    domain: Optional[DomainResult] = None


class TaskFormMetadataResultModel(StrictBaseModel):
    taskStage: Optional[IdNameResult] = None
    taskViewTemplateCode: Optional[str] = None
    components: Optional[Dict[str, TaskStageComponentResult]] = None
    attributes: Optional[Dict[str, TaskStageAttributeResult]] = None


class SuccessGetTaskFormMetadataResultModel(RootModel):
    root: Dict[str, TaskFormMetadataResultModel]


class TechnicianUserResult(StrictBaseModel):
    tenantMemberID: int
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class RatingResultModel(StrictBaseModel):
    technician: Optional[TechnicianUserResult] = None
    ratingCriteria: Optional[IdNameResult] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    isIgnore: Optional[bool] = None
    ignoreReason: Optional[str] = None


class SuccessGetListRatingResultModel(StrictBaseModel):
    results: List[RatingResultModel]


class TaskSkillResultModel(StrictBaseModel):
    name: str
    id: int


class SuccessGetTaskSkillResultModel(RootModel):
    root: Dict[str, TaskSkillResultModel]


class IdNameDescriptionResult(StrictBaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskStageModel(StrictBaseModel):
    taskSnapshotID: int
    color: str
    name: str
    id: int


class TaskChecklistModel(StrictBaseModel):
    id: int
    checkList: IdNameResult


class ModifiedByUserModel(StrictBaseModel):
    id: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None


class ChangeSetModel(StrictBaseModel):
    timeStamp: datetime
    modifiedBy: ModifiedByUserModel
    taskAction: IdNameResult
    assignedTo: Optional[IdNameResult] = None
    taskCheckList: Optional[TaskChecklistModel] = None
    actionLocationState: int


class ListStagingHistoryResultModel(StrictBaseModel):
    taskStageFrom: Optional[TaskStageModel] = None
    taskStageTo: Optional[TaskStageModel] = None
    taskStatus: Optional[IdNameResult] = None
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None
    changeSet: Optional[List[ChangeSetModel]] = None


class SuccessGetListStagingHistoryResultModel(StrictBaseModel):
    results: List[ListStagingHistoryResultModel]


class SuccessGetListTaskTagsModel(StrictBaseModel):
    results: List[str]


class EmploymentResult(StrictBaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
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


class TaskWatchListsListResultModel(StrictBaseModel):
    employments: Optional[List[EmploymentResult]] = None
    isCreator: Optional[bool] = None
    isExecutor: Optional[bool] = None
    hasExternalAccess: Optional[bool] = None
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


class SuccessGetListTaskWatchListsListResultModel(StrictBaseModel):
    results: List[TaskWatchListsListResultModel]


class NextStageModel(StrictBaseModel):
    nextStage: IdNameColorResult
    linkName: str
    sortOrder: int


class ListStagesNextResult(StrictBaseModel):
    taskTypeID: int
    currentStage: IdNameColorResult
    nextStages: List[NextStageModel]
    tasks: List[int]
    error: str


class SuccessGetListStagesNextModel(StrictBaseModel):
    results: List[ListStagesNextResult]
