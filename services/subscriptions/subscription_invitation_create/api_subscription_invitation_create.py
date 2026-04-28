from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_invitation_create.endpoints import Endpoints
from services.subscriptions.subscription_invitation_create.models.subscription_invitation_create_model import (
    SubscriptionInvitationCreateModel,
)
from services.subscriptions.subscription_invitation_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionInvitationCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Subscriptions/{sub_id}/invitation")
    def create_subscription_invitation(
        self,
        sub_id: int,
        *,
        company_id: int,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        position: str = "Director",
        is_accept_advertising: bool = False,
    ) -> tuple[requests.Response, SubscriptionInvitationCreateModel, dict]:
        payload = Payloads.build_subscription_invitation_payload(
            company_id=company_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            position=position,
            is_accept_advertising=is_accept_advertising,
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_subscription_invitation_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Expected HTTPStatus.OK/HTTPStatus.CREATED/HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, SubscriptionInvitationCreateModel(**(response.json() if response.text else {})), payload
