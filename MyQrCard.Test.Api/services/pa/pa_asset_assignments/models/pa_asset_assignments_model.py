from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, RootModel, ConfigDict, Field
from datetime import datetime


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdNameDeletedResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    deleted: Optional[datetime] = None


class UserResult(StrictBaseModel):
    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    avatarUrl: Optional[str] = None
    deleted: Optional[datetime] = None


class AssetResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    host: Optional[IdNameDeletedResult] = None
    deleted: Optional[datetime] = None
    parentID: Optional[int] = None


class PeriodResult(StrictBaseModel):
    from_: Optional[datetime] = Field(None, alias="from")
    till: Optional[datetime] = None


class AssetAssignmentsListResult(StrictBaseModel):
    user: Optional[UserResult] = None
    asset: Optional[AssetResult] = None
    validityPeriod: Optional[PeriodResult] = None
    notes: Optional[str] = None


class AssetAssignmentsListResponse(StrictBaseModel):
    results: List[AssetAssignmentsListResult]
