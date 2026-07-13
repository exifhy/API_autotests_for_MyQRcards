from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class AddResultModel(BaseModel):
    userID: int
    id: int


class SuccessEmploymentAdd(BaseModel):
    list: List[AddResultModel]
