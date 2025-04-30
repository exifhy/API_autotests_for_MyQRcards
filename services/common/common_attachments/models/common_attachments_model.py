from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, RootModel


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessUploadAttachmentsToServerDataFromFormModel(StrictBaseModel):
    attachmentID: int
    checkSum: str
    fileName: str
    isProtected: bool


class SuccessUploadAttachmentsToServerDataFromFormV2Model(StrictBaseModel):
    results: List[SuccessUploadAttachmentsToServerDataFromFormModel]


class SuccessGetAttachmentModel(StrictBaseModel):
    fileName: str
    url: str
    size: int
    created: datetime


class AttachmentsListResultModel(StrictBaseModel):
    id: int
    fileName: str
    description: Optional[str] = None
    publicUrl: Optional[str] = None
    isUploaded: bool
    isProtected: bool
    size: int
    created: datetime


class SuccessGetAttachmentsListResultModel(RootModel):
    root: Dict[str, AttachmentsListResultModel]


class PublishAttachmentModel(StrictBaseModel):
    attachmentID: int
    publicUrl: str


class HttpHeader(StrictBaseModel):
    name: str
    value: str


class DownloadLinkResultModel(StrictBaseModel):
    downloadUrl: str
    headers: List[HttpHeader]
    expiresAfter: datetime
    failures: Optional[List[str]] = None


class SuccessGetListRolesAttachmentModel(RootModel):
    root: str
