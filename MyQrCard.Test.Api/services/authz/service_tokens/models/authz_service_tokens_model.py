from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ServiceTokenModel(BaseModel):
    token: str
    created: datetime
    validTill: datetime


class SuccessGenerateServiceTokenModel(BaseModel):
    result: List[ServiceTokenModel]
