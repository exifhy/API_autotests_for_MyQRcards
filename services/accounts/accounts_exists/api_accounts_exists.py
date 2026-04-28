from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_exists.endpoints import Endpoints
from services.accounts.accounts_exists.models.accounts_exists_model import AccountExistsModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsExistsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @staticmethod
    def _to_bool(response: requests.Response) -> bool:
        try:
            data = response.json()
        except Exception:
            value = (response.text or "").strip().lower()
            if value == "true":
                return True
            if value == "false":
                return False
            raise AssertionError(f"Expected bool response body, got: {response.text}")

        if not isinstance(data, bool):
            raise AssertionError(f"Expected bool response body, got: {type(data)} {data}")
        return data

    @allure.step("GET /accounts/Exists")
    def get_exists(self, email: str) -> AccountExistsModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_exists_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            params={"email": email},
        )
        assert response.status_code == HTTPStatus.OK, f"{response.status_code} {response.text}"
        return AccountExistsModel(exists=self._to_bool(response))

