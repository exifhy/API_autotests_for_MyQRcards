from typing import Optional, Dict, List
from pydantic import BaseModel


class FieldResultModel(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


class SuccessExportDataListModel(BaseModel):
    result: Optional[List[FieldResultModel]] = None


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]
