from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, RootModel
from datetime import datetime


class SuccessUserModel(BaseModel):
    tenantID: Optional[int] = None
    tenantMemberID: Optional[int] = None
    userID: Optional[int] = None
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    id: Optional[int] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    verificationRequestValidTill: Optional[datetime] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class BanReason(BaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class Ban(BaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[BanReason] = None


class TimeZone(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class Location(BaseModel):
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    coordinate: Optional[str] = None
    timeZone: Optional[TimeZone] = None


class ActualLocation(BaseModel):
    actuality: Optional[datetime] = None
    coordinate: Optional[str] = None
    timeZone: Optional[TimeZone] = None


class Mobility(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class GeoTrackingMode(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class TeamLeader(BaseModel):
    leadID: Optional[int] = None
    leadFirstName: Optional[str] = None
    leadMiddleName: Optional[str] = None
    leadLastName: Optional[str] = None


class Rating(BaseModel):
    total: Optional[float] = None
    totalTrendDirection: Optional[float] = None
    timestamp: Optional[datetime] = None


class RateCurrency(BaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class SuccessGetDetailedInfoUserModel(BaseModel):
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


class OrgUnitResult(BaseModel):
    parentID: Optional[int] = None
    name: Optional[str] = None
    id: Optional[int] = None


class CompanyResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class EmploymentResult(BaseModel):
    orgUnit: Optional[OrgUnitResult] = None
    company: Optional[CompanyResult] = None
    position: Optional[str] = None
    scheduleRuleID: Optional[int] = None


class DistrictResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class UserTaskActualityResult(BaseModel):
    requested: Optional[int] = None
    assigned: Optional[int] = None


class UserRelevance(BaseModel):
    workType: Optional[int] = None
    onShift: Optional[int] = None
    responsibility: Optional[int] = None
    district: Optional[int] = None
    skill: Optional[int] = None


class CurrencyResult(BaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class UserResult(BaseModel):
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


class SuccessCreatedApiUserModel(BaseModel):
    userID: int
    tenantMemberID: int


class IdNameResult(BaseModel):
    name: str
    id: int


class SuccessGetUsersRolesModel(RootModel):
    root: Optional[Dict[str, List[IdNameResult]]] = None


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


class AssetListQueryResultModel(RootModel):
    root: Dict[str, AssetListQueryResult]

