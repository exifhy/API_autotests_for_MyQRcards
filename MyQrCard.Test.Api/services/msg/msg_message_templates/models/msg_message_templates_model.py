from datetime import datetime
from pydantic import BaseModel, RootModel, ConfigDict
from typing import List, Optional, Dict



class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddMessageTemplatesModel(StrictBaseModel):
    results: List[int]


class MessageTemplatesModel(StrictBaseModel):
    id: int
    description: Optional[str] = None
    subject: Optional[str] = None
    validated: Optional[datetime] = None
    isValid: bool
    providerID: int
    applicationID: Optional[int] = None
    navigateToID: Optional[int] = None
    contentTypeID: int


class SuccessMessageTemplatesModel(RootModel):
    root: Dict[str, MessageTemplatesModel]


class IdCodeNameResult(StrictBaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None


class GetMessageTemplatesModel(StrictBaseModel):
    id: int
    description: Optional[str] = None
    subject: Optional[str] = None
    validated: Optional[datetime] = None
    isValid: bool
    provider: Optional[IdCodeNameResult] = None
    application: Optional[IdCodeNameResult] = None
    navigateTo: Optional[IdCodeNameResult] = None
    contentType: Optional[IdCodeNameResult] = None
    content: Optional[str] = None
    deleted: Optional[datetime] = None