from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel
from datetime import datetime


class ScheduleAppointmentBaseResult(BaseModel):
    nextID: Optional[int] = None
    next: Optional[str] = None


class IdNameResult1(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class ListSchedulesResult(BaseModel):
    isActive: Optional[bool] = None
    appointment: Optional[ScheduleAppointmentBaseResult] = None
    id: Optional[int] = None
    frequencyType: Optional[IdNameResult1] = None


class IdNameDeletedResult1(BaseModel):
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class IdResult1(BaseModel):
    id: Optional[int] = None


class HostAssetResult(BaseModel):
    location: Optional[IdResult1] = None
    deleted: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class AssetResult(BaseModel):
    deleted: Optional[str] = None
    parentID: Optional[int] = None
    location: Optional[IdResult1] = None
    host: Optional[HostAssetResult] = None
    company: Optional[IdNameDeletedResult1] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TimeZoneResult(BaseModel):
    utcOffsetMinutes: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None


class CountryResult(BaseModel):
    id: Optional[int] = None
    twoSymbolCode: Optional[str] = None
    name: Optional[str] = None


class LocationResult(BaseModel):
    timeZone: Optional[TimeZoneResult] = None
    country: Optional[CountryResult] = None
    deleted: Optional[str] = None
    address: Optional[str] = None
    coordinate: Optional[str] = None
    description: Optional[str] = None
    id: Optional[int] = None


class ContractResult(BaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    date: Optional[str] = None
    dateTill: Optional[str] = None
    deleted: Optional[str] = None
    name: Optional[str] = None


class TaskTemplatesListResult(BaseModel):
    schedule: Optional[ListSchedulesResult] = None
    sortOrder: Optional[int] = None
    assetCount: Optional[int] = None
    id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[str] = None
    isVisible: Optional[bool] = None
    published: Optional[str] = None
    notes: Optional[str] = None
    taskType: Optional[IdNameDeletedResult1] = None
    asset: Optional[AssetResult] = None
    location: Optional[LocationResult] = None
    workType: Optional[IdNameDeletedResult1] = None
    criticality: Optional[IdNameDeletedResult1] = None
    contract: Optional[ContractResult] = None
    serviceLevelAgreement: Optional[IdNameDeletedResult1] = None
    allowCreateTask: Optional[bool] = None


class SuccessGetTaskTemplatesModel(RootModel):
    """Main class GET"""
    root: Optional[Dict[str, TaskTemplatesListResult]] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddTaskTemplatesModel(BaseModel):
    templates: List[str]


class TaskTemplateAssignmentMergeModel(BaseModel):
    tenantID: int
    taskTemplateID: str
    userID: int
    error: Optional[str] = None


class SuccessTaskTemplateAssignmentMergeModel(BaseModel):
    task: List[TaskTemplateAssignmentMergeModel]


class SuccessActivateTaskTemplatesSchedulesModel(BaseModel):
    isActive: Optional[bool] = None
    nextAppointment: Optional[datetime] = None
