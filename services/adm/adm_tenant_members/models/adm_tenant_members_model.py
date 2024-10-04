from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime


class CodeMessageModel(BaseModel):
    traceIdentifier: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class IdNameDescriptionResult(BaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class BanResult(BaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[IdNameDescriptionResult] = None


class AccountResult(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    login: Optional[str] = None
    ban: Optional[BanResult] = None


class UserResult(BaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None
    ban: Optional[BanResult] = None


class TokenResult(BaseModel):
    created: Optional[datetime] = None
    validTill: Optional[datetime] = None


class TenantMemberTokensResult(BaseModel):
    refreshToken: Optional[TokenResult] = None
    oneTimeLoginToken: Optional[TokenResult] = None
    serviceToken: Optional[TokenResult] = None


class SuccessTenantMembersListResultModel(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    validTill: Optional[datetime] = None
    account: Optional[AccountResult] = None
    user: Optional[UserResult] = None
    tokens: Optional[TenantMemberTokensResult] = None
