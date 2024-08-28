from pydantic import BaseModel
from typing import List, Optional, Dict


class SuccessAddLocationModel(BaseModel):
    location: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]