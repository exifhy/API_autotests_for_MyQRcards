from pydantic import BaseModel
from typing import List, Optional, Dict


class SuccessAddDistrictsModel(BaseModel):
    districts: List[int]


class CodeMessageModel(BaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(BaseModel):
    list_model: List[CodeMessageModel]


class PathDistrictModel(BaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetInfoDistrictModel(BaseModel):
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


class SuccessGetListInfoDistrictsModel(BaseModel):
    result: List[SuccessGetInfoDistrictModel]

