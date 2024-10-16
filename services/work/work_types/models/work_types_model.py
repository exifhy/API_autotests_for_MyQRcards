from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel


class SuccessAddWorkTypesModel(BaseModel):
    type: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class CostCurrency(BaseModel):
    id: Optional[int] = None
    shortName: Optional[str] = None
    asciiCode: Optional[str] = None


class SuccessResultWorkTypeModel(BaseModel):
    id: Optional[int] = None
    relatedWorkTypes: Optional[Dict[str, str]] = None
    workClassID: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parentID: Optional[int] = None
    hasChildren: Optional[bool] = None
    normalWorkingHours: Optional[int] = None
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None
    published: Optional[datetime] = None
    cost: Optional[float] = None
    costCurrency: Optional[CostCurrency] = None
    erpID: Optional[str] = None


class WorkTypesListResult(BaseModel):
    workClassID: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    parentID: Optional[int] = None
    hasChildren: Optional[bool] = None
    normalWorkingHours: Optional[int] = None
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None
    published: Optional[str] = None
    cost: Optional[float] = None
    costCurrency: Optional[CostCurrency] = None
    erpID: Optional[str] = None


class SuccessGetWorkTypesModel(RootModel):
    root: Optional[Dict[str, WorkTypesListResult]] = None
