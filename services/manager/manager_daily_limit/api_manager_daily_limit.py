from http import HTTPStatus

import allure

from config.headers import Headers
from services.manager.manager_daily_limit.endpoints import Endpoints
from services.manager.manager_daily_limit.models.manager_daily_limit_model import ManagerDailyLimitModel
from src.support.helper import Helper
from src.support.token_utils import get_manager_jwt, get_token


class ManagerDailyLimitAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Manager/dailylimit")
    def get_manager_daily_limit(self) -> ManagerDailyLimitModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_manager_daily_limit_endpoint,
            headers=Headers.auth_header(bearer_token=get_manager_jwt()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return ManagerDailyLimitModel(**response.json())

    @allure.step("GET /Manager/dailylimit (raw, no assert — for negative/non-manager cases)")
    def get_manager_daily_limit_raw(self):
        return self._call(
            "GET",
            url=self.endpoints.get_manager_daily_limit_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("GET /Manager/dailylimit without auth")
    def get_manager_daily_limit_without_auth(self):
        return self._call(
            "GET",
            url=self.endpoints.get_manager_daily_limit_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
