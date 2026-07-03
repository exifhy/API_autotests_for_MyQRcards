from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_actions.account_actions_web_account_verification.endpoints import Endpoints
from services.account_actions.account_actions_web_account_verification.models.account_action_create_model import (
    AccountActionCreateModel,
)
from services.account_actions.account_actions_web_account_verification.payloads import Payloads
from src.support.helper import Helper


class AccountActionsWebAccountVerificationAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accountActions/WebAccountVerification")
    def create_web_account_verification(
        self,
        *,
        push_token: str,
        client_name: str,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountActionCreateModel, dict]:
        request_payload = payload or Payloads.build_web_account_verification_payload(
            push_token=push_token,
            client_name=client_name,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_web_account_verification_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (
            HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED,
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT,
        ), f"Unexpected status on WebAccountVerification: {response.status_code}: {response.text}"
        data = response.json() if response.text else {}
        if isinstance(data, list):
            data = {"errors": data}
        return response, AccountActionCreateModel(**data), request_payload

    @allure.step("POST /accountActions/WebAccountVerification/silent")
    def create_web_account_verification_silent(
        self,
        *,
        push_token: str,
        client_name: str,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountActionCreateModel, dict]:
        request_payload = payload or Payloads.build_web_account_verification_payload(
            push_token=push_token,
            client_name=client_name,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_web_account_verification_silent_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (
            HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED,
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT,
        ), f"Unexpected status on WebAccountVerification/silent: {response.status_code}: {response.text}"
        data = response.json() if response.text else {}
        if isinstance(data, list):
            data = {"errors": data}
        return response, AccountActionCreateModel(**data), request_payload
