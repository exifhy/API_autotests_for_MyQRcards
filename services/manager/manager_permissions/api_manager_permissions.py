from http import HTTPStatus

import allure

from config.headers import Headers
from services.manager.manager_permissions.endpoints import Endpoints
from services.manager.manager_permissions.models.manager_permissions_model import (
    ManagerPermissionItemModel,
    ManagerPermissionsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_manager_jwt, get_token


class ManagerPermissionsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Manager/permissions")
    def get_manager_permissions(self) -> ManagerPermissionsModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_manager_permissions_endpoint,
            headers=Headers.auth_header(bearer_token=get_manager_jwt()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}: {data}"
        return ManagerPermissionsModel(items=[ManagerPermissionItemModel(**item) for item in data])

    @allure.step("GET /Manager/permissions (raw, no assert — for negative/non-manager cases)")
    def get_manager_permissions_raw(self):
        return self._call(
            "GET",
            url=self.endpoints.get_manager_permissions_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("GET /Manager/permissions without auth")
    def get_manager_permissions_without_auth(self):
        return self._call(
            "GET",
            url=self.endpoints.get_manager_permissions_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
