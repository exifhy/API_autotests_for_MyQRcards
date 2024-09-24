from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class ApplicationResult(BaseModel):
    code: str
    nameRu: str


class SuccessGetApplicationResultModel(RootModel):
    root: Dict[str, ApplicationResult]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
