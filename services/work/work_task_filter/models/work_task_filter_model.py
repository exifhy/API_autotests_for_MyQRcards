from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskFilterModel(BaseModel):
    id: int
    name: str
    isAttribute: bool
    isSelected: bool
    sortOrder: int


class SuccessGetListTaskFilterModel(BaseModel):
    result: List[TaskFilterModel]
