from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_sso_bindings.endpoints import Endpoints
from services.accounts.accounts_sso_bindings.models.sso_bindings_model import SsoBindingModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsSsoBindingsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/sso")
    def get_sso_bindings(self) -> tuple[object, list[SsoBindingModel]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_sso_bindings_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return response, []
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}: {data}"
        return response, [SsoBindingModel(**item) for item in data]

    @allure.step("GET /Accounts/sso without auth")
    def get_sso_bindings_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_sso_bindings_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        return response
