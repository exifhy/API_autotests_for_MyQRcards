from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_tokens.account_tokens_get.endpoints import Endpoints
from services.account_tokens.account_tokens_get.models.account_tokens_get_model import AccountTokenGetModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountTokensGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounttokens/{token}")
    def get_account_token(self, token: str) -> tuple[requests.Response, AccountTokenGetModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_account_token_endpoint.format(token=token),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return response, AccountTokenGetModel(**data)

    @allure.step("GET /accounttokens/{token} without auth")
    def get_account_token_without_auth(self, token: str) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_account_token_endpoint.format(token=token),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
