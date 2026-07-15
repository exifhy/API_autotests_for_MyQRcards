from src.models.base import StrictBaseModel


class ManagerPermissionItemModel(StrictBaseModel):
    permissionTypeID: int
    name: str


class ManagerPermissionsModel(StrictBaseModel):
    items: list[ManagerPermissionItemModel]
