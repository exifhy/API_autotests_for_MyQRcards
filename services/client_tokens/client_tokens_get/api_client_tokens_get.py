from http import HTTPStatus

import allure

from config.headers import Headers
from services.client_tokens.client_tokens_get.endpoints import Endpoints
from services.client_tokens.client_tokens_get.models.client_tokens_get_model import (
    ClientTokensGetModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class ClientTokensGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /clientTokens")
    def get_client_tokens(self) -> ClientTokensGetModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_client_tokens_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT:
            return ClientTokensGetModel()

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        return ClientTokensGetModel(**data)

    @allure.step("GET /clientTokens without auth")
    def get_client_tokens_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_client_tokens_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

