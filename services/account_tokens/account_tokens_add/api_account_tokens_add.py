from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_tokens.account_tokens_add.endpoints import Endpoints
from services.account_tokens.account_tokens_add.models.account_tokens_add_model import AccountTokenAddModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountTokensAddAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accounttokens/")
    def add_account_token(self) -> tuple[requests.Response, AccountTokenAddModel]:
        response = self._call(
            "POST",
            url=self.endpoints.add_account_token_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return response, AccountTokenAddModel(**data)

    @allure.step("POST /accounttokens/ without auth")
    def add_account_token_without_auth(self) -> requests.Response:
        response = self._call(
            "POST",
            url=self.endpoints.add_account_token_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
