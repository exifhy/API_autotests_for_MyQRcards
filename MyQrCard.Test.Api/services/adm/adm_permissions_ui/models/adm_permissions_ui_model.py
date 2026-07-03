from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class PermissionsUiGetResultModel(StrictBaseModel):
    code: str
    description: Optional[str] = None
    isSystem: bool
    mustBeAssignedToRole: Optional[bool] = None
    allowReadonlyOnly: Optional[bool] = None
    deleted: Optional[datetime] = None
    allowRewritableOnly: Optional[bool] = None


class PermissionsUiGetResponseModel(RootModel):
    root: Dict[str, PermissionsUiGetResultModel]


class PermissionsUiAddResponseModel(StrictBaseModel):
    results: List[int]
