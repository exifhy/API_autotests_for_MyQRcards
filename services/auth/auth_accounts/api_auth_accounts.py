from http import HTTPStatus

import allure

from config.headers import Headers
from services.auth.auth_accounts.endpoints import Endpoints
from services.auth.auth_accounts.models.auth_accounts_model import SuccessAccountAddResultEntityModel
from services.auth.auth_accounts.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AuthAccountsAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.endpoints = Endpoints()

    @allure.step("Create account")
    def post_accounts_register(self, email: str, mobile_phone: str, domain_login: str):
        response = self._call(
            "POST",
            url=self.endpoints.post_register_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=self.payloads.post_accounts_register_payload(email, mobile_phone, domain_login),
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Status code {response.status_code}, {response.text}"
        )
        return SuccessAccountAddResultEntityModel(**response.json())
