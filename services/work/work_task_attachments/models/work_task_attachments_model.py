from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class TaskAttachmentsModel(BaseModel):
    taskID: int
    attachmentID: int
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class SuccessTaskAttachmentsModel(BaseModel):
    result: List[TaskAttachmentsModel]
