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


class PermissionsApiListResultModel(StrictBaseModel):
    code: str
    description: str


class PermissionsApiListResponseModel(RootModel):
    root: Dict[str, PermissionsApiListResultModel]
