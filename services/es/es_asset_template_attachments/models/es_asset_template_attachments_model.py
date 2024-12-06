from typing import Optional, Dict, List
from pydantic import BaseModel


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class AttachmentsToAssetTemplateModel(BaseModel):
    assetTemplateID: int
    attachmentID: int


class SuccessBindAttachmentsToAssetTemplateModel(BaseModel):
    result: List[AttachmentsToAssetTemplateModel]


class SuccessUploadBindAttachmentToTemplateModel(BaseModel):
    assetTemplateID: int
    attachmentID: int
    checkSum: Optional[str] = None
    fileName: str
    isProtected: bool
