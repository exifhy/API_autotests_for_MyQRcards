from typing import Optional, Dict, List, Any
from pydantic import BaseModel, RootModel, ConfigDict, Field
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SuccessUserModel(StrictBaseModel):
    tenantID: Optional[int] = None
    tenantMemberID: Optional[int] = None
    userID: Optional[int] = None
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    id: Optional[int] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    verificationRequestValidTill: Optional[datetime] = None


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class BanReason(StrictBaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class Ban(StrictBaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[BanReason] = None


class TimeZone(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class Location(StrictBaseModel):
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    coordinate: Optional[str] = None
    timeZone: Optional[TimeZone] = None


class ActualLocation(StrictBaseModel):
    actuality: Optional[datetime] = None
    coordinate: Optional[str] = None
    timeZone: Optional[TimeZone] = None


class Mobility(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class GeoTrackingMode(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class TeamLeader(StrictBaseModel):
    leadID: Optional[int] = None
    leadFirstName: Optional[str] = None
    leadMiddleName: Optional[str] = None
    leadLastName: Optional[str] = None


class Rating(StrictBaseModel):
    total: Optional[float] = None
    totalTrendDirection: Optional[float] = None
    timestamp: Optional[datetime] = None


class RateCurrency(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class SuccessGetDetailedInfoUserModel(StrictBaseModel):
    ban: Optional[Ban] = None
    defaultLocation: Optional[Location] = None
    actualLocation: Optional[ActualLocation] = None
    mobility: Optional[Mobility] = None
    geoTrackingMode: Optional[GeoTrackingMode] = None
    teamUserID: Optional[int] = None
    teamLeader: Optional[TeamLeader] = None
    rating: Optional[Rating] = None
    flags: Optional[Dict[str, bool]] = None
    sex: Optional[Mobility] = None  # Используем ту же модель, что и Mobility
    lastSeen: Optional[datetime] = None
    rate: Optional[float] = None
    rateCurrency: Optional[RateCurrency] = None
    accountDomainLogin: Optional[str] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    isTechnician: Optional[bool] = None
    isTeam: Optional[bool] = None
    isCustomer: Optional[bool] = None
    avatarUrl: Optional[str] = None


class OrgUnitResult(StrictBaseModel):
    parentID: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompanyResult(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class EmploymentResult(StrictBaseModel):
    orgUnit: Optional[OrgUnitResult] = None
    company: Optional[CompanyResult] = None
    position: Optional[str] = None
    scheduleRuleID: Optional[int] = None


class DistrictResult(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class UserTaskActualityResult(StrictBaseModel):
    requested: Optional[int] = None
    assigned: Optional[int] = None


class UserRelevance(StrictBaseModel):
    workType: Optional[int] = None
    onShift: Optional[int] = None
    responsibility: Optional[int] = None
    district: Optional[int] = None
    skill: Optional[int] = None


class CurrencyResult(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class UserResult(StrictBaseModel):
    banTill: Optional[str] = None
    coordinate: Optional[str] = None
    locationActuality: Optional[str] = None
    employments: Optional[List[EmploymentResult]] = None
    districts: Optional[List[DistrictResult]] = None
    taskActualities: Optional[Dict[str, UserTaskActualityResult]] = None
    totalRating: Optional[float] = None
    relevance: Optional[UserRelevance] = None
    userID: Optional[int] = None
    deleted: Optional[str] = None
    sortOrder: Optional[int] = None
    lastSeen: Optional[str] = None
    rate: Optional[float] = None
    rateCurrency: Optional[CurrencyResult] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    isTechnician: Optional[bool] = None
    isTeam: Optional[bool] = None
    isCustomer: Optional[bool] = None
    avatarUrl: Optional[str] = None


class SuccessGetUsersListModel(RootModel):
    root: Optional[Dict[str, UserResult]] = None


class SuccessCreatedApiUserModel(StrictBaseModel):
    userID: int
    tenantMemberID: int


class IdNameResult(StrictBaseModel):
    name: str
    id: int


class IdNameResultDistrictsModel(StrictBaseModel):
    name: str
    id: Optional[int] = None


class SuccessGetUsersRolesModel(RootModel):
    root: Dict[str, List[IdNameResult]]


class SuccessGetUsersDistrictsModel(RootModel):
    root: Dict[str, IdNameResultDistrictsModel]


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


class RangeData(StrictBaseModel):
    offset: Optional[int] = None
    fetch: Optional[int] = None


class SortData(StrictBaseModel):
    orderBy: Optional[int] = None
    direction: Optional[int] = None
    # direction: Optional[Literal["Ascending", "Descending"]] = None


class AssetListQueryResult(StrictBaseModel):
    name: Optional[str] = None
    filter: Optional[AssetFilterData] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    sort: Optional[SortData] = None
    queryString: Optional[str] = None


class AssetListQueryResultModel(RootModel):
    root: Dict[str, AssetListQueryResult]


class ProviderResult(StrictBaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    name: Optional[str] = None
    isOn: Optional[bool] = None
    isAvailableForUser: Optional[bool] = None


class UserDisabledNotificationsListResult(StrictBaseModel):
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    providers: Optional[List[ProviderResult]] = None


class IdNameDeletedResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[datetime] = None


class AssetResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    host: Optional[IdNameDeletedResult] = None
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None


class PeriodResultModel(StrictBaseModel):
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[datetime] = None


class AssetAssignmentResult(StrictBaseModel):
    asset: Optional[AssetResult] = None
    validityPeriod: Optional[PeriodResultModel] = None
    notes: Optional[str] = None


class AssetAssignmentListResponse(StrictBaseModel):
    results: List[AssetAssignmentResult]


class AssetFilterDataModel(StrictBaseModel):
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
    validityPeriod: Optional[PeriodResultModel] = None
    creationPeriod: Optional[PeriodResultModel] = None
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
    dateRangePeriod: Optional[PeriodResultModel] = None
    attributeValues: Optional[dict] = None
    eventTransportTypes: Optional[List[int]] = None
    materials: Optional[List[int]] = None
    warehouses: Optional[List[int]] = None
    assetFlags: Optional[AssetFlagFilter] = None
    assetText: Optional[AssetTextFilter] = None
    warrantyPeriod: Optional[PeriodResultModel] = None
    responsiblePersons: Optional[List[int]] = None


class AssetListQueryResponseModel(StrictBaseModel):
    name: Optional[str] = None
    filter: Optional[AssetFilterDataModel] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    queryString: Optional[str] = None
    sort: Optional[SortData] = None


class AssetListQueryResponseRootModel(RootModel):
    root: Dict[str, AssetListQueryResponseModel]


class EmploymentShortResult(StrictBaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    scheduleRuleID: Optional[int] = None


class UserShortResult(StrictBaseModel):
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    isTechnician: bool
    isTeam: bool
    isCustomer: bool
    avatarUrl: Optional[str] = None
    userID: int
    employments: Optional[List[EmploymentShortResult]] = None
    deleted: Optional[datetime] = None
    sortOrder: int
    lastSeen: Optional[datetime] = None
    rate: Optional[float] = None
    rateCurrency: Optional[CurrencyResult] = None


class UserShortResultResponseModel(RootModel):
    root: Dict[str, UserShortResult]


class UserRelevanceModel(StrictBaseModel):
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    isTechnician: bool
    isTeam: bool
    isCustomer: bool
    avatarUrl: Optional[str] = None
    userID: int
    employments: Optional[List[EmploymentResult]] = None
    deleted: Optional[datetime] = None
    sortOrder: int
    lastSeen: Optional[datetime] = None
    rate: Optional[float] = None
    rateCurrency: Optional[CurrencyResult] = None
    banTill: Optional[datetime] = None
    coordinate: Optional[str] = None
    locationActuality: Optional[datetime] = None
    districts: Optional[List[IdNameResult]] = None
    taskActualities: Optional[Dict[str, UserTaskActualityResult]] = None
    totalRating: Optional[float] = None
    relevance: UserRelevance


class UserRelevanceResponseModel(RootModel):
    root: Dict[str, UserRelevanceModel]


class EmploymentUserProfileResult(StrictBaseModel):
    company: Optional[IdNameResult] = None
    position: Optional[str] = None
    scheduleRuleID: Optional[int] = None
    orgUnit: Optional[OrgUnitResult] = None
    dateFrom: datetime
    dateTill: datetime


class UserProfileResult(StrictBaseModel):
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    workPhone: Optional[str] = None
    otherPhone: Optional[str] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    isTechnician: bool
    isTeam: bool
    isCustomer: bool
    avatarUrl: Optional[str] = None
    userID: int
    isDelegationOn: bool
    sex: Optional[IdNameResult] = None
    employments: Optional[List[EmploymentUserProfileResult]] = None
    averageRating: Optional[float] = None
    geoTrackingMode: Optional[IdNameResult] = None


class UserAddByIntegrationModel(StrictBaseModel):
    tenantID: int
    tenantMemberID: int
    userID: int
    roleIDs: List[int]


class UserPermissionUiModel(StrictBaseModel):
    results: Dict[str, str]


class UserPermissionExtModel(StrictBaseModel):
    results: Dict[str, str]


class UserAvatarUploadModel(StrictBaseModel):
    attachmentID: int
    publicUrl: str
    size: int


class MarkRatingResult(StrictBaseModel):
    markNumber: Optional[int] = None
    countOfTotal: Optional[float] = None
    direction: Optional[int] = None


class RatingListResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    averageRating: Optional[float] = None
    rating: Optional[List[MarkRatingResult]] = None


class RatingTechnicianResultModel(StrictBaseModel):
    technicianID: int
    averageRating: Optional[float] = None
    maxMark: Optional[int] = None
    ratingCriterias: Optional[List[RatingListResult]] = None


class UserRegistrationWithInvitationResponseModel(StrictBaseModel):
    accountID: int
    tenantID: int
    userID: int
    verificationCodeRepeatTimeout: Optional[int] = None


class UserRegistrationVerifyResponseModel(StrictBaseModel):
    accountID: int
    tenantID: int
    userID: Optional[int] = None
    verificationCodeRepeatTimeout: Optional[int] = None


class UserSkillsModel(StrictBaseModel):
    id: int
    name: str
    dateFrom: Optional[datetime] = None
    dateTill: Optional[datetime] = None


class UserSkillsResponseModel(RootModel):
    root: Dict[str, UserSkillsModel]


class UserTagsResponseModel(StrictBaseModel):
    results: List[str]


class TaskFlagFilter(StrictBaseModel):
    hasAssigneeCheckedIn: Optional[bool] = None
    isClosed: Optional[bool] = None
    isFavourite: Optional[bool] = None
    isCompleted: Optional[bool] = None
    isAssigned: Optional[bool] = None
    isOutdated: Optional[bool] = None
    isRated: Optional[bool] = None
    isScheduled: Optional[bool] = None
    topLevelTasksForHierarchy: Optional[bool] = None


class TaskFilterData(StrictBaseModel):
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
    validityPeriod: Optional[PeriodResultModel] = None
    creationPeriod: Optional[PeriodResultModel] = None
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
    dateRangePeriod: Optional[PeriodResultModel] = None
    attributeValues: Optional[Dict[str, Any]] = None
    eventTransportTypes: Optional[List[int]] = None
    materials: Optional[List[int]] = None
    warehouses: Optional[List[int]] = None
    requestedBy: Optional[List[int]] = None
    assignedTo: Optional[List[int]] = None
    approvalWith: Optional[List[int]] = None
    escalatedTo: Optional[List[int]] = None
    assetResponsiblePersons: Optional[List[int]] = None
    taskStatuses: Optional[List[int]] = None
    taskStages: Optional[List[int]] = None
    taskFlags: Optional[TaskFlagFilter] = None
    assignationPeriod: Optional[PeriodResultModel] = None
    completionPeriod: Optional[PeriodResultModel] = None
    closingPeriod: Optional[PeriodResultModel] = None
    deadlinePeriod: Optional[PeriodResultModel] = None
    taskNumbers: Optional[List[str]] = None
    ratingCriterias: Optional[List[int]] = None
    taskTemplates: Optional[List[str]] = None
    requestMethods: Optional[List[int]] = None
    branches: Optional[List[int]] = None
    assetSchemas: Optional[List[int]] = None
    lastModifiedPeriod: Optional[PeriodResultModel] = None
    completedWorks: Optional[List[int]] = None
    payeeCompanies: Optional[List[int]] = None
    tabs: Optional[List[str]] = None
    sections: Optional[List[str]] = None


class TaskListQueryResult(StrictBaseModel):
    name: Optional[str] = None
    filter: Optional[TaskFilterData] = None
    searchText: Optional[str] = None
    range: Optional[RangeData] = None
    queryString: Optional[str] = None
    isUserQuery: bool
    sort: Optional[SortData] = None


class UserTaskListQueryResponse(RootModel):
    root: Dict[str, TaskListQueryResult]


class IdNameErpIdModel(StrictBaseModel):
    id: int
    name: str
    erpID: str


class UsersWarehousesResponseModel(StrictBaseModel):
    results: List[IdNameErpIdModel]
