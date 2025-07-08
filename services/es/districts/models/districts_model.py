from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SuccessAddDistrictsModel(StrictBaseModel):
    districts: List[int]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class PathDistrictModel(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetInfoDistrictModel(StrictBaseModel):
    hasChildren: Optional[bool] = None
    path: Optional[PathDistrictModel] = None
    description: Optional[str] = None
    erpID: Optional[str] = None
    parentID: Optional[int] = None
    sortOrder: Optional[int] = None
    usersCount: Optional[int] = None
    assetsCount: Optional[int] = None
    taskTypesCount: Optional[int] = None
    isDefault: Optional[bool] = None
    name: Optional[str] = None
    id: Optional[int] = None
    tenantID: Optional[int] = None
    createdBy: Optional[int] = None
    created: Optional[datetime] = None
    modifiedBy: Optional[int] = None
    modified: Optional[datetime] = None


class SuccessGetListInfoDistrictsModel(StrictBaseModel):
    result: List[SuccessGetInfoDistrictModel]
