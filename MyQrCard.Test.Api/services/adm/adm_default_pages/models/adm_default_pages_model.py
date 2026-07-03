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


class DefaultPagesModel(StrictBaseModel):
    tenantID: int
    code: Optional[str] = None
    version: Optional[str] = None
    nameRu: Optional[str] = None
    resourceID: Optional[int] = None
    resourceNameRu: Optional[str] = None


class SuccessGetDefaultPagesModel(StrictBaseModel):
    results: List[DefaultPagesModel]