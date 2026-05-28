from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_tokens.account_tokens_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountTokensDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /accounttokens/{token}")
    def delete_account_token(self, token: str) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_account_token_endpoint.format(token=token),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Expected 200/202/204/404, got {response.status_code}: {response.text}"
        return response

    @allure.step("DELETE /accounttokens/{token} without auth")
    def delete_account_token_without_auth(self, token: str) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_account_token_endpoint.format(token=token),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
