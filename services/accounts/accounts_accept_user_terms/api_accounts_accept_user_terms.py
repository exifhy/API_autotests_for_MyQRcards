from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_accept_user_terms.endpoints import Endpoints
from services.accounts.accounts_accept_user_terms.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsAcceptUserTermsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /accounts/this/acceptUserTerms")
    def accept_user_terms(self):
        payload = Payloads.build_accept_user_terms_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.accept_user_terms_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload

    @allure.step("PUT /accounts/this/acceptUserTerms without auth")
    def accept_user_terms_without_auth(self):
        payload = Payloads.build_accept_user_terms_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.accept_user_terms_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response, payload

