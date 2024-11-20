from typing import Optional, Dict, List
from pydantic import BaseModel
from datetime import datetime


class SuccessAddChecklistsToAssetModel(BaseModel):
    result: List[int]


class SuccessGetChecklistByIdResultModel(BaseModel):
    deleted: Optional[datetime] = None
    description: Optional[str] = None
    name: str
    id: int


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
