from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime


class IdNameResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class ClientResult(BaseModel):
    id: Optional[int] = None
    uniqueClientIdentifier: Optional[str] = None
    agent: Optional[str] = None
    clientType: Optional[IdNameResult] = None


class ApplicationResult(BaseModel):
    version: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class ApplicationListResult(BaseModel):
    client: Optional[ClientResult] = None
    application: Optional[ApplicationResult] = None
    pushToken: Optional[str] = None
    timestamp: Optional[datetime] = None


class SuccessGetApplicationListResultModel(BaseModel):
    result: List[ApplicationListResult]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAccountAddResultEntityModel(BaseModel):
    isPasswordDefined: Optional[bool] = None
    isNewAccount: Optional[bool] = None
    id: Optional[int] = None
    verificationRequestValidTill: Optional[datetime] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None


class BanResult(BaseModel):
    dateTill: Optional[str] = None
    banReason: Optional[IdNameResult] = None


class SocialProfileResult(BaseModel):
    dateFrom: Optional[str] = None
    dateTill: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessAccountsGetResultModel(BaseModel):
    id: Optional[int] = None
    credential: Optional[str] = None
    ban: Optional[BanResult] = None
    isAnonymous: Optional[bool] = None
    isCrossTenantAdmin: Optional[bool] = None
    domainLogin: Optional[str] = None
    socialProfiles: Optional[List[SocialProfileResult]] = None


class NotificationListResult(BaseModel):
    notificationID: Optional[int] = None
    providerID: Optional[int] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    created: Optional[datetime] = None
    sent: Optional[datetime] = None


class SuccessNotificationListResultModel(BaseModel):
    result: Optional[List[NotificationListResult]] = None

