from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_actions.account_actions_mobile_account_notification_send.endpoints import Endpoints
from services.account_actions.account_actions_mobile_account_notification_send.payloads import Payloads
from services.account_actions.account_actions_web_account_verification.models.account_action_create_model import (
    AccountActionCreateModel,
)
from src.support.helper import Helper


class AccountActionsMobileAccountNotificationSendAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accountActions/MobileAccountNotificationSend")
    def create_mobile_account_notification_send(
        self,
        *,
        push_token: str,
        guid: str,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountActionCreateModel, dict]:
        request_payload = payload or Payloads.build_mobile_account_notification_send_payload(
            push_token=push_token,
            guid=guid,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_mobile_account_notification_send_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (
            HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED,
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT,
        ), f"Unexpected status on MobileAccountNotificationSend: {response.status_code}: {response.text}"
        data = response.json() if response.text else {}
        if isinstance(data, list):
            data = {"errors": data}
        return response, AccountActionCreateModel(**data), request_payload
