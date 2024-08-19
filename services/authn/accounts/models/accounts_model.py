from pydantic import BaseModel
from typing import List, Optional


class TenantAuthorizationProjectionModel(BaseModel):
    accountID: Optional[int] = None
    userID: Optional[int] = None
    tenantMemberID: Optional[int] = None
    tenantMemberDescription: Optional[str] = None
    tenantMemberValidTill: Optional[str] = None
    userBanTill: Optional[str] = None
    isUserBanned: Optional[bool] = None
    userBanReasonID: Optional[int] = None
    userBanReasonCode: Optional[str] = None
    email: Optional[str] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    hasUserProfile: Optional[bool] = None
    tenantID: Optional[int] = None
    uriName: Optional[str] = None
    name: Optional[str] = None
    fullName: Optional[str] = None
    banTill: Optional[str] = None
    banReasonID: Optional[int] = None
    banReasonCode: Optional[str] = None
    isTenantArchived: Optional[bool] = None
    isTenantDeleted: Optional[bool] = None


class TenantCreationRequestEntityModel(BaseModel):
    id: Optional[str] = None
    accountID: Optional[int] = None
    tenantID: Optional[int] = None
    tenantName: Optional[str] = None
    tenantFullName: Optional[str] = None
    tenantUriName: Optional[str] = None
    ownerFirstName: Optional[str] = None
    ownerLastName: Optional[str] = None
    ownerMiddleName: Optional[str] = None
    templateID: Optional[int] = None
    isSuccess: Optional[bool] = None
    message: Optional[str] = None
    licenseID: Optional[int] = None
    created: Optional[str] = None
    processed: Optional[str] = None
    approved: Optional[str] = None
    rejected: Optional[str] = None
    rejectionReason: Optional[str] = None


class SuccessUserAccountAuthenticationModel(BaseModel):
    tenantEntities: List[TenantAuthorizationProjectionModel]
    requests: List[TenantCreationRequestEntityModel]
    accountHasUserProfile: Optional[bool] = None
    isCrossTenantAdmin: Optional[bool] = None
    isAnonymous: Optional[bool] = None
    jwtValidTill: Optional[str] = None
    accountUserTypeID: Optional[int] = None
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]

