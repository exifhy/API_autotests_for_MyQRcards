from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ScheduledAppointmentResult(BaseModel):
    notes: Optional[str] = None
    isContinuedOnTheNextDay: Optional[bool] = None
    from_: Optional[str] = None
    till: Optional[str] = None


class UserResult(BaseModel):
    tenantMemberID: Optional[int] = None
    coordinate: Optional[str] = None
    email: Optional[str] = None
    mobilePhone: Optional[str] = None
    otherPhone: Optional[str] = None
    workPhone: Optional[str] = None
    isTechnician: Optional[bool] = None
    isCustomer: Optional[bool] = None
    isEmailVerified: Optional[bool] = None
    isMobilePhoneVerified: Optional[bool] = None
    coordinateActuality: Optional[str] = None
    distance: Optional[int] = None
    rate: Optional[float] = None
    rateCurrencyID: Optional[int] = None
    appointments: Optional[List[ScheduledAppointmentResult]] = None
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[str] = None


class AttachmentBaseResult(BaseModel):
    id: Optional[int] = None
    fileName: Optional[str] = None
    publicUrl: Optional[str] = None
    thumbnailUrl: Optional[str] = None


class IdNameDeletedResult(BaseModel):
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class AssetResult(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[str] = None
    host: Optional[IdNameDeletedResult] = None


class TaskResult(BaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    notes: Optional[str] = None
    unreadMessagesCount: Optional[int] = None


class TaskMessageModel(BaseModel):
    id: Optional[int] = None
    created: Optional[str] = None
    message: Optional[str] = None
    isExternal: Optional[bool] = None
    author: Optional[UserResult] = None
    attachment: Optional[List[AttachmentBaseResult]] = None
    asset: Optional[AssetResult] = None
    task: Optional[TaskResult] = None


class SuccessGetListTaskMessageModel(BaseModel):
    result: List[TaskMessageModel]
