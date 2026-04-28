import uuid
from http import HTTPStatus

import allure
import requests

from services.subscriptions.subscription_request.endpoints import Endpoints
from src.support.helper import Helper


class SubscriptionRequestAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @staticmethod
    def random_email() -> str:
        return f"autotest_{uuid.uuid4().hex[:8]}@autotest.dev"

    @staticmethod
    def build_payload(*, email: str | None = None) -> dict:
        return {
            "Email": email or SubscriptionRequestAPI.random_email(),
            "CompanyName": "AutoTest Company",
            "FirstName": "Auto",
            "LastName": "Test",
            "MobilePhone": "+79000000001",
            "Position": "Tester",
            "InvitationsLimit": 100,
        }

    @allure.step("POST /Subscriptions/request")
    def create_subscription_request(self, *, email: str | None = None) -> requests.Response:
        response = self._call(
            "POST",
            url=self.endpoints.subscription_request_endpoint,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=self.build_payload(email=email),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected 200/201/202/204, got {response.status_code}: {response.text}"
        return response
