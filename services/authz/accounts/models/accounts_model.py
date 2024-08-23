from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class IdNameResultModel(BaseModel):
    name: str
    id: int


class UserProfileResultModel(BaseModel):
    userID: int
    firstName: str
    lastName: str
    middleName: str
    email: str
    mobilePhone: str
    workPhone: str
    otherPhone: str
    avatarUrl: str
    geoTrackingMode: IdNameResultModel


class RefreshTokenModel(BaseModel):
    jwtValidTill: datetime
    access_token: str
    refresh_token: str
    expires_in: int


class TenantModel(BaseModel):
    fullName: str
    uriName: str
    name: str
    id: int


class TenantMemberModel(BaseModel):
    description: str
    userID: int
    accountID: int
    id: int


class LicenseModel(BaseModel):
    name: str
    code: str
    id: int


class TenantLicenseModel(BaseModel):
    license: LicenseModel
    dateTill: datetime
    isTrialPeriod: bool
    dateFrom: datetime
    trialPeriodDays: Optional[int] = None


class SuccessAuthorizationModel(BaseModel):
    profile: Optional[UserProfileResultModel] = None
    permissions: Dict[str, str]
    refreshToken: Optional[RefreshTokenModel] = None
    tenant: Optional[TenantModel] = None
    tenantMember: Optional[TenantMemberModel] = None
    tenantLicenses: List[TenantLicenseModel]
    featureFlags: List[str]
    jwtValidTill: datetime
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
