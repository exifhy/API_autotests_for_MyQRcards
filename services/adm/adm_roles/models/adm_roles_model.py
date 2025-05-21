from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, ConfigDict, RootModel


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CodeMessageModel(StrictBaseModel):
    traceIdentifier: str
    code: str
    message: str
    arguments: Optional[Dict[str, str]] = None


class ErrorModel(StrictBaseModel):
    list_model: List[CodeMessageModel]


class SystemRole(StrictBaseModel):
    name: Optional[str] = None
    id: Optional[int] = None


class RolesModel(StrictBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    deleted: Optional[str] = None
    systemRoles: Optional[List[SystemRole]] = None


class SuccessGetListRolesModel(StrictBaseModel):
    results: List[RolesModel]


class RoleApplicationsModel(StrictBaseModel):
    applicationCode: str
    applicationName: str


class RoleApplicationsResponseModel(RootModel):
    root: Dict[str, RoleApplicationsModel]


class RolaAttachmentModel(StrictBaseModel):
    fileName: str
    description: str
    isUploaded: bool
    publicUrl: str
    contentType: str


class RoleAttachmentsListResponseModel(StrictBaseModel):
    results: List[RolaAttachmentModel]


class IdNameResultModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class RoleGetResultResponseModel(StrictBaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    deleted: Optional[datetime] = None
    systemRoles: Optional[List[IdNameResultModel]] = None


class SuccessAddRoleResponseModel(StrictBaseModel):
    results: List[int]


class SuccessAddCopyRolesResponseModel(StrictBaseModel):
    results: List[int]


class RolePermissionsApiResultModel(StrictBaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    permissionApiID: Optional[int] = None
    isChecked: Optional[bool] = None
    systemTag: Optional[IdNameResultModel] = None


class RolePermissionsApiListResponseModel(RootModel):
    root: Dict[str, List[RolePermissionsApiResultModel]]


class RolePermissionsExtResultModel(StrictBaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    permissionExtID: Optional[int] = None
    isChecked: Optional[bool] = None
    systemTag: Optional[IdNameResultModel] = None


class RolePermissionsExtListResponseModel(RootModel):
    root: Dict[str, List[RolePermissionsExtResultModel]]


class RolePermissionsUiListResult(StrictBaseModel):
    capabilityID: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None
    allowReadonlyOnly: Optional[bool] = None
    isSystem: Optional[bool] = None
    mustBeAssignedToRole: Optional[bool] = None
    permissionUiID: Optional[int] = None
    isChecked: Optional[bool] = None
    systemTag: Optional[IdNameResultModel] = None
    allowRewritableOnly: Optional[bool] = None


class RolePermissionsUiListResponseModel(RootModel):
    root: Dict[str, List[RolePermissionsUiListResult]]
