from pydantic import BaseModel
from typing import List, Optional, Dict


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class BindAttachmentsAndCompanyModel(BaseModel):
    companyID: int
    attachmentID: int


class SuccessBindAttachmentsAndCompanyModel(BaseModel):
    result: List[BindAttachmentsAndCompanyModel]


class SuccessUploadCompanyAttachmentsModel(BaseModel):
    companyID: int
    attachmentID: int
    checkSum: str
    fileName: str
    isProtected: bool
