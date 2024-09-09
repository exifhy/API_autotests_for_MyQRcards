from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ResultModel(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


class SuccessTasksResultModel(BaseModel):
    list: Optional[List[ResultModel]] = None

