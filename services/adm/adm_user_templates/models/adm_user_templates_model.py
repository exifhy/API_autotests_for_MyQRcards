from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, RootModel, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class IdNameDescriptionResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None


class BanResult(StrictBaseModel):
    dateTill: Optional[datetime] = None
    banReason: Optional[IdNameDescriptionResult] = None


class IdNameResult(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class UserTemplatesListResultModel(StrictBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    isTechnician: bool
    isTeam: bool
    isCustomer: bool
    banned: Optional[BanResult] = None
    defaultLocationID: Optional[int] = None
    mobilityID: Optional[int] = None
    geoTrackingModeID: Optional[int] = None
    districts: Optional[List[IdNameResult]] = None
    roles: Optional[List[IdNameResult]] = None


class SuccessGetUserTemplatesListResultModel(RootModel):
    root: Dict[str, UserTemplatesListResultModel]


class SuccessAddUserTemplatesModel(StrictBaseModel):
    results: List[int]


class DefaultLocationResult(StrictBaseModel):
    coordinate: Optional[str] = None
    timeZone: Optional[IdNameResult] = None
    id: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None


class UserTemplateGetResult(StrictBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    isTechnician: bool
    isTeam: bool
    isCustomer: bool
    banned: Optional[BanResult] = None
    defaultLocation: Optional[DefaultLocationResult] = None
    mobility: Optional[IdNameResult] = None
    geoTrackingMode: Optional[IdNameResult] = None


class UserTemplatesListResultDistrictsModel(StrictBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    isTechnician: Optional[bool] = None
    isTeam: Optional[bool] = None
    isCustomer: Optional[bool] = None
    banned: Optional[BanResult] = None
    defaultLocationID: Optional[int] = None
    mobilityID: Optional[int] = None
    geoTrackingModeID: Optional[int] = None
    districts: Optional[List[IdNameResult]] = None
    roles: Optional[List[IdNameResult]] = None


class SuccessGetUserTemplatesListResultDistrictsModel(StrictBaseModel):
    results: List[UserTemplatesListResultDistrictsModel]


class SuccessGetUserTemplatesRolesModel(StrictBaseModel):
    results: List[IdNameResult]
