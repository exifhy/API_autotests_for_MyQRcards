from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_accept_advertising.endpoints import Endpoints
from services.accounts.accounts_accept_advertising.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsAcceptAdvertisingAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /accounts/this/acceptAdvertising")
    def update_accept_advertising(self, is_accept_advertising: bool):
        payload = Payloads.build_accept_advertising_payload(is_accept_advertising)
        response = self._call(
            "PUT",
            url=self.endpoints.update_accept_advertising_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload

    @allure.step("PUT /accounts/this/acceptAdvertising (raw payload, no assert — for edge/negative cases)")
    def update_accept_advertising_raw(self, payload: dict):
        return self._call(
            "PUT",
            url=self.endpoints.update_accept_advertising_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )

    @allure.step("PUT /accounts/this/acceptAdvertising without auth")
    def update_accept_advertising_without_auth(self):
        payload = Payloads.build_accept_advertising_payload(True)
        response = self._call(
            "PUT",
            url=self.endpoints.update_accept_advertising_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
