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


class PermissionsExtTagListResultModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    permissionExtID: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None


class PermissionsExtTagListResponseModel(RootModel):
    root: Dict[str, List[PermissionsExtTagListResultModel]]
