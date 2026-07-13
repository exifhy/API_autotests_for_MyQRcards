from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskMaterialsModel(BaseModel):
    taskID: int
    id: int


class SuccessAddTaskMaterialsModel(BaseModel):
    result: List[TaskMaterialsModel]
