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


class RolePermissionsApiModel(StrictBaseModel):
    roleID: int
    permissionApiID: int


class RolePermissionsApiListResponseModel(StrictBaseModel):
    results: List[RolePermissionsApiModel]
