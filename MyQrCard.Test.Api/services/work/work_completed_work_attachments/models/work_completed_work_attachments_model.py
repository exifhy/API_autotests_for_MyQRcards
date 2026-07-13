from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class CompletedWorkAttachmentsModel(BaseModel):
    taskID: int
    completedWorkID: int
    attachmentID: int
    md5Hash: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None


class SuccessCompletedWorkAttachmentsModel(BaseModel):
    result: List[CompletedWorkAttachmentsModel]
