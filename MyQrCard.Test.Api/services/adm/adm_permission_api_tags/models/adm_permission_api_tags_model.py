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


class PermissionsApiTagListResultModel(StrictBaseModel):
    id: int
    name: Optional[str] = None
    permissionApiID: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None


class SuccessGetPermissionsApiTagListResultModel(RootModel):
    root: Dict[str, List[PermissionsApiTagListResultModel]]
