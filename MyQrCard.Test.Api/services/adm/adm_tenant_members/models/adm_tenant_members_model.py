from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, RootModel
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdNameDescriptionResult(StrictBaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class BanResult(StrictBaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[IdNameDescriptionResult] = None


class AccountResult(StrictBaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    login: Optional[str] = None
    ban: Optional[BanResult] = None


class UserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    ban: Optional[BanResult] = None


class TokenResult(StrictBaseModel):
    created: Optional[datetime] = None
    validTill: Optional[datetime] = None


class TenantMemberTokensResult(StrictBaseModel):
    refreshToken: Optional[TokenResult] = None
    oneTimeLoginToken: Optional[TokenResult] = None
    serviceToken: Optional[TokenResult] = None


class SuccessTenantMembersListResultModel(StrictBaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    validTill: Optional[datetime] = None
    account: Optional[AccountResult] = None
    user: Optional[UserResult] = None
    tokens: Optional[TenantMemberTokensResult] = None


class TenantMembersListResponseModel(RootModel):
    root: Dict[str, SuccessTenantMembersListResultModel]


class TenantMembersGetResultModel(StrictBaseModel):
    id: int
    accountID: int
    userID: int
    validTill: Optional[datetime] = None
    description: Optional[str] = None


class AddTenantMemberResponseModel(StrictBaseModel):
    results: List[int]
