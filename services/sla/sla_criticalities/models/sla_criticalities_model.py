from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ListCriticalitiesModel(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    isDefault: Optional[bool] = None
    sortOrder: Optional[int] = None


class SuccessGetListCriticalitiesModel(RootModel):
    root: Dict[str, ListCriticalitiesModel]
