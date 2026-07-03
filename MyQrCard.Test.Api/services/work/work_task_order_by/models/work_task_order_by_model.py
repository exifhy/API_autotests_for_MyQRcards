from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskOrderByModel(BaseModel):
    name: str
    code: str


class SuccessGetTaskOrderByModels(RootModel):
    root: Dict[str, TaskOrderByModel]
