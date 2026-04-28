from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_actions.account_actions_subscription_invitation.endpoints import Endpoints
from services.account_actions.account_actions_subscription_invitation.payloads import Payloads
from services.account_actions.account_actions_web_account_verification.models.account_action_create_model import (
    AccountActionCreateModel,
)
from src.support.helper import Helper


class AccountActionsSubscriptionInvitationAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /accountActions/SubscriptionInvitation")
    def create_subscription_invitation_action(
        self,
        *,
        push_token: str,
        client_name: str,
        payload: dict | None = None,
    ) -> tuple[requests.Response, AccountActionCreateModel, dict]:
        request_payload = payload or Payloads.build_subscription_invitation_action_payload(
            push_token=push_token,
            client_name=client_name,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_subscription_invitation_action_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (
            HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED,
            HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT,
        ), f"Unexpected status on SubscriptionInvitation: {response.status_code}: {response.text}"
        data = response.json() if response.text else {}
        if isinstance(data, list):
            data = {"errors": data}
        return response, AccountActionCreateModel(**data), request_payload
