from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BanReasonResult(BaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class BanResult(BaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[BanReasonResult] = None


class TenantMemberResult(BaseModel):
    accountID: Optional[int] = None
    description: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    id: Optional[int] = None


class SuccessGetCurrentTenantResult(BaseModel):
    banned: Optional[BanResult] = None
    owner: Optional[TenantMemberResult] = None
    tenantMembers: Optional[List[TenantMemberResult]] = None
    isCurrent: Optional[bool] = None
    uriName: Optional[str] = None
    fullName: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetListTenantsResultModel(BaseModel):
    result: List[SuccessGetCurrentTenantResult]
