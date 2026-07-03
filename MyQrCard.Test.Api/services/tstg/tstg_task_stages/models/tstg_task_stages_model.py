from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class IdNameResultByte(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameResultInt(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class TaskStagesListResult(BaseModel):
    color: Optional[str] = None
    messageTriggerCount: Optional[int] = None
    taskViewTemplate: Optional[IdNameResultByte] = None
    action: Optional[IdNameResultByte] = None
    assigneeSelectionRule: Optional[IdNameResultByte] = None
    assignToUser: Optional[IdNameResultInt] = None
    assignToRole: Optional[IdNameResultInt] = None
    isShowTechnicianOnMap: Optional[bool] = None
    deleted: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetListTaskStagesResultModel(RootModel):
    root: Dict[str, TaskStagesListResult]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
