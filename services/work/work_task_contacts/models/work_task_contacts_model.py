from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskContactsModel(BaseModel):
    taskID: int
    contactID: int


class SuccessGetListTaskContactsModel(BaseModel):
    result: List[TaskContactsModel]
