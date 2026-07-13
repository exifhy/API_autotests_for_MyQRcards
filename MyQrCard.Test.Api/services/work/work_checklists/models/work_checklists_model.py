from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel
from datetime import datetime


class SuccessAddChecklistsToAssetModel(BaseModel):
    result: List[int]


class SuccessGetChecklistByIdResultModel(BaseModel):
    deleted: Optional[datetime] = None
    description: Optional[str] = None
    name: str
    id: int


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class ChecklistsModel(BaseModel):
    assetsCount: Optional[int] = None
    workTypesCount: Optional[int] = None
    sortOrder: Optional[int] = None
    description: Optional[str] = None
    name: str
    id: int


class SuccessGetListChecklistsModel(RootModel):
    root: Dict[str, ChecklistsModel]


class AttributeModel(BaseModel):
    name: str
    id: int


class AttributeTypeResultModel(BaseModel):
    code: str
    name: str
    id: int


class MeasurementUnitResultModel(BaseModel):
    id: int
    name: str
    abbreviation: str
    designation: str


class CheckListItemResultModel(BaseModel):
    name: str
    description: Optional[str] = None
    sortOrder: Optional[int] = None
    attribute: Optional[AttributeModel] = None
    attributeType: Optional[AttributeTypeResultModel] = None
    measurementUnit: Optional[MeasurementUnitResultModel] = None


class SuccessGetListChecklistsItemsModel(RootModel):
    root: Dict[str, CheckListItemResultModel]

