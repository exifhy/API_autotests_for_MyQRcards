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


class RoleApplicationModel(StrictBaseModel):
    tenantID: int
    roleID: int
    applicationID: int


class RoleApplicationsListResponseModel(StrictBaseModel):
    results: List[RoleApplicationModel]
