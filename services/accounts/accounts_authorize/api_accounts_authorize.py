from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_authorize.endpoints import Endpoints
from services.accounts.accounts_authorize.models.accounts_authorize_model import AccountsAuthorizeModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsAuthorizeAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accounts/authorize")
    def authorize_account(self, payload: dict | None = None) -> tuple[requests.Response, AccountsAuthorizeModel]:
        response = self._call(
            "POST",
            url=self.endpoints.authorize_account_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return response, AccountsAuthorizeModel(**response.json())

    @allure.step("POST /accounts/authorize (with access token)")
    def authorize_account_with_token(
        self,
        bearer_token: str,
        app_id: str | None = None,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountsAuthorizeModel]:
        response = self._call(
            "POST",
            url=self.endpoints.authorize_account_endpoint,
            headers=Headers.auth_header(bearer_token=bearer_token, app_id=app_id),
            json=payload,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        return response, AccountsAuthorizeModel(**response.json())

    @allure.step("POST /accounts/authorize without auth")
    def authorize_account_without_auth(self, payload: dict | None = None):
        response = self._call(
            "POST",
            url=self.endpoints.authorize_account_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
