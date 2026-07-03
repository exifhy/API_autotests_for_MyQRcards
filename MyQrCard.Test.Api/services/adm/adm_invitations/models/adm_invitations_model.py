from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdNameModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameDescriptionResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None


class BanResult(StrictBaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[IdNameDescriptionResult] = None


class TenantMemberResult(StrictBaseModel):
    id: Optional[int] = None
    accountID: Optional[int] = None
    description: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None


class TenantsListResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    uriName: Optional[str] = None
    fullName: Optional[str] = None
    banned: Optional[BanResult] = None
    owner: Optional[TenantMemberResult] = None
    tenantMembers: Optional[List[TenantMemberResult]] = None
    isCurrent: Optional[bool] = None


class InvitationsGetResultModel(StrictBaseModel):
    id: str
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    allowSelfRegistration: Optional[bool] = None
    requiredSelfRegistration: Optional[bool] = None
    validFrom: Optional[datetime] = None
    validTill: Optional[datetime] = None
    tenant: Optional[TenantsListResult] = None
    allowRegisterWithoutVerification: Optional[bool] = None
    pinCode: Optional[str] = None
    isForSupport: Optional[bool] = None
    userTemplate: Optional[IdNameDescriptionResult] = None


class InvitationsGetShortResultModel(StrictBaseModel):
    id: str
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    allowSelfRegistration: Optional[bool] = None
    requiredSelfRegistration: Optional[bool] = None
    validFrom: Optional[datetime] = None
    validTill: Optional[datetime] = None
    tenant: Optional[TenantsListResult] = None
    allowRegisterWithoutVerification: Optional[bool] = None


class InvitationProjectionModel(StrictBaseModel):
    tenantID: Optional[int] = None
    invitationID: Optional[int] = None
    description: Optional[str] = None
    userTemplateID: Optional[int] = None
    isPublic: Optional[bool] = None
    allowSelfRegistration: Optional[bool] = None
    requiredSelfRegistration: Optional[bool] = None
    validFrom: Optional[datetime] = None
    validTill: Optional[datetime] = None
    deleted: Optional[datetime] = None
    tenantUriName: Optional[str] = None
    tenantName: Optional[str] = None
    tenantFullName: Optional[str] = None
    tenantIsTemplate: Optional[bool] = None
    tenantBanTill: Optional[datetime] = None
    allowRegisterWithoutVerification: Optional[bool] = None
    pinCode: Optional[str] = None
    isForSupport: Optional[bool] = None
    powerTenantMemberID: Optional[int] = None
    userTemplateName: Optional[str] = None
    userTemplateDescription: Optional[str] = None
    userTemplate: Optional[IdNameModel] = None


class SuccessGetListInvitationProjectionModel(RootModel):
    root: Dict[str, InvitationsGetResultModel]


class InvitationsAddResultModel(StrictBaseModel):
    id: str
    tenantID: int


class SuccessAddListInvitationsAddResultModel(StrictBaseModel):
    results: List[InvitationsAddResultModel]
