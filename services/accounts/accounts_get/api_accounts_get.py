from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_get.endpoints import Endpoints
from services.accounts.accounts_get.models.accounts_get_model import AccountGetModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsGetAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/{account_id}")
    def get_account(self, account_id: int) -> AccountGetModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_account_endpoint.format(account_id=account_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else {}
        resp_id = data.get("id", data.get("Id"))
        assert resp_id is not None, f"No id field in response: {data}"
        assert int(resp_id) == int(account_id), f"Expected id={account_id}, got {resp_id}"

        normalized = {
            "id": int(resp_id),
            "email": data.get("email", data.get("Email")),
            "firstName": data.get("firstName", data.get("FirstName")),
            "lastName": data.get("lastName", data.get("LastName")),
        }
        return AccountGetModel(**normalized)

    @allure.step("GET /accounts/{account_id} without auth")
    def get_account_without_auth(self, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_account_endpoint.format(account_id=account_id),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
