from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, RootModel


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: Optional[str] = None
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SuccessAddWarehousesModel(StrictBaseModel):
    result: List[int]


class WarehousesModel(StrictBaseModel):
    deleted: Optional[str] = None
    deletedBy: Optional[int] = None
    erpID: Optional[str] = None
    isDefault: Optional[bool] = None
    name: str
    id: int


class GetListWarehousesModel(RootModel):
    root: Dict[str, WarehousesModel]


class UsersToWarehousesResponseModel(RootModel):
    root: Dict[str, List[int]]


class UsersWarehousesGetResponseModel(StrictBaseModel):
    userFullName: str
    userID: int


class UsersWarehousesGetListResponseModel(StrictBaseModel):
    results: List[UsersWarehousesGetResponseModel]
