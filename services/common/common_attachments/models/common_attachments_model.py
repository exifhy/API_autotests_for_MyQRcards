from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class SuccessUploadAttachmentsToServerDataFromFormModel(BaseModel):
    attachmentID: Optional[int] = None
    checkSum: Optional[str] = None
    fileName: Optional[str] = None
    isProtected: Optional[bool] = None

