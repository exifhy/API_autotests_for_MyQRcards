from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_sso_providers.endpoints import Endpoints
from services.accounts.accounts_sso_providers.models.sso_providers_model import SsoProviderModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsSsoProvidersAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/sso/providers")
    def get_sso_providers(self) -> tuple[object, list[SsoProviderModel]]:
        response = self._call(
            "GET",
            url=self.endpoints.get_sso_providers_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200 or 204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return response, []
        data = response.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}: {data}"
        return response, [SsoProviderModel(**item) for item in data]

    @allure.step("GET /Accounts/sso/providers without auth")
    def get_sso_providers_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_sso_providers_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        return response
