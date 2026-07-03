from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class AttachmentsToAssetTemplateModel(StrictBaseModel):
    assetTemplateID: int
    attachmentID: int


class SuccessBindAttachmentsToAssetTemplateModel(StrictBaseModel):
    result: List[AttachmentsToAssetTemplateModel]


class SuccessUploadBindAttachmentToTemplateModel(StrictBaseModel):
    assetTemplateID: int
    attachmentID: int
    checkSum: Optional[str] = None
    fileName: str
    isProtected: Optional[bool] = None
