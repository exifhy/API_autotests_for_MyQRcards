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


class PermissionsUiTagResultModel(StrictBaseModel):
    id: int
    name: Optional[str] = None
    permissionUiID: int
    code: Optional[str] = None
    description: Optional[str] = None
    mustBeAssignedToRole: Optional[bool] = None
    allowReadonlyOnly: Optional[bool] = None
    allowRewritableOnly: Optional[bool] = None


class PermissionsUiTagsListResponseModel(RootModel):
    root: Dict[str, List[PermissionsUiTagResultModel]]
