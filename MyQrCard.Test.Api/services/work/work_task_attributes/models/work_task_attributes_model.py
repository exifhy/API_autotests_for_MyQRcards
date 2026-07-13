from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class DomainResultModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None


class TaskAttributesResultModel(BaseModel):
    tenantID: int
    taskID: int
    attributeID: int
    attributeName: Optional[str] = None
    value: Optional[str] = None
    domain: Optional[DomainResultModel] = None
    listOfValues: Optional[Dict[str, str]] = None


class SuccessGetListTaskAttributesResultModel(BaseModel):
    result: List[TaskAttributesResultModel]
