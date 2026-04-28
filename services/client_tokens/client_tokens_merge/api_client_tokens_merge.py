from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.client_tokens.client_tokens_merge.endpoints import Endpoints
from services.client_tokens.client_tokens_merge.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class ClientTokensMergeAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /clientTokens")
    def merge_client_tokens(
        self,
        *,
        client_id: str,
        push_token: str,
        payload: dict | None = None,
    ) -> tuple[requests.Response, dict]:
        request_payload = payload or Payloads.build_client_tokens_merge_payload(
            client_id=client_id,
            push_token=push_token,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.merge_client_tokens_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, request_payload

    @allure.step("PUT /clientTokens without auth")
    def merge_client_tokens_without_auth(
        self,
        *,
        client_id: str,
        push_token: str,
        payload: dict | None = None,
    ):
        request_payload = payload or Payloads.build_client_tokens_merge_payload(
            client_id=client_id,
            push_token=push_token,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.merge_client_tokens_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response, request_payload
