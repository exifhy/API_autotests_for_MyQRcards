from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ListTaskTypesModel(BaseModel):
    name: Optional[str] = None
    numberMask: Optional[str] = None
    closeMinutes: Optional[int] = None


class SuccessGetListTaskTypesModel(RootModel):
    root: Dict[str, ListTaskTypesModel]


class IdNameDeletedResult(BaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetRouteResultModel(BaseModel):
    startTaskStage: Optional[IdNameDeletedResult] = None
    finishTaskStage: Optional[IdNameDeletedResult] = None
    startTaskStatus: Optional[IdNameDeletedResult] = None
