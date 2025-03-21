from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel,  ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class TaskTypesModel(StrictBaseModel):
    name: str
    numberMask: str
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None


class SuccessGetListTaskTypesModel(RootModel):
    root: Dict[str, TaskTypesModel]


class IdNameDeletedResult(StrictBaseModel):
    deleted: Optional[datetime] = None
    name: Optional[str] = None
    id: Optional[int] = None


class SuccessGetRouteResultModel(StrictBaseModel):
    startTaskStage: Optional[IdNameDeletedResult] = None
    finishTaskStage: Optional[IdNameDeletedResult] = None
    startTaskStatus: Optional[IdNameDeletedResult] = None


class TaskTypesIdModel(StrictBaseModel):
    results: List[int]


class DistrictsTaskTypesModel(StrictBaseModel):
    districtName: str
    parentID: Optional[int] = None


class SuccessGetListDistrictsTaskTypesModel(RootModel):
    root: Dict[str, DistrictsTaskTypesModel]


class IdNameModel(StrictBaseModel):
    id: int
    name: str


class GetListWorkTypesTaskTypes(StrictBaseModel):
    results: Dict[str, str]


class GetTaskTypesModel(StrictBaseModel):
    route: SuccessGetRouteResultModel
    name: str
    numberMask: str
    closeMinutes: Optional[int] = None
    isDefault: Optional[bool] = None

