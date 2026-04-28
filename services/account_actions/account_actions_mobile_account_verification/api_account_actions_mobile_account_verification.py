from http import HTTPStatus

import allure
import os
import requests
from requests.auth import HTTPBasicAuth

from config.headers import Headers
from services.account_actions.account_actions_mobile_account_verification.endpoints import Endpoints
from services.account_actions.account_actions_mobile_account_verification.payloads import Payloads
from services.account_actions.account_actions_web_account_verification.models.account_action_create_model import (
    AccountActionCreateModel,
)
from src.support.helper import Helper


class AccountActionsMobileAccountVerificationAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accountActions/MobileAccountVerification")
    def create_mobile_account_verification(
        self,
        *,
        push_token: str,
        client_name: str,
        is_accept_advertising: bool = False,
        basic_login: str | None = None,
        basic_password: str | None = None,
        app_id: str | None = None,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountActionCreateModel, dict]:
        request_payload = payload or Payloads.build_mobile_account_verification_payload(
            push_token=push_token,
            client_name=client_name,
            is_accept_advertising=is_accept_advertising,
        )
        headers = Headers.without_authorization_field_header(app_id=app_id or os.getenv("APP_ID") or "3")
        login = basic_login or os.getenv("ACCOUNT_ACTIONS_BASIC_LOGIN")
        password = basic_password or os.getenv("ACCOUNT_ACTIONS_BASIC_PASSWORD")
        assert login, "ACCOUNT_ACTIONS_BASIC_LOGIN is not set"
        assert password, "ACCOUNT_ACTIONS_BASIC_PASSWORD is not set"
        response = self._call(
            "POST",
            url=self.endpoints.create_mobile_account_verification_endpoint,
            headers=headers,
            json=request_payload,
            auth=HTTPBasicAuth(login, password),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.CONFLICT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.CREATED/HTTPStatus.ACCEPTED/HTTPStatus.CONFLICT, got {response.status_code}: {response.text}"
        data = response.json() if response.text else {}
        if isinstance(data, list):
            data = {"errors": data}
        return response, AccountActionCreateModel(**data), request_payload
