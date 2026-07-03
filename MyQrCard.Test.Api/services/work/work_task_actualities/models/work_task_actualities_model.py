from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskActualitiesModel(BaseModel):
    name: str
    toBeExpiredAfterMinutes: Optional[int] = None
    isTillNextDay: Optional[bool] = None
    color: Optional[str] = None
    sortOrder: Optional[int] = None


class SuccessGetListTaskActualitiesModel(RootModel):
    root: Dict[str, TaskActualitiesModel]
