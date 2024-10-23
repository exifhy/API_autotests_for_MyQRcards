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
