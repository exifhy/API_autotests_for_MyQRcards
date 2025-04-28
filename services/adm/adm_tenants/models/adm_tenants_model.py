from pydantic import BaseModel, ConfigDict, RootModel
from typing import List, Optional, Dict
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    results: List[CodeMessageModel]


class BanReasonResult(StrictBaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class BanResult(StrictBaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[BanReasonResult] = None


class TenantMemberResult(StrictBaseModel):
    accountID: Optional[int] = None
    description: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    id: Optional[int] = None


class TenantOwnerResult(StrictBaseModel):
    tenantMemberID: int
    userID: int
    accountID: int
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    email: Optional[str] = None


class SuccessGetCurrentTenantResult(StrictBaseModel):
    banned: Optional[BanResult] = None
    owner: Optional[TenantMemberResult] = None
    tenantMembers: Optional[List[TenantMemberResult]] = None
    isCurrent: Optional[bool] = None
    uriName: Optional[str] = None
    fullName: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetCurrentOwnerTenantResult(StrictBaseModel):
    banned: Optional[BanResult] = None
    owner: Optional[TenantOwnerResult] = None
    paymentInfo: Optional[Dict] = None
    isCurrent: Optional[bool] = None
    uriName: Optional[str] = None
    fullName: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetListTenantsResultModel(StrictBaseModel):
    result: List[SuccessGetCurrentTenantResult]


class IdNameDescriptionResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None


class TenantsListResult(StrictBaseModel):
    id: int
    name: str
    uriName: str
    fullName: Optional[str] = None
    banned: Optional[BanResult] = None
    owner: TenantMemberResult
    tenantMembers: Optional[List[TenantMemberResult]] = None
    isCurrent: Optional[bool] = None


class SuccessGetListTenantsListResult(StrictBaseModel):
    results: List[TenantsListResult]


class ITenantEntityModel(StrictBaseModel):
    modified: Optional[datetime] = None
    modifiedBy: Optional[int] = None
    deleted: Optional[datetime] = None
    deletedBy: Optional[int] = None
    id: int
    uriName: Optional[str] = None
    name: str
    fullName: Optional[str] = None
    powerTenantMemberID: Optional[int] = None
    isTemplate: Optional[bool] = None
    banTill: Optional[datetime] = None
    banReasonID: Optional[int] = None
    created: Optional[datetime] = None


class SuccessGetListTemplatesITenantEntityModel(StrictBaseModel):
    results: List[ITenantEntityModel]


class SuccessGetListFeatureFlagsForTenantModel(StrictBaseModel):
    results: List[str]


class IdNameResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class LicenseResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None


class TotalCountTenantLicenseResult(StrictBaseModel):
    techniciansCount: Optional[int] = None
    companiesCount: Optional[int] = None
    publicTaskTemplatesCount: Optional[int] = None


class TenantLicenseResultModel(StrictBaseModel):
    license: LicenseResult
    type: Optional[IdNameResult] = None
    dateTill: Optional[datetime] = None
    dateFrom: Optional[datetime] = None
    trialPeriodDays: Optional[int] = None
    remainig: Optional[TotalCountTenantLicenseResult] = None
    total: Optional[TotalCountTenantLicenseResult] = None
    status: IdNameResult


class SuccessGetListTenantLicenseResultModel(StrictBaseModel):
    results: List[TenantLicenseResultModel]


class PackageResult(StrictBaseModel):
    id: str
    name: str
    version: str
    iconUrl: str
    isAddAuthorizeParameters: Optional[bool] = None


class TenantPackagesListResult(StrictBaseModel):
    resource: IdNameResult
    package: PackageResult


class SuccessGetTenantPackagesListResultModel(StrictBaseModel):
    results: List[TenantPackagesListResult]


class TenantVariablesResultModel(StrictBaseModel):
    value: str
    description: str


class SuccessGetListTenantVariablesResultModel(RootModel):
    root: Dict[str, TenantVariablesResultModel]
