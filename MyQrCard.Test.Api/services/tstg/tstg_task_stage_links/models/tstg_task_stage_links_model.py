from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class IdNameResult(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class IdNameDescriptionResult(BaseModel):
    description: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None


class TaskStageLinksListResult(BaseModel):
    taskTypeID: Optional[int] = None
    fromTaskStage: Optional[IdNameResult] = None
    toTaskStage: Optional[IdNameResult] = None
    taskStatus: Optional[IdNameResult] = None
    branch: Optional[IdNameResult] = None
    name: Optional[str] = None
    description: Optional[str] = None
    isPositiveResult: Optional[bool] = None
    permissionUiID: Optional[int] = None
    sortOrder: Optional[int] = None
    timeoutSeconds: Optional[int] = None
    timeoutToDeadlineSeconds: Optional[int] = None
    roles: Optional[List[IdNameDescriptionResult]] = None


class SuccessGetListTaskStageLinksModel(BaseModel):
    links: List[TaskStageLinksListResult]
