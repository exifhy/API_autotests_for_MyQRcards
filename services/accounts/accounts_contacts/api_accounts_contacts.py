from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_contacts.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsContactsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/contacts")
    def get_contacts(self, params: dict | None = None):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_contacts_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params=params,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        return response
