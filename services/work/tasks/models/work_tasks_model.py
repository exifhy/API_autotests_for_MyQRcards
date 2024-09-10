from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddTasksModel(BaseModel):
    id: int
    number: str


class ResultDeleteModel(BaseModel):
    tenantID: Optional[int] = None
    taskID: Optional[int] = None
    error: Optional[str] = None


class SuccessDeleteTaskModel(BaseModel):
    list: Optional[List[ResultDeleteModel]] = None
