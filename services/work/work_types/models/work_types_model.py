from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SuccessAddWorkTypesModel(StrictBaseModel):
    type: List[int]


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class CostCurrency(StrictBaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class SuccessResultWorkTypeModel(StrictBaseModel):
    id: Optional[int] = None
    relatedWorkTypes: Optional[Dict[str, str]] = None
    workClassID: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parentID: Optional[int] = None
    hasChildren: Optional[bool] = None
    normalWorkingHours: Optional[int] = None
    normalWorkingMinutes: Optional[int] = None
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None
    published: Optional[datetime] = None
    cost: Optional[float] = None
    costCurrency: Optional[CostCurrency] = None
    erpID: Optional[str] = None


class WorkTypesListResult(StrictBaseModel):
    workClassID: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parentID: Optional[int] = None
    hasChildren: Optional[bool] = None
    normalWorkingHours: Optional[int] = None
    normalWorkingMinutes: Optional[int] = None
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None
    published: Optional[str] = None
    cost: Optional[float] = None
    costCurrency: Optional[CostCurrency] = None
    erpID: Optional[str] = None


class SuccessGetWorkTypesModel(RootModel):
    root: Optional[Dict[str, WorkTypesListResult]] = None


class CheckListsModel(StrictBaseModel):
    deleted: Optional[datetime] = None
    description: Optional[str] = None
    name: str
    id: int


class SuccessGetResultCheckListsModel(RootModel):
    root: Dict[str, List[CheckListsModel]]


class IdNameModel(StrictBaseModel):
    id: int
    name: str


class SuccessGetListTaskTypesModel(StrictBaseModel):
    results: Dict[str, str]
