from pydantic import BaseModel, ConfigDict
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


class SuccessGetCurrentTenantResult(StrictBaseModel):
    banned: Optional[BanResult] = None
    owner: Optional[TenantMemberResult] = None
    tenantMembers: Optional[List[TenantMemberResult]] = None
    isCurrent: Optional[bool] = None
    uriName: Optional[str] = None
    fullName: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetListTenantsResultModel(StrictBaseModel):
    result: List[SuccessGetCurrentTenantResult]
